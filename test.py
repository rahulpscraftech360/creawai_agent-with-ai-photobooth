from crewai import Agent, Task, Crew
from langchain_community.chat_models import ChatOpenAI
import os

# Set up your Groq API key
os.environ["GROQ_API_KEY"] = "your_groq_api_key"

# Initialize the Groq LLM using ChatOpenAI (Groq API compatible)

# Initialize the Groq LLM using OpenAI-compatible API
llm = ChatOpenAI(
    model_name="mixtral-8x7b-32768",
    openai_api_key=os.environ["GROQ_API_KEY"],
    openai_api_base="https://api.groq.com/openai/v1"
)

# Define the agent
assistant_agent = Agent(
    name="Simple Assistant",
    role="AI Assistant",
    backstory="An AI assistant designed to help users by answering questions.",
    description="An AI assistant capable of answering questions using AI.",
    goal="Provide helpful and accurate answers to user questions.",
    llm=llm,
)

# Define the task
answer_task = Task(
    name="Answer Question",
    description="Answer user questions to the best of your ability.",
    agent=assistant_agent,
    expected_output="A clear and accurate answer to the user's question.",
)

# Create the crew
crew = Crew(
    agents=[assistant_agent],
    tasks=[answer_task],
)

# Run the crew
if __name__ == "__main__":
    question = input("Ask your question: ")
    crew.kickoff(inputs={"Answer Question": question})