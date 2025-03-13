from crewai import Task

def research_topic_task(agent, content_niche):
    return Task(
        description=f"""Research and identify 3-5 trending and engaging topics in the {content_niche} niche.
        For each topic:
        1. Provide a concise title
        2. Explain why this topic would engage the target audience
        3. Include approximate audience size or interest level
        4. Outline potential talking points
        
        The topics should be specific enough to create focused content but broad enough to appeal to a sizable audience.
        """,
        agent=agent,
        expected_output="A list of 3-5 potential topics with detailed rationale for each"
    )

def retrieve_data_task(agent, selected_topic):
    return Task(
        description=f"""Research and collect comprehensive information about "{selected_topic}".
        Your research should include:
        1. Key facts and statistics from reliable sources
        2. Different perspectives on the topic
        3. Recent developments or news
        4. Expert opinions
        5. Interesting examples or case studies
        
        Organize the information in a structured format and cite all sources.
        """,
        agent=agent,
        expected_output="A detailed research document with organized information and cited sources"
    )

def write_script_task(agent, selected_topic, research_data):
    # Fix: Pass raw research data as string directly
    return Task(
        description=f"""Write an engaging script for a video on "{selected_topic}" using the provided research.
        The script should include:
        1. A hook to grab viewer attention in the first 10 seconds
        2. A clear introduction explaining what will be covered
        3. A well-structured main content section with logical flow
        4. Clear transitions between sections
        5. A compelling conclusion with a call to action
        
        Use conversational language appropriate for video content and incorporate key points from the research.
        
        Research: {research_data if isinstance(research_data, str) else 
                 research_data.get('content', 'No research available')}
        """,
        agent=agent,
        expected_output="A complete, ready-to-use video script with clearly marked sections"
    )

def create_media_assets_task(agent, selected_topic, script):
    return Task(
        description=f"""Create compelling title options and thumbnail concepts for a video about "{selected_topic}".
        Based on the script provided, generate:
        1. 5 attention-grabbing title options that would perform well on YouTube (consider using numbers, questions, or emotional triggers)
        2. 3 thumbnail concepts with detailed descriptions including:
           - Main visual elements
           - Text overlay suggestions
           - Color scheme
           - Emotional tone
        
        Ensure titles and thumbnails accurately represent the content while maximizing viewer interest.
        
        Script: {script}
        """,
        agent=agent,
        expected_output="A list of title options and detailed thumbnail concepts"
    )