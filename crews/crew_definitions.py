from crewai import Crew
import time

from agents.agent_definitions import (
    get_topic_research_agent,
    get_data_retrieval_agent,
    get_script_writing_agent,
    get_media_enhancement_agent
)
from tasks.task_definitions import (
    research_topic_task,
    retrieve_data_task,
    write_script_task,
    create_media_assets_task
)

def get_content_creation_crew(content_niche=None, selected_topic=None, research_data=None, script=None):
    # Initialize agents
    topic_research_agent = get_topic_research_agent()
    data_retrieval_agent = get_data_retrieval_agent()
    script_writing_agent = get_script_writing_agent()
    media_enhancement_agent = get_media_enhancement_agent()
    
    # Create tasks list based on available information
    tasks = []
    
    if content_niche and not selected_topic:
        tasks.append(research_topic_task(topic_research_agent, content_niche))
    
    if selected_topic and not research_data:
        tasks.append(retrieve_data_task(data_retrieval_agent, selected_topic))
    
    if selected_topic and research_data and not script:
        tasks.append(write_script_task(script_writing_agent, selected_topic, research_data))
    
    if selected_topic and script:
        tasks.append(create_media_assets_task(media_enhancement_agent, selected_topic, script))
    
    time.sleep(15) 
    # Create and return the crew
    return Crew(
        agents=[
            topic_research_agent,
            data_retrieval_agent,
            script_writing_agent,
            media_enhancement_agent
        ],
        tasks=tasks,
        verbose=True
    )