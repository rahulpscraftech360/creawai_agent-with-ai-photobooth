import os
from crewai import Agent, Task, Crew, Process
from rich import print
from rich.prompt import Prompt

class ChatAgent:
    def __init__(self):
        # Configure environment for LM Studio
        os.environ["OPENAI_API_KEY"] = "no-key-needed"
        os.environ["OPENAI_API_BASE"] = "http://172.28.128.1:1234/v1"
        
        self.agent = Agent(
            role="Friendly AI Assistant",
            goal="Help users by providing informative and engaging responses",
            backstory="I am a helpful AI assistant with a friendly personality and extensive knowledge",
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

    def chat(self, user_input):
        chat_task = Task(
            description=f"""
            Respond to this user message in a helpful and engaging way:
            {user_input}

            Instructions:
            1. Be concise but informative
            2. Use a friendly tone
            3. If asked for code, provide it in appropriate markdown blocks
            4. If unsure, ask for clarification
            """,
            agent=self.agent,
            expected_output="Helpful response to user query"
        )

        crew = Crew(
            agents=[self.agent],
            tasks=[chat_task],
            verbose=True,
            process=Process.sequential
        )

        return crew.kickoff()

def main():
    chat_agent = ChatAgent()
    print("[bold blue]🤖 AI Chat Assistant[/bold blue]")
    print("[italic]Type 'exit' to end the conversation[/italic]\n")

    while True:
        user_input = Prompt.ask("[bold green]You[/bold green]")
        
        if user_input.lower() == 'exit':
            print("\n[bold blue]👋 Goodbye![/bold blue]")
            break
            
        try:
            response = chat_agent.chat(user_input)
            print(f"\n[bold purple]Assistant[/bold purple]: {response}\n")
        except Exception as e:
            print(f"\n[bold red]❌ Error: {str(e)}[/bold red]\n")

if __name__ == "__main__":
    main()