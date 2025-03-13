import os
import json
import random
from pathlib import Path
import streamlit as st

# Create directory for storing session data
def ensure_data_directory():
    data_dir = Path("session_data")
    data_dir.mkdir(exist_ok=True)
    return data_dir

# Custom JSON encoder to handle CrewOutput objects
class CustomEncoder(json.JSONEncoder):
    def default(self, obj):
        try:
            return super().default(obj)
        except TypeError:
            return str(obj)  # Convert any non-serializable objects to strings

# Save data between session steps
def save_session_data(session_id, data_dict):
    data_dir = ensure_data_directory()
    with open(data_dir / f"{session_id}.json", "w") as f:
        json.dump(data_dict, f, cls=CustomEncoder)  # Use the custom encoder

# Load data from previous session steps
def load_session_data(session_id):
    data_dir = ensure_data_directory()
    try:
        with open(data_dir / f"{session_id}.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

# Parse agent output for display
def parse_topic_results(output):
    """Parse the topic research results into a structured format"""
    try:
        # This is a simple example - in reality you'd want more robust parsing
        topics = []
        current_topic = {}
        
        for line in output.split('\n'):
            line = line.strip()
            if line.startswith("Topic"):
                if current_topic and 'title' in current_topic:
                    topics.append(current_topic)
                current_topic = {'title': line.split(':', 1)[1].strip() if ':' in line else line}
            elif "why" in line.lower() and current_topic:
                current_topic['rationale'] = line.split(':', 1)[1].strip() if ':' in line else line
            elif "audience" in line.lower() and current_topic:
                current_topic['audience'] = line.split(':', 1)[1].strip() if ':' in line else line
            elif "talking points" in line.lower() and current_topic:
                current_topic['talking_points'] = line.split(':', 1)[1].strip() if ':' in line else line
        
        if current_topic and 'title' in current_topic:
            topics.append(current_topic)
            
        return topics
    except Exception:
        # If parsing fails, return the raw output
        return [{"title": "Raw output", "rationale": output}]
    
    # filepath: /Users/siddharthshukla/Library/CloudStorage/OneDrive-ManipalUniversityJaipur/Kaam Dhandha/Internship/Varnan Labs/MAS/crewai-groq-project/utils/helpers.py
import time
from functools import wraps

def retry_with_exponential_backoff(max_retries=5, initial_delay=1):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            delay = initial_delay
            for i in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                     if "rate_limit_exceeded" in str(e):
                        if i == max_retries - 1:
                            raise
                        sleep_time = delay * (2 ** i) + random.uniform(0, 1)
                        st.warning(f"Rate limit reached. Retrying in {sleep_time:.2f} seconds...")
                        time.sleep(sleep_time)
                     else:
                        raise
        return wrapper
    return decorator