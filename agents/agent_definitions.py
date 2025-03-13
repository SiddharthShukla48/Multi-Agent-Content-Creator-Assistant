from crewai import Agent
from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os

load_dotenv()

# Initialize the Groq language model
def get_llm(model="llama-3.3-70b-versatile"):
    # Update this to explicitly specify the provider is Groq
    return ChatGroq(
        api_key=os.getenv("GROQ_API_KEY"),
        model_name=f"groq/{model}"  # Explicitly prefix with "groq/"
    )

# For vision tasks
def get_vision_llm():
    return ChatGroq(
        api_key=os.getenv("GROQ_API_KEY"),
        model="groq/llama-3.2-90b-vision-preview"  # Adjust to an appropriate Groq vision model
    )

# Define agents
def get_topic_research_agent():
    return Agent(
        role="Topic Research Specialist",
        goal="Identify trending and engaging topics in the creator's niche",
        backstory="""You are an expert in content trends and audience engagement.
        You have a deep understanding of what topics resonate with different audience 
        segments and can predict which content ideas will perform well.""",
        verbose=True,
        allow_delegation=True,
        llm=get_llm()
    )

def get_data_retrieval_agent():
    return Agent(
        role="Data Research Specialist",
        goal="Find comprehensive and accurate information on the selected topic",
        backstory="""You are a master researcher with the ability to find, evaluate, 
        and synthesize information from various sources. You have a keen eye for 
        credible sources and can quickly distinguish valuable data from noise.""",
        verbose=True,
        allow_delegation=False,
        llm=get_llm()
    )

def get_script_writing_agent():
    return Agent(
        role="Script Writing Expert",
        goal="Create engaging, well-structured scripts for video content",
        backstory="""You are a talented scriptwriter who specializes in creating 
        compelling narratives for video content. You know how to craft introductions 
        that hook viewers, develop informative main sections, and close with impactful 
        conclusions.""",
        verbose=True,
        allow_delegation=False,
        llm=get_llm()
    )

def get_media_enhancement_agent():
    return Agent(
        role="Media Optimization Specialist",
        goal="Create attention-grabbing titles and thumbnail concepts",
        backstory="""You are an expert in digital media optimization who understands 
        what makes viewers click. You can craft compelling headlines and visualize 
        thumbnails that increase click-through rates while maintaining content integrity.""",
        verbose=True,
        allow_delegation=False,
        llm=get_llm()
    )