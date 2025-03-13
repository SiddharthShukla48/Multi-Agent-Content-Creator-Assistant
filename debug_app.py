# debug_app.py
import streamlit as st
import os
import uuid
from utils.helpers import load_session_data, save_session_data

# Initialize session state
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())
if "step" not in st.session_state:
    st.session_state.step = 1
if "data" not in st.session_state:
    st.session_state.data = {}

# Load existing data
session_data = load_session_data(st.session_state.session_id)
if session_data:
    st.session_state.data = session_data

# Display state info
st.header("Session State Debug")
st.write(f"Current step: {st.session_state.step}")
st.write(f"Session ID: {st.session_state.session_id}")
st.write("Data keys:", list(st.session_state.data.keys()))

# Manually set step
col1, col2, col3, col4, col5 = st.columns(5)
if col1.button("Set Step 1"): 
    st.session_state.step = 1
    save_session_data(st.session_state.session_id, {"step": 1})
    st.rerun()
if col2.button("Set Step 2"): 
    st.session_state.step = 2
    save_session_data(st.session_state.session_id, {"step": 2})
    st.rerun()
if col3.button("Set Step 3"): 
    st.session_state.step = 3
    save_session_data(st.session_state.session_id, {"step": 3})
    st.rerun()
if col4.button("Set Step 4"): 
    st.session_state.step = 4
    save_session_data(st.session_state.session_id, {"step": 4})
    st.rerun()
if col5.button("Set Step 5"): 
    st.session_state.step = 5
    save_session_data(st.session_state.session_id, {"step": 5})
    st.rerun()

if st.button("Reset All Data"):
    st.session_state.step = 1
    st.session_state.data = {}
    save_session_data(st.session_state.session_id, {"step": 1})
    st.rerun()