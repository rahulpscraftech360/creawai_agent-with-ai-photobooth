import json
import os
import re
import argparse
import shutil
import logging
from datetime import datetime
from pathlib import Path
from crewai import Agent, Task, Crew, Process
from rich.console import Console

# Configure logging with Rich
console = Console()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
isreviewer = False

class CodeReviewerAgent:
    def __init__(self):
        # Configure environment for LM Studio
        os.environ["OPENAI_API_KEY"] = "no-key-needed"
        os.environ["OPENAI_API_BASE"] = "http://172.28.128.1:1234/v1"
        
        self.agent = Agent(
            role="Code Reviewer",
            goal="Review the generated code for quality and best practices",
            backstory="Senior developer specializing in code reviews and best practices",
            verbose=True,
            allow_delegation=False,
            llm_config={
                "model": "hermes-3-llama-3.2-3b",
                "temperature": 0.7,
                "api_base": "http://172.28.128.1:1234/v1",
                "api_key": "no-key-needed",
                "context_window": 131072,
                "max_tokens": 65536
            }
        )

    def review_code(self, code):
        review_task = Task(
            description=f"""
            Review this React code for quality and best practices:
            {code}

            Requirements:
            1. Check code readability and maintainability
            2. Verify React best practices
            3. Identify potential issues
            4. Provide actionable improvements
            5. Return review in markdown format
            """,
            agent=self.agent,
            expected_output="Detailed code review with suggestions"
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
        
        # Configure environment for LM Studio
        os.environ["OPENAI_API_KEY"] = "no-key-needed"
        os.environ["OPENAI_API_BASE"] = "http://172.28.128.1:1234/v1"
        
        self.agent = Agent(
            role="React Developer",
            goal="Implement requested changes while maintaining best practices",
            backstory="Senior React developer specialized in clean, maintainable code",
            verbose=True,
            allow_delegation=False,
            llm_config={
                "model": "hermes-3-llama-3.2-3b",
                "temperature": 0.7,
                "api_base": "http://172.28.128.1:1234/v1",
                "api_key": "no-key-needed",
                "context_window": 131072,
                "max_tokens": 65536
            }
        )
        self.reviewer_agent = CodeReviewerAgent()

    def improve_file(self, improvements):
        with open(self.file_path, 'r', encoding='utf-8') as f:
            original_code = f.read()

        improve_task = Task(
            description=f"""
            Improve this React file by implementing these specific changes:
            {improvements}

            Original code:
            {original_code}

            Requirements:
            1. Provide complete updated code
            2. Include all imports
            3. Maintain existing functionality
            4. Keep the existing file structure
            5. Return code in markdown block with ```jsx
            """,
            agent=self.agent,
            expected_output="Complete updated React component code"
        )

        crew = Crew(
            agents=[self.agent],
            tasks=[improve_task],
            verbose=True,
            process=Process.sequential
        )

        result = crew.kickoff()
        improved_code = self._extract_code(result)
        
        # Get code review if isreviewer is True
        if isreviewer:
            review = self.reviewer_agent.review_code(improved_code)
            console.print("\n[bold cyan]Code Review:[/bold cyan]")
            console.print(review)
        
        return improved_code

    def _extract_code(self, generated_code):
        code_block = re.search(r'```(?:jsx|javascript|react)?\n(.*?)\n```', 
                             str(generated_code), 
                             re.DOTALL)
        
        if code_block:
            return code_block.group(1).strip()
        return generated_code.strip()

class ReactProjectManager:
    def __init__(self):
        self.project_dir = ""
        self.backup_path = ""

    def _create_backup(self, project_dir):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        src_dir = os.path.join(project_dir, 'src')
        
        if not os.path.exists(src_dir):
            raise ValueError(f"Source directory not found: {src_dir}")

        backup_path = f"{src_dir}_backup_{timestamp}"
        shutil.copytree(src_dir, backup_path)
        console.print(f"\n✅ Created backup at: {backup_path}", style="green")
        return backup_path

    def execute_project(self, project_dir, file_changes, dry_run=False):
        self.project_dir = project_dir
        self.backup_path = self._create_backup(project_dir)

        try:
            console.rule("[bold blue]🚀 STARTING PROJECT EXECUTION")

            for file_name, improvements in file_changes.items():
                # Construct full file path relative to src directory
                file_path = os.path.join(self.project_dir, 'src', file_name)
                
                if not os.path.exists(file_path):
                    raise ValueError(f"File not found: {file_path}")

                console.print(f"\n🛠️ Processing: {file_name}", style="yellow")
                console.print(f"📝 Changes: {improvements}", style="cyan")

                file_agent = ReactFileAgent(file_path)
                improved_code = file_agent.improve_file(improvements)

                if dry_run:
                    console.print("✨ Dry run preview:", style="magenta")
                    syntax = Syntax(improved_code, "jsx", theme="monokai")
                    console.print(syntax)
                else:
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(improved_code)
                    console.print(f"✅ Updated: {file_path}", style="green")

            console.rule("[bold green]✅ Project completed successfully!")

        except Exception as e:
            console.print(f"\n❌ Error: {str(e)}", style="bold red")
            self._restore_backup()
            raise

    def _restore_backup(self):
        if self.backup_path and os.path.exists(self.backup_path):
            src_dir = self.backup_path.replace(f"_backup_{self.backup_path.split('_backup_')[1]}", '')
            if os.path.exists(src_dir):
                shutil.rmtree(src_dir)
            shutil.copytree(self.backup_path, src_dir)
            console.print(f"\n✅ Restored from backup: {self.backup_path}", style="green")

def main():
    parser = argparse.ArgumentParser(description="React Project Improvement System")
    parser.add_argument("project_dir", help="Path to React project directory")
    parser.add_argument("--changes", help="Path to JSON file containing changes or JSON string")
    parser.add_argument("--dry-run", action="store_true", help="Preview changes without applying them")
    parser.add_argument("--review", action="store_true", help="Enable code review")
    args = parser.parse_args()

    global isreviewer
    isreviewer = args.review

    try:
        # Try to load as file first, then as JSON string
        try:
            with open(args.changes, 'r') as f:
                file_changes = json.load(f)
        except (FileNotFoundError, IsADirectoryError):
            file_changes = json.loads(args.changes)

        manager = ReactProjectManager()
        manager.execute_project(args.project_dir, file_changes, args.dry_run)

    except Exception as e:
        console.print(f"\n❌ Error: {str(e)}", style="bold red")
        exit(1)

if __name__ == "__main__":
    main()