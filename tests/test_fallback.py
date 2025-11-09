"""
Test Fallback Mechanism
Quick test script to verify mock AI fallback works
"""

import streamlit as st
import sys
sys.path.insert(0, '/Users/ketankeshav/Documents/GitHub/BuddyBlocks')

from utils.snowflake_client import get_snowflake_client


def main():
    st.set_page_config(
        page_title="Fallback Test",
        page_icon="🔄",
        layout="wide"
    )
    
    st.title("🔄 Fallback Mechanism Test")
    st.caption("Testing graceful fallback to Mock AI")
    
    st.divider()
    
    # Get client (will show connection status)
    client = get_snowflake_client()
    
    # Display AI source
    st.info(f"**Current AI Source:** {client.get_ai_source()}")
    
    st.divider()
    
    # Test 1: Journal Parsing
    st.header("Test 1: Journal Parsing")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        journal_text = st.text_area(
            "Enter journal text:",
            value="I need to prepare presentation slides and practice my demo. Also review feedback from team.",
            height=100
        )
    
    with col2:
        st.write("")
        st.write("")
        if st.button("🔍 Parse Journal", type="primary", use_container_width=True):
            try:
                with st.spinner("Parsing journal..."):
                    tasks = client.parse_journal(journal_text)
                    
                    st.success(f"✅ Parsed {len(tasks)} tasks")
                    
                    for i, task in enumerate(tasks, 1):
                        with st.expander(f"Task {i}: {task['title']}", expanded=True):
                            st.write(f"**Description:** {task['description']}")
                            st.write(f"**Duration:** {task['estimated_duration']} minutes")
                            st.write(f"**Subtasks:**")
                            for subtask in task.get('subtasks', []):
                                st.write(f"  • {subtask}")
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
    
    st.divider()
    
    # Test 2: Coach Messages
    st.header("Test 2: Coach Messages")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("🚀 Session Start", use_container_width=True):
            try:
                msg = client.get_coach_message('session_start', {
                    'task': 'Write Report',
                    'duration': 60
                })
                st.info(f"🎙️ {msg}")
            except Exception as e:
                st.error(f"❌ {str(e)}")
    
    with col2:
        if st.button("⏱️ Halfway", use_container_width=True):
            try:
                msg = client.get_coach_message('halfway', {
                    'task': 'Write Report',
                    'duration': 60
                })
                st.info(f"🎙️ {msg}")
            except Exception as e:
                st.error(f"❌ {str(e)}")
    
    with col3:
        if st.button("☕ Break", use_container_width=True):
            try:
                msg = client.get_coach_message('break', {
                    'task': 'Write Report',
                    'duration': 60
                })
                st.info(f"🎙️ {msg}")
            except Exception as e:
                st.error(f"❌ {str(e)}")
    
    with col4:
        if st.button("🎉 Completion", use_container_width=True):
            try:
                msg = client.get_coach_message('completion', {
                    'task': 'Write Report',
                    'duration': 60
                })
                st.info(f"🎙️ {msg}")
            except Exception as e:
                st.error(f"❌ {str(e)}")
    
    st.divider()
    
    # Connection Status
    st.header("Connection Status")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric("Connected to Snowflake", "Yes" if client.is_connected else "No")
    
    with col2:
        st.metric("AI Source", client.get_ai_source())
    
    st.divider()
    
    # Summary
    if client.is_connected:
        st.success("✅ **Using Snowflake Cortex AI** - All features available!")
    else:
        st.info("""
        ℹ️ **Using Mock AI (Demo Mode)**
        
        **What works:**
        - ✅ Journal parsing (with mock AI)
        - ✅ Coach messages (with mock AI)
        
        **What requires Snowflake:**
        - ⚠️ Database operations (saving/loading tasks)
        - ⚠️ Session statistics
        """)


if __name__ == "__main__":
    main()
