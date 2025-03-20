import json
import os
import re
import argparse
import shutil
import logging
from datetime import datetime
from pathlib import Path
from crewai import Agent, Task, Crew, Process
from dotenv import load_dotenv
import cohere

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Set up Cohere client for direct API calls
cohere_api_key = os.getenv("COHERE_API_KEY")
co = cohere.Client(cohere_api_key)

class CodeReviewerAgent:
    def __init__(self):
        self.agent = Agent(
            role="Code Reviewer",
            goal="Review the generated code for quality and best practices",
            backstory=(
                "You are a senior developer specializing in code reviews. "
                "You ensure that all code is clean, efficient, and follows best practices."
            ),
            verbose=True,
            allow_delegation=False,
            llm=dict(  # Explicit LLM config for Cohere
                provider="cohere",
                config={
                    "model": "command",
                    "api_key": os.getenv("COHERE_API_KEY")
                }
            )
        )

    def review_code(self, code):
        """Review the generated code for quality and best practices."""
        review_task = Task(
            description=f"""
            Review the following code for quality and best practices:
            {code}

            Requirements:
            1. Check for code readability and maintainability.
            2. Ensure best practices are followed.
            3. Identify potential bugs or vulnerabilities.
            4. Provide a detailed review report.
            """,
            agent=self.agent,
            expected_output="Detailed review report with suggestions for improvement"
        )

        crew = Crew(
            agents=[self.agent],
            tasks=[review_task],
            verbose=True,
            process=Process.sequential
        )

        return crew.kickoff()


class ReactFileAgent:
    def __init__(self, file_path):
        self.file_path = file_path
        self.developer_agent = Agent(
            role=f"React Developer for {os.path.basename(file_path)}",
            goal="Implement requested changes to this specific file while maintaining functionality and best practices",
            backstory=(
                "You are a senior React developer specializing in implementing specific "
                "changes to React components while following best practices."
            ),
            verbose=True,
            allow_delegation=False,
            llm=dict(  # Explicit LLM config for Cohere
                provider="cohere",
                config={
                    "model": "command",
                    "api_key": os.getenv("COHERE_API_KEY")
                }
            )
        )
        self.reviewer_agent = CodeReviewerAgent()

    def improve_file(self, improvements):
        """Improve the React file based on the provided improvements."""
        with open(self.file_path, 'r', encoding='utf-8') as f:
            original_code = f.read()

        # Combine all improvements into a single description
        improvements_description = "\n".join(f"- {improvement}" for improvement in improvements)

        # Use Cohere API to generate improved code
        prompt = f"""
        Improve this React file by implementing these specific changes:
        {improvements_description}

        Original code:
        {original_code}

        Requirements:
        1. Provide the complete updated code
        2. Include all imports
        3. Maintain existing functionality
        4. Keep the existing file structure
        5. Return the code in a markdown code block
        """

        response = co.generate(
            prompt=prompt,
            model="command",
            max_tokens=1000,
            temperature=0.7
        )

        improved_code = response.generations[0].text
        improved_code = self._extract_code(improved_code)
        
        # Verify we have valid code
        if not improved_code or 'import' not in improved_code:
            raise ValueError("Failed to generate valid React component code")
        
        # Review the improved code
        review_report = self.reviewer_agent.review_code(improved_code)
        logger.info(f"Code Review Report:\n{review_report}")
        
        return improved_code

    def _extract_code(self, generated_code):
        """Extract code from the generated output."""
        generated_code = str(generated_code)
        
        # Look for code block
        code_block = re.search(r'```(?:javascript|jsx|react)?\n(.*?)\n```', 
                             generated_code, 
                             re.DOTALL)
        
        if code_block:
            return code_block.group(1).strip()
        
        # If no code block found, try to extract content between specific markers
        code_start = generated_code.find('import')
        code_end = generated_code.find('export default')
        
        if code_start != -1 and code_end != -1:
            return generated_code[code_start:code_end+len('export default Camera;')].strip()
            
        # If all else fails, return the original content
        return generated_code.strip()


class ReactProjectManager:
    def __init__(self):
        self.project_dir = ""
        self.backup_path = ""

    def _create_backup(self, project_dir):
        """Create a backup of the project's src directory."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        src_dir = os.path.join(project_dir, 'src')
        
        if not os.path.exists(src_dir):
            raise ValueError(f"Source directory not found: {src_dir}")

        # Create backup of only the src folder
        backup_path = f"{src_dir}_backup_{timestamp}"
        if os.path.exists(backup_path):
            raise FileExistsError(f"Backup directory already exists: {backup_path}")
        
        shutil.copytree(src_dir, backup_path)
        logger.info(f"\n✅ Created backup at: {backup_path}")
        return backup_path

    def _restore_backup(self):
        """Restore the project from the backup."""
        if self.backup_path and os.path.exists(self.backup_path):
            src_dir = self.backup_path.replace(f"_backup_{self.backup_path.split('_backup_')[1]}", '')
            
            if os.path.exists(src_dir):
                shutil.rmtree(src_dir)
            
            shutil.copytree(self.backup_path, src_dir)
            logger.info(f"\n✅ Restored project from backup: {self.backup_path}")

    def execute_project(self, project_dir, file_changes, dry_run=False):
        """Execute the project improvements."""
        self.project_dir = project_dir
        self.backup_path = self._create_backup(project_dir)

        try:
            logger.info("\n" + "="*80)
            logger.info("🚀 STARTING PROJECT EXECUTION")
            logger.info("="*80)

            for file_path, improvements in file_changes.items():
                logger.info(f"\n🛠️ Processing file: {file_path}")
                logger.info(f"📝 Changes requested: {improvements}")

                file_agent = ReactFileAgent(file_path)
                improved_code = file_agent.improve_file(improvements)

                if dry_run:
                    logger.info(f"✅ Dry run - would update: {file_path}")
                    logger.info(f"Generated code:\n{improved_code}")
                else:
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(improved_code)
                    logger.info(f"✅ Successfully updated: {file_path}")

            logger.info("\n" + "="*80)
            logger.info(f"✅ Project completed successfully!")
            logger.info(f"📁 Project location: {project_dir}")
            logger.info(f"💾 Backup at: {self.backup_path}")
            logger.info("="*80)

        except Exception as e:
            self._restore_backup()
            logger.error(f"\n❌ Error: {str(e)}")
            logger.error("Project restored from backup")
            exit(1)


def validate_changes(file_changes):
    """Validate the file changes."""
    for file_path, _ in file_changes.items():
        if not Path(file_path).exists():
            raise FileNotFoundError(f"File not found: {file_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="React Project Improvement System")
    parser.add_argument("project_dir", help="Path to React project directory")
    parser.add_argument("--changes", help="Path to JSON file containing changes or JSON string of changes")
    parser.add_argument("--dry-run", action="store_true", help="Preview changes without modifying files")
    args = parser.parse_args()

    try:
        # Load changes from JSON file or string
        try:
            with open(args.changes, 'r') as f:
                file_changes = json.load(f)
        except (FileNotFoundError, IsADirectoryError):
            file_changes = json.loads(args.changes)

        # Validate changes
        validate_changes(file_changes)

        # Execute the project
        manager = ReactProjectManager()
        manager.execute_project(args.project_dir, file_changes, args.dry_run)

    except Exception as e:
        logger.error(f"\n❌ Error: {str(e)}")
        exit(1)