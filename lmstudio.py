import json
import os
import re
import argparse
import shutil
from datetime import datetime
from crewai import Agent, Task, Crew, Process,  LLM, agent



class ReactLMStudioAgent:
    def __init__(self, file_path):
        self.file_path = file_path
        
        # Configure environment for LM Studio
        os.environ["OPENAI_API_KEY"] = "no-key-needed"
        os.environ["OPENAI_API_BASE"] = "http://172.28.128.1:1234/v1"
        
        self.agent = Agent(
            role="React Developer",
            goal="Implement requested changes to React components while maintaining best practices",
            backstory="Senior React developer specializing in clean code and modern React patterns",
            verbose=True,
            allow_delegation=False,
            llm_config={
                "config_list": [{
                    "model": "hermes-3-llama-3.2-3b",
                    "temperature": 0.7,
                    "api_base": "http://172.28.128.1:1234/v1",
                    "api_key": "no-key-needed",
                    "context_window": 4096,
                    "max_tokens": 2048
                }]
            }
        )

    def improve_code(self, requirements):
        with open(self.file_path, 'r', encoding='utf-8') as f:
            original_code = f.read()

        improve_task = Task(
            description=f"""
            Improve this React component according to these requirements:
            {requirements}

            Current code:
            {original_code}

            Instructions:
            1. Return complete updated code
            2. Keep all imports
            3. Maintain existing functionality
            4. Use modern React patterns
            5. Return code in markdown block with ```jsx

            Focus on clean, maintainable code.
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
        return self._extract_code(result)

    def _extract_code(self, generated_code):
        code_block = re.search(r'```(?:jsx|javascript|react)?\n(.*?)\n```', 
                             str(generated_code), 
                             re.DOTALL)
        
        if code_block:
            return code_block.group(1).strip()
        return generated_code.strip()

def main():
    parser = argparse.ArgumentParser(description="React Code Improver using LM Studio")
    parser.add_argument("file_path", help="Path to React component file")
    parser.add_argument("--requirements", help="Improvement requirements")
    args = parser.parse_args()

    try:
        agent = ReactLMStudioAgent(args.file_path)
        improved_code = agent.improve_code(args.requirements)
        
        # Create backup
        backup_path = f"{args.file_path}.backup"
        shutil.copy2(args.file_path, backup_path)
        
        # Write improved code
        with open(args.file_path, 'w', encoding='utf-8') as f:
            f.write(improved_code)
            
        print(f"✅ Successfully improved {args.file_path}")
        print(f"💾 Backup created at {backup_path}")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        if 'backup_path' in locals():
            shutil.copy2(backup_path, args.file_path)
            print("✅ Restored from backup")
        exit(1)

if __name__ == "__main__":
    main()
    
    # python lmstudio.py ./projects/photobooth/src/Camera.jsx --requirements "add dark mode toggle"