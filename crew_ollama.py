import json
import os
import re
import argparse
import shutil
from datetime import datetime
from crewai import Agent, Task, Crew, Process
from dotenv import load_dotenv

load_dotenv()

class ReactFileAgent:
    def __init__(self, file_path):
        self.file_path = file_path
        self.agent = Agent(
            role=f"React Developer for {os.path.basename(file_path)}",
            goal="Implement requested changes to this specific file while maintaining functionality and best practices",
            backstory=(
                "You are a senior React developer specializing in implementing specific "
                "changes to React components while following best practices."
            ),
            verbose=True,
            allow_delegation=False,
            llm="ollama/llama3"  # Use Ollama with Llama3 locally
        )

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
            1. Provide the complete updated code
            2. Include all imports
            3. Maintain existing functionality
            4. Keep the existing file structure
            5. Return the code in a markdown code block
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
        
        # Verify we have valid code
        if not improved_code or 'import' not in improved_code:
            raise ValueError("Failed to generate valid React component code")
            
        return improved_code

    def _extract_code(self, generated_code):
        # Convert CrewAI output to string if needed
        generated_code = str(generated_code)
        
        # Look for code block
        code_block = re.search(r'```(?:javascript|jsx|react)?\n(.*?)\n```', 
                             generated_code, 
                             re.DOTALL)
        
        if code_block:
            # Extract just the code from within the code block
            return code_block.group(1).strip()
        
        # If no code block found, try to extract content between specific markers
        code_start = generated_code.find('import')
        code_end = generated_code.find('export default')
        
        if code_start != -1 and code_end != -1:
            # Include the export statement
            return generated_code[code_start:code_end+len('export default Camera;')].strip()
            
        # If all else fails, return the original content
        return generated_code.strip()

class ReactProjectManager:
    def __init__(self):
        self.project_dir = ""
        self.backup_path = ""
        self.manager = Agent(
            role="Project Manager",
            goal="Coordinate file-specific agents to implement changes",
            backstory=(
                "Experienced technical manager with strong organizational skills "
                "and expertise in React project coordination."
            ),
            verbose=True,
            allow_delegation=True,
            llm="ollama/llama3"  # Use Ollama with Llama3 locally
        )

    def _create_backup(self):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.backup_path = f"{self.project_dir}_backup_{timestamp}"
        shutil.copytree(self.project_dir, self.backup_path)
        print(f"✅ Created backup at: {self.backup_path}")

    def execute_project(self, project_dir, file_changes):
        self.project_dir = project_dir
        self._create_backup()

        try:
            print("\n" + "="*80)
            print("🚀 STARTING PROJECT EXECUTION")
            print("="*80)

            for file_path, improvements in file_changes.items():
                print(f"\n🛠️ Processing file: {file_path}")
                print(f"📝 Changes requested: {improvements}")

                file_agent = ReactFileAgent(file_path)
                improved_code = file_agent.improve_file(improvements)

                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(improved_code)

                print(f"✅ Successfully updated: {file_path}")

            print("\n" + "="*80)
            print(f"✅ Project completed successfully!")
            print(f"📁 Project location: {project_dir}")
            print(f"💾 Backup at: {self.backup_path}")
            print("="*80)

        except Exception as e:
            self._restore_backup()
            print(f"\n❌ Error: {str(e)}")
            print("Project restored from backup")
            exit(1)

    def _restore_backup(self):
        if os.path.exists(self.project_dir):
            shutil.rmtree(self.project_dir)
        shutil.move(self.backup_path, self.project_dir)
        print(f"✅ Restored project from backup: {self.backup_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="React Project Improvement System")
    parser.add_argument("project_dir", help="Path to React project directory")
    parser.add_argument("--changes", help="Path to JSON file containing changes or JSON string of changes")
    args = parser.parse_args()

    try:
        # Try to load as file first, then as JSON string
        try:
            with open(args.changes, 'r') as f:
                file_changes = json.load(f)
        except (FileNotFoundError, IsADirectoryError):
            file_changes = json.loads(args.changes)

        manager = ReactProjectManager()
        manager.execute_project(args.project_dir, file_changes)

    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        exit(1)