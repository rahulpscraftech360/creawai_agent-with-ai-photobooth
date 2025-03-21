import os
from crewai import Agent, Task, Crew, Process
from rich import print
from rich.prompt import Prompt
from rich.syntax import Syntax
from rich.console import Console

class CodingAgent:
    def __init__(self):
        # Configure environment for LM Studio
        os.environ["OPENAI_API_KEY"] = "no-key-needed"
        os.environ["OPENAI_API_BASE"] = "http://172.28.128.1:1234/v1"
        
        self.agent = Agent(
            role="Senior Python Developer",
            goal="Write efficient, clean Python code and provide detailed explanations",
            backstory="I am an experienced Python developer specialized in writing clean, maintainable code",
            verbose=True,
            allow_delegation=False,
            allow_code_execution=False,
            llm_config={
                "config_list": [{
                    "model": "hermes-3-llama-3.2-3b",
                    "temperature": 0.7,
                    "api_base": "http://172.28.128.1:1234/v1",
                    "api_key": "no-key-needed",
                     "context_window": 131072,  # Updated to maximum supported tokens
                    "max_tokens": 65536        # Set to half of context window for safe responses
                
                }]
            }
        )
        self.console = Console()

    def code(self, user_input):
        coding_task = Task(
            description=f"""
            Respond to this coding request with implementation and explanation:
            {user_input}

            Instructions:
            1. Provide complete, working code
            2. Include comments explaining key parts
            3. Return code in markdown blocks with language specification
            4. Add any necessary imports
            5. Explain the implementation after the code block
            """,
            agent=self.agent,
            expected_output="Complete code implementation with explanation"
        )

        crew = Crew(
            agents=[self.agent],
            tasks=[coding_task],
            verbose=True,
            process=Process.sequential
        )

        response = crew.kickoff()
        return self._format_response(response)

    def _format_response(self, response):
        # Extract code blocks and format them
        import re
        code_blocks = re.findall(r'```(?:python)?\n(.*?)\n```', str(response), re.DOTALL)
        
        if code_blocks:
            formatted_response = str(response)
            for block in code_blocks:
                syntax = Syntax(block.strip(), "python", theme="monokai")
                formatted_response = formatted_response.replace(
                    f"```python\n{block}```",
                    f"\n{syntax}\n"
                )
            return formatted_response
        return response

def main():
    coding_agent = CodingAgent()
    print("[bold blue]🚀 Python Coding Assistant[/bold blue]")
    print("[italic]Type 'exit' to end the session[/italic]\n")
    print("[yellow]Example commands:[/yellow]")
    print("- Write a function to calculate Fibonacci numbers")
    print("- Create a class for handling API requests")
    print("- Help me optimize this code: <paste code>\n")

    while True:
        user_input = Prompt.ask("[bold green]Code Request[/bold green]")
        
        if user_input.lower() == 'exit':
            print("\n[bold blue]👋 Happy coding![/bold blue]")
            break
            
        try:
            response = coding_agent.code(user_input)
            print(f"\n[bold purple]Solution:[/bold purple]")
            print(response)
            print("\n")
        except Exception as e:
            print(f"\n[bold red]❌ Error: {str(e)}[/bold red]\n")

if __name__ == "__main__":
    main()