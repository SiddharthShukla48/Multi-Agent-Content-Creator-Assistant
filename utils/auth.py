"""
Authentication module for Content Creator Assistant
Simple file-based authentication system
"""

import streamlit as st
import hashlib
import json
from pathlib import Path
from typing import Optional, Dict
from datetime import datetime


class SimpleAuth:
    """Simple file-based authentication system"""
    
    def __init__(self, users_file: str = "users.json"):
        self.users_file = Path(users_file)
        self._ensure_users_file()
    
    def _ensure_users_file(self):
        """Create users file if it doesn't exist"""
        if not self.users_file.exists():
            with open(self.users_file, 'w') as f:
                json.dump({}, f)
    
    def _hash_password(self, password: str) -> str:
        """Hash password using SHA256"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def _load_users(self) -> Dict:
        """Load users from file"""
        try:
            with open(self.users_file, 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}
    
    def _save_users(self, users: Dict):
        """Save users to file"""
        with open(self.users_file, 'w') as f:
            json.dump(users, f, indent=2)
    
    def register_user(self, username: str, password: str, email: str) -> tuple[bool, str]:
        """Register a new user"""
        users = self._load_users()
        
        if username in users:
            return False, "Username already exists"
        
        # Check if email already exists
        for user_data in users.values():
            if user_data.get("email") == email:
                return False, "Email already registered"
        
        users[username] = {
            "password": self._hash_password(password),
            "email": email,
            "created_at": datetime.now().isoformat(),
            "last_login": None
        }
        
        self._save_users(users)
        return True, "Registration successful"
    
    def authenticate(self, username: str, password: str) -> bool:
        """Authenticate user"""
        users = self._load_users()
        
        if username not in users:
            return False
        
        if users[username]["password"] == self._hash_password(password):
            # Update last login
            users[username]["last_login"] = datetime.now().isoformat()
            self._save_users(users)
            return True
        
        return False
    
    def get_user_info(self, username: str) -> Optional[Dict]:
        """Get user information"""
        users = self._load_users()
        return users.get(username)


def check_authentication():
    """Check if user is authenticated"""
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
    
    if "username" not in st.session_state:
        st.session_state.username = None
    
    return st.session_state.authenticated


def login_page():
    """Display login/registration page"""
    st.markdown(
        """
        <style>
        .main-header {
            text-align: center;
            padding: 2rem 0;
        }
        .auth-container {
            max-width: 500px;
            margin: 0 auto;
            padding: 2rem;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    
    st.markdown('<div class="main-header">', unsafe_allow_html=True)
    st.title("🎬 Content Creator Assistant")
    st.write("AI-Powered Multi-Agent Content Creation System")
    st.markdown('</div>', unsafe_allow_html=True)
    
    auth = SimpleAuth()
    
    tab1, tab2 = st.tabs(["🔐 Login", "📝 Register"])
    
    with tab1:
        st.subheader("Login to Your Account")
        with st.form("login_form"):
            username = st.text_input("Username", placeholder="Enter your username")
            password = st.text_input("Password", type="password", placeholder="Enter your password")
            submit = st.form_submit_button("Login", use_container_width=True)
            
            if submit:
                if not username or not password:
                    st.error("Please fill in all fields")
                elif auth.authenticate(username, password):
                    st.session_state.authenticated = True
                    st.session_state.username = username
                    st.success(f"Welcome back, {username}!")
                    st.rerun()
                else:
                    st.error("Invalid username or password")
    
    with tab2:
        st.subheader("Create New Account")
        with st.form("register_form"):
            new_username = st.text_input("Choose Username", placeholder="Choose a unique username")
            new_email = st.text_input("Email", placeholder="your.email@example.com")
            new_password = st.text_input("Choose Password", type="password", placeholder="At least 6 characters")
            confirm_password = st.text_input("Confirm Password", type="password", placeholder="Re-enter your password")
            register = st.form_submit_button("Register", use_container_width=True)
            
            if register:
                if not new_username or not new_password or not new_email:
                    st.error("All fields are required")
                elif len(new_username) < 3:
                    st.error("Username must be at least 3 characters")
                elif new_password != confirm_password:
                    st.error("Passwords don't match")
                elif len(new_password) < 6:
                    st.error("Password must be at least 6 characters")
                elif "@" not in new_email or "." not in new_email:
                    st.error("Please enter a valid email address")
                else:
                    success, message = auth.register_user(new_username, new_password, new_email)
                    if success:
                        st.success(message + " Please login.")
                    else:
                        st.error(message)
    
    # Footer
    st.divider()
    st.markdown(
        """
        <div style='text-align: center; color: #666; font-size: 0.9rem;'>
        <p>🔒 Your data is securely stored and encrypted</p>
        <p>Built with CrewAI, Groq, and Streamlit</p>
        </div>
        """,
        unsafe_allow_html=True
    )


def logout():
    """Logout current user and clear all session data"""
    # Clear authentication
    st.session_state.authenticated = False
    st.session_state.username = None
    
    # Clear session data
    st.session_state.session_id = None
    st.session_state.step = 1
    st.session_state.data = {}
    
    # Clear all flags
    for flag in ["topic_research_in_progress", "content_research_in_progress", 
                 "script_generation_in_progress", "media_generation_in_progress"]:
        if flag in st.session_state:
            st.session_state[flag] = False
    
    st.rerun()
