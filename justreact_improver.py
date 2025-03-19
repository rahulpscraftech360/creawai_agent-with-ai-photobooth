import os
from crewai import Agent, Task, Crew, Process
from dotenv import load_dotenv

load_dotenv()

# Set up Groq configuration
os.environ["OPENAI_API_BASE"] = "https://api.groq.com/openai/v1"
os.environ["OPENAI_MODEL_NAME"] = "llama3-70b-8192"
os.environ["OPENAI_API_KEY"] = os.getenv("GROQ_API_KEY")

class ReactImproverCrew:
    def __init__(self):
        self.code_analyzer = Agent(
            role="React Code Analyzer",
            goal="Analyze React components for improvements in performance, patterns, and best practices",
            backstory="You are an expert React developer specializing in code analysis and modern React patterns.",
            verbose=True,
            allow_delegation=False
        )

        self.code_improver = Agent(
            role="React Code Improver",
            goal="Implement suggested improvements while maintaining component functionality",
            backstory="You are a senior React developer who excels at refactoring and modernizing React components.",
            verbose=True,
            allow_delegation=False
        )

    def improve_component(self, original_code, improvements="Analyze and improve the component"):
        analyze_task = Task(
            description=f"Analyze this React component and suggest improvements:\n\n{original_code}",
            agent=self.code_analyzer,
            expected_output="List of specific improvements needed with explanations."
        )

        improve_task = Task(
            description="Implement the suggested improvements while maintaining the component's core functionality",
            agent=self.code_improver,
            expected_output="Improved React component code with explanations of changes made."
        )

        crew = Crew(
            agents=[self.code_analyzer, self.code_improver],
            tasks=[analyze_task, improve_task],
            verbose=True,
            process=Process.sequential
        )

        return crew.kickoff()

def read_react_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        return f.read()

if __name__ == "__main__":
    import argparse
    from datetime import datetime

    parser = argparse.ArgumentParser(description="React Component Improver using CrewAI and Groq")
    parser.add_argument("input_file", help="Path to input React component file")
    parser.add_argument("--improvements", help="Improvements needed (in quotes)", default="Analyze and improve the component")
    parser.add_argument("--output", help="Output directory", default="output")
    args = parser.parse_args()

    try:
        # Read the input React component
        input_code = read_react_file(args.input_file)
        
        # Initialize the crew
        crew = ReactImproverCrew()
        
        # Generate timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Get improvements with the specified requirements
        result = crew.improve_component(input_code, args.improvements)
        generated_code = str(result)

        # Extract the improved code block
        import re
        code_block = re.search(r'```(?:javascript|jsx|react)?\n(.*?)\n```', 
                             generated_code, 
                             re.DOTALL)
        
        if code_block:
            improved_code = code_block.group(1)
        else:
            improved_code = generated_code

        # Save to file
        output_dir = args.output
        os.makedirs(output_dir, exist_ok=True)
        base_name = os.path.splitext(os.path.basename(args.input_file))[0]
        output_file = os.path.join(output_dir, f"{base_name}_improved_{timestamp}.jsx")

        with open(output_file, "w", encoding='utf-8') as f:
            f.write(improved_code)

        print("\n" + "="*80)
        print(f"✅ Component improved successfully!")
        print(f"📁 Original file: {args.input_file}")
        print(f"📁 Improved version saved to: {output_file}")
        print("="*80 + "\n")
        print("Improvements Made:")
        print("-"*80)
        print(generated_code)
        print("-"*80)

    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        print("\nStack trace:")
        import traceback
        print(traceback.format_exc())
        exit(1)