from crewai import Agent, LLM
from tools import tool
import litellm
from dotenv import load_dotenv
load_dotenv()
from langchain_google_genai import ChatGoogleGenerativeAI
import os

## call the gemini models
# llm=ChatGoogleGenerativeAI(model="gemini-1.5-flash",
#                            verbose=True,
#                            temperature=0.5,
#                            google_api_key=os.getenv("GEMINI_API_KEY"))

os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")
api_key = "AIzaSyA_jVLib-F27Fe6GvPqdHH5VQZ1eRJUJbY"
litellm.api_key = api_key
GEMINI_API_KEY = api_key 

llm = LLM(
    # model="gemini/gemini-1.5-pro-latest",
    model="gemini/gemini-2.0-flash",
    temperature=0.7,
    google_api_key=api_key
)

# Creating a senior researcher agent with memory and verbose mode

news_researcher=Agent(
    role="Senior Researcher",
    goal='Unccover ground breaking technologies in {topic}',
    verbose=True,
    memory=True,
    backstory=(
        "Driven by curiosity, you're at the forefront of"
        "innovation, eager to explore and share knowledge that could change"
        "the world."

    ),
    tools=[tool],
    llm=llm,
    allow_delegation=True

)

## creating a write agent with custom tools responsible in writing news blog

news_writer = Agent(
  role='Writer',
  goal='Narrate compelling tech stories about {topic}',
  verbose=True,
  memory=True,
  backstory=(
    "With a flair for simplifying complex topics, you craft"
    "engaging narratives that captivate and educate, bringing new"
    "discoveries to light in an accessible manner."
  ),
  tools=[tool],
  llm=llm,
  allow_delegation=False
)

