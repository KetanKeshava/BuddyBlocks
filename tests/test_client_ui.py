"""
Streamlit UI Test for SnowflakeClient
Interactive testing of all client methods
"""

import streamlit as st
import uuid
import sys
from pathlib import Path
from datetime import datetime

# Add parent directory to path to import utils
parent_dir = Path(__file__).parent.parent
sys.path.insert(0, str(parent_dir))

from utils.snowflake_client import get_snowflake_client


def main():
    """Main test application"""
    
    # Set page configuration
    st.set_page_config(
        page_title="Test Snowflake Client",
        page_icon="🧪",
        layout="wide"
    )
    
    # App header
    st.title("🧪 Snowflake Client Test Suite")
    st.markdown("Interactive testing of all SnowflakeClient methods with real Snowflake Cortex AI")
    
    st.divider()
    
    # Get the Snowflake client
    with st.spinner("Initializing Snowflake connection..."):
        client = get_snowflake_client()
    
    # Display connection status
    if client and client.is_connected:
        st.success("✅ Connected to Snowflake Cortex!", icon="✅")
        
        # Display connection info
        with st.expander("🔍 Connection Details"):
            try:
                credentials = st.secrets["snowflake"]
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Account", credentials['account'])
                    st.metric("Warehouse", credentials['warehouse'])
                with col2:
                    st.metric("Database", credentials['database'])
                    st.metric("Schema", credentials['schema'])
                with col3:
                    st.metric("Role", credentials['role'])
            except Exception as e:
                st.error(f"Error displaying connection details: {str(e)}")
    else:
        st.error("❌ Not connected to Snowflake", icon="❌")
        st.info("💡 Please check your credentials in .streamlit/secrets.toml")
        st.stop()
    
    st.divider()
    
    # ========================================
    # TEST 1: Journal Parsing
    # ========================================
    st.header("📝 Test 1: Journal Parsing")
    st.caption("Parse natural language journal entries into structured tasks using Cortex AI")
    
    # Journal input
    journal_text = st.text_area(
        "Enter journal text:",
        value="I need to prepare slides for my presentation, practice my demo, and send follow-up emails to attendees",
        height=150,
        key="journal_input"
    )
    
    col1, col2 = st.columns([1, 4])
    with col1:
        parse_button = st.button("🤖 Parse with AI", type="primary", use_container_width=True)
    
    if parse_button:
        if not journal_text.strip():
            st.warning("⚠️ Please enter some journal text first")
        else:
            try:
                with st.spinner("⏳ Parsing with Snowflake Cortex AI..."):
                    # Parse journal using client
                    parsed_tasks = client.parse_journal(journal_text)
                
                # Display results
                st.success(f"✅ Successfully parsed {len(parsed_tasks)} tasks!", icon="🎉")
                
                # Show JSON
                with st.expander("📋 View Raw JSON Response"):
                    st.json(parsed_tasks)
                
                # Display tasks in cards
                st.subheader("Parsed Tasks:")
                for i, task in enumerate(parsed_tasks, 1):
                    with st.container():
                        st.markdown(f"### Task {i}: {task.get('title', 'Untitled')}")
                        
                        col1, col2 = st.columns([3, 1])
                        with col1:
                            st.write(f"**Description:** {task.get('description', 'No description')}")
                        with col2:
                            st.metric("Duration", f"{task.get('estimated_duration', 0)} min")
                        
                        # Display subtasks
                        st.write("**Subtasks:**")
                        for j, subtask in enumerate(task.get('subtasks', []), 1):
                            st.write(f"   {j}. {subtask}")
                        
                        st.divider()
                
            except Exception as e:
                st.error(f"❌ Error parsing journal: {str(e)}")
                with st.expander("🔍 Error Details"):
                    st.code(str(e))
    
    st.divider()
    
    # ========================================
    # TEST 2: Coach Messages
    # ========================================
    st.header("🎙️ Test 2: AI Coach Messages")
    st.caption("Generate motivational coaching messages for different session events")
    
    # Task context inputs
    col1, col2 = st.columns(2)
    with col1:
        task_name = st.text_input("Task Name", value="Write Project Report", key="coach_task")
    with col2:
        duration = st.number_input("Duration (minutes)", min_value=30, max_value=120, value=90, step=15, key="coach_duration")
    
    # Coach message buttons
    st.write("**Click a button to generate a coaching message:**")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("▶️ Session Start", use_container_width=True):
            try:
                with st.spinner("🤖 Generating message..."):
                    message = client.get_coach_message(
                        'session_start',
                        {'task': task_name, 'duration': duration}
                    )
                st.info(f"🎙️ {message}")
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
    
    with col2:
        if st.button("⏱️ Halfway", use_container_width=True):
            try:
                with st.spinner("🤖 Generating message..."):
                    message = client.get_coach_message(
                        'halfway',
                        {'task': task_name, 'duration': duration}
                    )
                st.info(f"🎙️ {message}")
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
    
    with col3:
        if st.button("☕ Break", use_container_width=True):
            try:
                with st.spinner("🤖 Generating message..."):
                    message = client.get_coach_message(
                        'break',
                        {'task': task_name, 'duration': duration}
                    )
                st.info(f"🎙️ {message}")
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
    
    with col4:
        if st.button("✅ Completion", use_container_width=True):
            try:
                with st.spinner("🤖 Generating message..."):
                    message = client.get_coach_message(
                        'completion',
                        {'task': task_name, 'duration': duration}
                    )
                st.info(f"🎙️ {message}")
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
    
    st.divider()
    
    # ========================================
    # TEST 3: Data Storage
    # ========================================
    st.header("💾 Test 3: Data Storage")
    st.caption("Save tasks to Snowflake database")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        test_task_title = st.text_input("Task Title", value="Test Task", key="save_title")
    with col2:
        test_task_duration = st.number_input("Duration (min)", min_value=30, max_value=120, value=60, key="save_duration")
    with col3:
        test_task_priority = st.slider("Priority", min_value=0.0, max_value=100.0, value=75.0, step=5.0, key="save_priority")
    
    test_task_desc = st.text_area("Description", value="This is a test task to verify data storage", key="save_desc")
    
    if st.button("💾 Save Test Task", type="primary"):
        try:
            # Create test task
            test_task = {
                'task_id': str(uuid.uuid4()),
                'title': test_task_title,
                'description': test_task_desc,
                'estimated_duration': test_task_duration,
                'subtasks': ['Setup environment', 'Write code', 'Test functionality'],
                'status': 'pending',
                'priority_score': test_task_priority
            }
            
            with st.spinner("💾 Saving to Snowflake..."):
                result = client.save_task(test_task)
            
            st.success(result, icon="✅")
            st.toast("✅ Task saved successfully!", icon="✅")
            
            # Display saved task details
            with st.expander("📋 Saved Task Details"):
                st.json(test_task)
                
        except Exception as e:
            st.error(f"❌ Error saving task: {str(e)}")
            with st.expander("🔍 Error Details"):
                st.code(str(e))
    
    st.divider()
    
    # ========================================
    # TEST 4: Retrieve Tasks
    # ========================================
    st.header("📥 Test 4: Retrieve Tasks")
    st.caption("Query and display tasks from Snowflake database")
    
    col1, col2, col3 = st.columns([1, 1, 3])
    
    with col1:
        if st.button("🔄 Get All Tasks", type="primary", use_container_width=True):
            try:
                with st.spinner("📥 Retrieving tasks from Snowflake..."):
                    tasks = client.get_all_tasks()
                
                if not tasks:
                    st.info("ℹ️ No tasks found in database")
                else:
                    st.success(f"✅ Retrieved {len(tasks)} tasks!", icon="📦")
                    
                    # Display tasks in expandable cards
                    for i, task in enumerate(tasks, 1):
                        with st.expander(f"📌 {task.get('title', 'Untitled Task')}", expanded=False):
                            col1, col2, col3 = st.columns(3)
                            
                            with col1:
                                st.metric("Duration", f"{task.get('estimated_duration', 0)} min")
                            with col2:
                                st.metric("Priority", f"{task.get('priority_score', 0):.1f}")
                            with col3:
                                status = task.get('status', 'unknown')
                                status_emoji = {
                                    'pending': '⏳',
                                    'in_progress': '▶️',
                                    'completed': '✅'
                                }.get(status, '❓')
                                st.metric("Status", f"{status_emoji} {status.replace('_', ' ').title()}")
                            
                            st.write(f"**Description:** {task.get('description', 'No description')}")
                            st.caption(f"**Task ID:** `{task.get('task_id', 'N/A')}`")
                            st.caption(f"**Created:** {task.get('created_at', 'Unknown')}")
                            
                            # Display subtasks if available
                            subtasks = task.get('subtasks', [])
                            if subtasks:
                                st.write("**Subtasks:**")
                                for j, subtask in enumerate(subtasks, 1):
                                    st.write(f"   {j}. {subtask}")
                    
            except Exception as e:
                st.error(f"❌ Error retrieving tasks: {str(e)}")
                with st.expander("🔍 Error Details"):
                    st.code(str(e))
    
    with col2:
        if st.button("📊 Get Statistics", use_container_width=True):
            try:
                with st.spinner("📊 Fetching session statistics..."):
                    stats = client.get_session_statistics()
                
                st.success("✅ Statistics retrieved!", icon="📈")
                
                # Display statistics
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Total Sessions", stats.get('total_sessions', 0))
                    st.metric("Total Time", f"{stats.get('total_minutes', 0)} min")
                with col2:
                    st.metric("Completion Rate", f"{stats.get('completion_rate', 0)}%")
                    st.metric("Unique Tasks", stats.get('unique_tasks', 0))
                
            except Exception as e:
                st.error(f"❌ Error getting statistics: {str(e)}")
    
    st.divider()
    
    # ========================================
    # TEST 5: Save Work Session
    # ========================================
    st.header("⏱️ Test 5: Work Session Tracking")
    st.caption("Save completed work sessions to database")
    
    col1, col2 = st.columns(2)
    with col1:
        session_duration = st.number_input("Session Duration (min)", min_value=5, max_value=120, value=45, key="session_duration")
    with col2:
        session_completed = st.checkbox("Completed", value=True, key="session_completed")
    
    if st.button("💾 Save Work Session", type="primary"):
        try:
            # Create test session
            test_session = {
                'session_id': str(uuid.uuid4()),
                'task_id': str(uuid.uuid4()),  # Random task ID for test
                'start_time': datetime.now().isoformat(),
                'duration_minutes': session_duration,
                'completed': session_completed
            }
            
            with st.spinner("💾 Saving work session..."):
                result = client.save_work_session(test_session)
            
            st.success(result, icon="✅")
            st.toast("✅ Work session saved!", icon="✅")
            
            with st.expander("📋 Session Details"):
                st.json(test_session)
                
        except Exception as e:
            st.error(f"❌ Error saving work session: {str(e)}")
            with st.expander("🔍 Error Details"):
                st.code(str(e))
    
    st.divider()
    
    # ========================================
    # TEST 6: Update Task Status
    # ========================================
    st.header("🔄 Test 6: Update Task Status")
    st.caption("Update the status of existing tasks")
    
    col1, col2 = st.columns(2)
    with col1:
        update_task_id = st.text_input("Task ID to Update", placeholder="Enter task ID from above", key="update_task_id")
    with col2:
        new_status = st.selectbox("New Status", options=["pending", "in_progress", "completed"], key="update_status")
    
    if st.button("🔄 Update Status", type="primary"):
        if not update_task_id.strip():
            st.warning("⚠️ Please enter a task ID")
        else:
            try:
                with st.spinner("🔄 Updating task status..."):
                    result = client.update_task_status(update_task_id, new_status)
                
                st.success(result, icon="✅")
                st.toast("✅ Status updated!", icon="✅")
                
            except Exception as e:
                st.error(f"❌ Error updating status: {str(e)}")
                with st.expander("🔍 Error Details"):
                    st.code(str(e))
    
    # Footer
    st.divider()
    st.markdown(
        """
        <div style='text-align: center; padding: 20px; color: #666;'>
            <p><strong>All tests use real Snowflake Cortex AI ⚡</strong></p>
            <p>Powered by Streamlit + Snowflake</p>
        </div>
        """,
        unsafe_allow_html=True
    )


if __name__ == "__main__":
    main()
