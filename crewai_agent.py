# crewai_agent.py
import os
from crewai import Agent, Task, Crew
from dotenv import load_dotenv

load_dotenv()

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
            verbose=True,  # Set to True for detailed agent output
            allow_delegation=False
        )

        self.code_reviewer = Agent(
            role="Code Reviewer",
            goal="Ensure the generated code is valid, secure, and follows best practices",
            backstory=(
                "You are a meticulous code reviewer with a sharp eye for detail. "
                "You ensure code is free of vulnerabilities and adheres to best practices."
            ),
            verbose=True,  # Set to True for detailed agent output
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
            verbose=True  # Set to True for detailed crew output
        )

        # Kick off the crew's work
        result = crew.kickoff()
        return result

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="AI Code Generator using CrewAI")
    parser.add_argument("prompt", help="Your code generation request")
    args = parser.parse_args()

    if not args.prompt:
        print("Error: Prompt is required")
        parser.print_help()
        exit(1)

    # Initialize the crew
    crew = CodeGeneratorCrew()
    generated_code = crew.generate_code(args.prompt)

    # Save the output to a file
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, "generated_code.js")

    with open(output_file, "w") as f:
        f.write(generated_code)

    print(f"Code generated and saved to: {output_file}")