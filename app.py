from crewai import Agent, Task, Crew, Process
import os

os.environ["OPENAI_API_BASE"] = "https://api.groq.com/openai/v1"
os.environ["OPENAI_MODEL_NAME"] = "llama3-70b-8192"
os.environ["OPENAI_API_KEY"] = "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"

ticket = "Customer support ticket: Unable to access account"

# Define the Ticket Classifier Agent
classifier = Agent(
    role="Ticket Classifier",
    goal="Accurately classify incoming customer support tickets into relevant categories: urgent, routine, or non-support-related.",
    backstory="You are an AI assistant tasked with classifying incoming customer support tickets to help streamline the support process.",
    verbose=True,
    allow_delegation=False
)

# Define the Ticket Action Agent
action_taker = Agent(
    role="Ticket Action Taker",
    goal="Take appropriate actions based on the classification of the customer support ticket: notify appropriate personnel for urgent issues, assign routine inquiries to relevant support teams, and filter out non-support-related messages.",
    backstory="You are an AI assistant responsible for taking actions on classified customer support tickets to ensure timely resolution.",
    verbose=True,
    allow_delegation=False
)

# Define the Task: Classify the Ticket
classify_ticket = Task(
    description=f"Classify the following support ticket: '{ticket}'",
    agent=classifier,
    expected_output="One of these three options: 'urgent', 'routine', or 'non-support-related'"
)

# Define the Task: Take Action on the Ticket
take_action_on_ticket = Task(
    description=f"Take appropriate action on the support ticket: '{ticket}' based on the classification provided by the 'classifier' agent.",
    agent=action_taker,
    expected_output="An action taken on the ticket based on the classification provided by the 'classifier' agent."
)

# Create the Crew
crew = Crew(
    agents=[classifier, action_taker],
    tasks=[classify_ticket, take_action_on_ticket],
    verbose=True,
    process=Process.sequential
)

# Execute the Crew
output = crew.kickoff()
print(output)