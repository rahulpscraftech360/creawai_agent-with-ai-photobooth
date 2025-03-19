# crewai_groq_agent.py
import os
from crewai import Agent, Task, Crew, Process
from dotenv import load_dotenv

load_dotenv()

# Set up Groq configuration
os.environ["OPENAI_API_BASE"] = "https://api.groq.com/openai/v1"
os.environ["OPENAI_MODEL_NAME"] = "llama3-70b-8192"
os.environ["OPENAI_API_KEY"] = os.getenv("GROQ_API_KEY")

class CodeGeneratorCrew:
    def __init__(self):
        # Define the agents
        self.code_writer = Agent(
            role="Senior JavaScript Developer",
            goal="Generate clean, efficient, and modern JavaScript code",
            backstory=(
                "You are an expert in JavaScript and modern web development. "
                "You specialize in writing clean, maintainable, and efficient code."
            ),
            verbose=True,
            allow_delegation=False
        )

        self.code_reviewer = Agent(
            role="Code Reviewer",
            goal="Ensure the generated code is valid, secure, and follows best practices",
            backstory=(
                "You are a meticulous code reviewer with a sharp eye for detail. "
                "You ensure code is free of vulnerabilities and adheres to best practices."
            ),
            verbose=True,
            allow_delegation=False
        )

    def generate_code(self, prompt):
        # Define the tasks
        code_generation_task = Task(
            description=f"Generate JavaScript code for: {prompt}",
            agent=self.code_writer,
            expected_output="A complete, valid JavaScript code snippet."
        )

        code_review_task = Task(
            description="Review the generated code for errors, security issues, and best practices",
            agent=self.code_reviewer,
            expected_output="The same code, but improved and validated."
        )

        # Assemble the crew
        crew = Crew(
            agents=[self.code_writer, self.code_reviewer],
            tasks=[code_generation_task, code_review_task],
            verbose=True,
            process=Process.sequential
        )

        # Kick off the crew's work
        result = crew.kickoff()
        return result

if __name__ == "__main__":
    import argparse
    from datetime import datetime

    # Verify Groq API key
    if not os.getenv("GROQ_API_KEY"):
        print("Error: GROQ_API_KEY is missing from .env file.")
        exit(1)

    parser = argparse.ArgumentParser(description="AI Code Generator using CrewAI and Groq")
    parser.add_argument("prompt", help="Your code generation request")
    parser.add_argument("--output", help="Output directory", default="output")
    args = parser.parse_args()

    if not args.prompt:
        print("Error: Prompt is required")
        parser.print_help()
        exit(1)

    # Initialize the crew
    crew = CodeGeneratorCrew()
    try:
        # Generate timestamp for unique filenames
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        result = crew.generate_code(args.prompt)
        generated_code = str(result)

        # Extract just the code block from the result
        import re
        code_block = re.search(r'```(?:javascript|jsx)?\n(.*?)\n```', 
                             generated_code, 
                             re.DOTALL)
        
        if code_block:
            clean_code = code_block.group(1)
        else:
            clean_code = generated_code

        # Save the output to a file
        output_dir = args.output
        os.makedirs(output_dir, exist_ok=True)
        output_file = os.path.join(output_dir, f"generated_code_{timestamp}.js")

        with open(output_file, "w", encoding='utf-8') as f:
            f.write(clean_code)

        print("\n" + "="*80)
        print(f"✅ Code generated successfully!")
        print(f"📁 Saved to: {output_file}")
        print("="*80 + "\n")
        print("Generated Code:")
        print("-"*80)
        print(clean_code)
        print("-"*80)

    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        print("\nStack trace:")
        import traceback
        print(traceback.format_exc())
        exit(1)