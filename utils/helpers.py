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
        output_str = str(output)
        
        # Try to parse as JSON first
        import re
        # Look for JSON array in the output
        json_match = re.search(r'\[[\s\S]*\]', output_str)
        if json_match:
            try:
                topics_data = json.loads(json_match.group(0))
                if isinstance(topics_data, list) and len(topics_data) > 0:
                    # Convert JSON format to our format
                    topics = []
                    for topic in topics_data:
                        parsed_topic = {
                            'title': topic.get('title', 'Untitled'),
                            'rationale': topic.get('engagement_reason', topic.get('rationale', 'Not provided')),
                            'audience': topic.get('audience_size', topic.get('audience', 'Not provided')),
                            'talking_points': ', '.join(topic.get('talking_points', [])) if isinstance(topic.get('talking_points'), list) else topic.get('talking_points', 'Not provided')
                        }
                        topics.append(parsed_topic)
                    return topics
            except json.JSONDecodeError:
                pass
        
        # Fallback to line-by-line parsing
        topics = []
        current_topic = {}
        
        for line in output_str.split('\n'):
            line = line.strip()
            if line.startswith("Topic") or line.startswith("title"):
                if current_topic and 'title' in current_topic:
                    topics.append(current_topic)
                current_topic = {'title': line.split(':', 1)[1].strip() if ':' in line else line}
            elif "why" in line.lower() or "engagement" in line.lower() and current_topic:
                current_topic['rationale'] = line.split(':', 1)[1].strip() if ':' in line else line
            elif "audience" in line.lower() and current_topic:
                current_topic['audience'] = line.split(':', 1)[1].strip() if ':' in line else line
            elif "talking points" in line.lower() and current_topic:
                current_topic['talking_points'] = line.split(':', 1)[1].strip() if ':' in line else line
        
        if current_topic and 'title' in current_topic:
            topics.append(current_topic)
        
        # If we got topics, return them
        if topics:
            return topics
            
        # Otherwise return None to trigger fallback display
        return None
        
    except Exception as e:
        # If parsing fails completely, return None to show raw output
        return None

# Generate PDF from script content
def create_script_pdf(script_content, topic_title="Content Script"):
    """Generate a PDF file from the script content"""
    from fpdf import FPDF
    from datetime import datetime
    
    # Create PDF object with proper configuration
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_left_margin(15)
    pdf.set_right_margin(15)
    
    # Add title
    pdf.set_font("Arial", "B", 24)
    pdf.cell(0, 15, "Content Script", ln=True, align="C")
    pdf.ln(5)
    
    # Add topic title
    pdf.set_font("Arial", "B", 14)
    # Clean the topic title to avoid encoding issues
    clean_topic = topic_title.encode('latin-1', 'replace').decode('latin-1')
    pdf.multi_cell(0, 10, clean_topic)
    pdf.ln(5)
    
    # Add date
    pdf.set_font("Arial", "I", 10)
    pdf.cell(0, 10, f"Generated on: {datetime.now().strftime('%B %d, %Y')}", ln=True)
    pdf.ln(10)
    
    # Add content
    pdf.set_font("Arial", "", 11)
    
    # Process content line by line to handle special formatting
    lines = script_content.split('\n')
    for line in lines:
        # Clean line to handle encoding issues
        try:
            clean_line = line.encode('latin-1', 'replace').decode('latin-1')
        except:
            clean_line = line.encode('ascii', 'ignore').decode('ascii')
        
        # Skip empty lines
        if not clean_line.strip():
            pdf.ln(4)
            continue
            
        # Handle headers (lines starting with #)
        if clean_line.strip().startswith('#'):
            # Remove # symbols and make bold
            header_text = clean_line.strip().lstrip('#').strip()
            if header_text:  # Only render if there's actual text
                pdf.set_font("Arial", "B", 13)
                try:
                    pdf.multi_cell(0, 7, header_text)
                except:
                    # Fallback if rendering fails
                    pdf.cell(0, 7, header_text[:100], ln=True)
                pdf.ln(3)
                pdf.set_font("Arial", "", 11)
        # Handle bold text (**text**)
        elif '**' in clean_line:
            # Remove ** markers
            plain_text = clean_line.replace('**', '')
            if plain_text.strip():
                try:
                    pdf.multi_cell(0, 6, plain_text)
                except:
                    pdf.cell(0, 6, plain_text[:150], ln=True)
        # Regular text
        else:
            if clean_line.strip():
                try:
                    pdf.multi_cell(0, 6, clean_line)
                except:
                    # Fallback: truncate very long lines
                    pdf.cell(0, 6, clean_line[:150], ln=True)
    
    # Return PDF as bytes (output already returns bytearray/bytes)
    return bytes(pdf.output())
    
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