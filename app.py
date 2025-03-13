# This must be the first code that runs
import os
# Configure environment before any imports
os.environ["LANGCHAIN_TRACING_V2"] = "false"
os.environ["CHROMA_DB_IMPL"] = "duckdb+parquet"
os.environ["CHROMADB_CLIENT_SETTINGS_PERSIST_DIRECTORY"] = ""

# Continue with standard imports
# import sys
# __import__('pysqlite3')
# sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

import streamlit as st
import uuid
import time
import logging
import json
import os
from crews.crew_definitions import get_content_creation_crew
from utils.helpers import save_session_data, load_session_data, parse_topic_results

# ... rest of your code remains unchanged

# Configure logging with more detail
logging.basicConfig(
    level=logging.DEBUG,  # Change to DEBUG for more detailed logs
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("app_debug.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Add this debug helper
def debug_state():
    """Log current session state for debugging"""
    logger.debug(f"SESSION STATE: step={st.session_state.get('step', 'Not set')}")
    logger.debug(f"SESSION STATE: data keys={list(st.session_state.data.keys())}")
    logger.debug(f"SESSION STATE: flags={[f for f in st.session_state.keys() if f.endswith('_in_progress')]}")

# Initialize session state variables
def initialize_session_state():
    if "session_id" not in st.session_state:
        st.session_state.session_id = str(uuid.uuid4())
    if "step" not in st.session_state:
        st.session_state.step = 1
    if "data" not in st.session_state:
        st.session_state.data = {}
    
    # Action flags
    for flag in ["topic_research_in_progress", "content_research_in_progress", 
                 "script_generation_in_progress", "media_generation_in_progress"]:
        if flag not in st.session_state:
            st.session_state[flag] = False

# Load previous session data
def load_previous_session():
    session_data = load_session_data(st.session_state.session_id)
    if session_data:
        # If we have session data
        if "step" in session_data:
            # Make sure step is loaded directly into session state
            st.session_state.step = session_data["step"]
            # Log that we've loaded the step
            logger.info(f"Loaded step {st.session_state.step} from session data")
        
        # Update the rest of the data
        if not isinstance(st.session_state.data, dict):
            st.session_state.data = {}
        
        # Copy all data except step
        for key, value in session_data.items():
            if key != "step":  # We've already handled step
                st.session_state.data[key] = value

# Display the sidebar navigation
def display_sidebar():
    st.sidebar.header("Progress")
    st.sidebar.progress(st.session_state.step / 5)
    st.sidebar.write(f"Step {st.session_state.step} of 5")
    
    st.sidebar.header("Navigation")
    step_names = {
        1: "Topic Research",
        2: "Topic Selection",
        3: "Script Generation",
        4: "Script Review & Media Assets",
        5: "Final Results"
    }
    
    for step, name in step_names.items():
        if st.sidebar.button(name, disabled=step > st.session_state.step):
            if step <= st.session_state.step:
                st.session_state.step = step
                st.rerun()

# Step 1: Research topics based on content niche
def step_topic_research():
    st.header("Step 1: Topic Research")
    
    with st.form("niche_form"):
        content_niche = st.text_input("What's your content niche? (e.g., Tech Reviews, Cooking, Personal Finance)", 
                                      help="Be specific but not too narrow")
        topic_research_submitted = st.form_submit_button("Research Topics")
    
    if topic_research_submitted and content_niche:
        st.session_state.topic_research_in_progress = True
        st.rerun()

    if st.session_state.topic_research_in_progress:
        try:
            with st.spinner("Researching trending topics in your niche..."):
                # Create and run crew for topic research
                crew = get_content_creation_crew(content_niche=content_niche)
                result = crew.kickoff()
                
                # Parse and store results
                topics = parse_topic_results(result)
                
                # Update session state
                st.session_state.data.update({
                    "content_niche": content_niche,
                    "topic_research_result": str(result),
                    "topics": topics
                })
                
                st.session_state.step = 2
                st.session_state.topic_research_in_progress = False
                
                # Save session data
                save_session_data(st.session_state.session_id, {
                    "step": st.session_state.step,
                    "content_niche": content_niche,
                    "topic_research_result": str(result),
                    "topics": topics
                })
                
                st.success("Topics researched successfully!")
                st.rerun()
        except Exception as e:
            st.error(f"Error during topic research: {str(e)}")
            logger.error(f"Topic research error: {str(e)}", exc_info=True)
            st.session_state.topic_research_in_progress = False

# Step 2: Select a topic and research it
def step_topic_selection():
    st.header("Step 2: Select a Topic")
    
    # Display topic options
    if "topics" in st.session_state.data:
        topics = st.session_state.data["topics"]
        
        # If parsing failed, just show the raw output
        if not topics or (len(topics) == 1 and topics[0].get("title", "").startswith("Raw output")):
            st.text_area("Research Results", st.session_state.data["topic_research_result"], height=300)
            selected_topic = st.text_input("Enter your chosen topic based on the research above:")
        else:
            # Display parsed topics
            for i, topic in enumerate(topics):
                with st.expander(f"Topic {i+1}: {topic.get('title', 'Unnamed Topic')}"):
                    st.write(f"**Rationale:** {topic.get('rationale', 'Not provided')}")
                    st.write(f"**Audience:** {topic.get('audience', 'Not provided')}")
                    st.write(f"**Talking Points:** {topic.get('talking_points', 'Not provided')}")
            
            # Let the user select a topic or enter a custom one
            topic_options = [topic.get("title", f"Topic {i+1}") for i, topic in enumerate(topics)]
            topic_options.append("Enter my own topic")
            
            selected_option = st.selectbox("Select a topic:", topic_options)
            
            if selected_option == "Enter my own topic":
                selected_topic = st.text_input("Enter your custom topic:")
            else:
                selected_topic = selected_option
    
    else:
        st.error("No topic research results found. Please go back to Step 1.")
        if st.button("Back to Step 1"):
            st.session_state.step = 1
            st.rerun()
        return
    
    # Research button
    if st.button("Research this Topic") and selected_topic:
        st.session_state.content_research_in_progress = True
        st.session_state.selected_topic = selected_topic
        st.rerun()

    # Handle research process
    if st.session_state.content_research_in_progress:
        try:
            with st.spinner("Gathering comprehensive research on your topic..."):
                # Create and run crew for data retrieval
                crew = get_content_creation_crew(selected_topic=st.session_state.selected_topic)
                time.sleep(2)  # Small delay to avoid rate limits
                result = crew.kickoff()
                
                # Store results in session state FIRST
                st.session_state.data["selected_topic"] = st.session_state.selected_topic
                st.session_state.data["research_data"] = str(result)
                
                # Set the step directly in session state
                st.session_state.step = 3
                st.session_state.content_research_in_progress = False
                
                # Save session data AFTER updating session state
                save_session_data(st.session_state.session_id, st.session_state.data)
                
                # Show success message
                st.success("Research complete! Moving to script generation...")
                st.rerun()
                
        except Exception as e:
            st.error(f"Error during research: {str(e)}")
            logger.error(f"Research error: {str(e)}", exc_info=True)
            st.session_state.content_research_in_progress = False

# Step 3: Generate script based on research
def step_script_generation():
    st.header("Step 3: Script Generation")
    
    # Display research data
    if "research_data" in st.session_state.data:
        with st.expander("Research Data", expanded=False):
            st.markdown(st.session_state.data["research_data"])
    
    # Check if script has already been generated
    if "script" in st.session_state.data:
        st.success("Script has been generated!")
        with st.expander("Generated Script", expanded=True):
            st.write(st.session_state.data["script"])
            
        # Simple direct navigation button
        if st.button("Continue to Script Review"):
            st.session_state.step = 4
            save_session_data(st.session_state.session_id, {"step": 4})
            st.rerun()
    else:
        # Simple direct button for script generation
        st.write(f"Generate a script for: **{st.session_state.data.get('selected_topic', 'Unknown Topic')}**")
        
        # Simplified approach - direct button without columns
        if st.button("Generate Script", key="direct_generate"):
            st.session_state.script_generation_in_progress = True
            st.rerun()
        
        if st.session_state.script_generation_in_progress:
            try:
                # Fetch required data
                selected_topic = st.session_state.data["selected_topic"]
                research_data = st.session_state.data["research_data"]
                
                # Just pass the string directly - we've updated task_definitions.py to handle this
                crew = get_content_creation_crew(
                    selected_topic=selected_topic,
                    research_data=research_data  # Pass string directly
                )
                
                # Show progress
                with st.spinner("Writing your script based on the research..."):
                    result = crew.kickoff()
                
                # Store result immediately
                st.session_state.data["script"] = str(result)
                st.session_state.step = 4
                st.session_state.script_generation_in_progress = False
                
                # Save data
                save_session_data(st.session_state.session_id, {
                    "step": 4,
                    "script": str(result),
                    **st.session_state.data
                })
                
                # Success message and forced navigation
                st.success("✓ Script generated successfully!")
                st.rerun()
                
            except Exception as e:
                st.error(f"Error generating script: {str(e)}")
                logger.error(f"Script generation error: {str(e)}", exc_info=True)
                st.session_state.script_generation_in_progress = False

# Step 4: Review script and generate media assets
def step_script_review():
    st.header("Step 4: Script Review & Media Assets")
    
    # Display and allow editing of the script
    if "script" in st.session_state.data:
        st.subheader("Your Script")
        edited_script = st.text_area("Review and edit your script:", 
                                   st.session_state.data["script"], 
                                   height=300)
        st.session_state.data["edited_script"] = edited_script
        
        save_button = st.button("Save Edits")
        if save_button:
            save_session_data(st.session_state.session_id, {
                "edited_script": edited_script,
                **st.session_state.data
            })
            st.success("Script edits saved!")
    
    # Generate media assets
    if st.button("Generate Titles & Thumbnail Concepts"):
        st.session_state.media_generation_in_progress = True
        st.rerun()
        
    if st.session_state.media_generation_in_progress:
        try:
            with st.spinner("Creating titles and thumbnail concepts..."):
                selected_topic = st.session_state.data["selected_topic"]
                script = st.session_state.data.get("edited_script", st.session_state.data["script"])
                
                # Create and run crew for media assets
                crew = get_content_creation_crew(
                    selected_topic=selected_topic,
                    script=script
                )
                time.sleep(2)  # Small delay to avoid rate limits
                result = crew.kickoff()
                
                # Store results
                st.session_state.data["media_assets"] = str(result)
                st.session_state.step = 5
                st.session_state.media_generation_in_progress = False
                
                save_session_data(st.session_state.session_id, {
                    "step": 5,
                    "media_assets": str(result),
                    **st.session_state.data
                })
                
                st.success("Media assets generated successfully!")
                st.rerun()
        except Exception as e:
            st.error(f"Error generating media assets: {str(e)}")
            logger.error(f"Media assets generation error: {str(e)}", exc_info=True)
            st.session_state.media_generation_in_progress = False

# Step 5: Display final results
def step_final_results():
    st.header("Your Content Package")
    
    # Display all generated content
    st.subheader("📝 Script")
    script = st.session_state.data.get("edited_script", st.session_state.data["script"])
    st.markdown(script)
    
    st.subheader("🏷️ Title Options & Thumbnail Concepts")
    if "media_assets" in st.session_state.data:
        st.markdown(st.session_state.data["media_assets"])
    
    # Download buttons
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.download_button(
            label="Download Script",
            data=script,
            file_name="content_script.txt",
            mime="text/plain"
        )
    
    with col2:
        if "media_assets" in st.session_state.data:
            st.download_button(
                label="Download Media Assets",
                data=st.session_state.data["media_assets"],
                file_name="media_assets.txt",
                mime="text/plain"
            )
    
    with col3:
        if "research_data" in st.session_state.data:
            st.download_button(
                label="Download Research",
                data=st.session_state.data["research_data"],
                file_name="research_data.txt",
                mime="text/plain"
            )
    
    # Start over button
    if st.button("Start a New Project"):
        st.session_state.step = 1
        st.session_state.data = {}
        for flag in ["topic_research_in_progress", "content_research_in_progress", 
                     "script_generation_in_progress", "media_generation_in_progress"]:
            st.session_state[flag] = False
        st.rerun()

# Main function
def main():
    # Set page config
    st.set_page_config(
        page_title="Content Creator Assistant",
        page_icon="🎬",
        layout="wide"
    )
    
    # Initialize and load session
    initialize_session_state()
    load_previous_session()
    
    # App title
    st.title("🎬 Content Creator Assistant")
    st.write("A multi-agent system to help content creators automate their workflow")
    
    # Display sidebar
    display_sidebar()
    
    # Handle current step
    if st.session_state.step == 1:
        step_topic_research()
    elif st.session_state.step == 2:
        step_topic_selection()
    elif st.session_state.step == 3:
        step_script_generation()
    elif st.session_state.step == 4:
        step_script_review()
    elif st.session_state.step == 5:
        step_final_results()
    
    # Debug info
    logger.info(f"Current step at end of main: {st.session_state.step}")

if __name__ == "__main__":
    main()