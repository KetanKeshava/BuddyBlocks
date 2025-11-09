"""
Focus Flow - AI-Powered Task Coach with Smart Time Blocking
Main Streamlit application with Snowflake Cortex AI integration
"""

import streamlit as st
import time
import uuid
from datetime import datetime
from utils.models import initialize_session_state
from utils.snowflake_client import get_snowflake_client
from utils.ui_components import show_connection_status, show_ai_badge


def display_task_card(task):
    """Display a task in an expandable card format"""
    # Determine priority color
    if task.priority_score > 70:
        priority_color = "🔴"
        priority_label = "High"
    elif task.priority_score >= 40:
        priority_color = "🟡"
        priority_label = "Medium"
    else:
        priority_color = "🟢"
        priority_label = "Low"
    
    with st.expander(f"**{task.title}**", expanded=False):
        st.write(f"**Description:** {task.description}")
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"⏱️ **Duration:** `{task.estimated_duration} min`")
        with col2:
            st.markdown(f"{priority_color} **Priority:** `{priority_label} ({task.priority_score:.1f})`")
        
        st.write("**Subtasks:**")
        for i, subtask in enumerate(task.subtasks, 1):
            st.write(f"{i}. {subtask}")


def display_task_grid_card(task, index):
    """Display a task card in the grid layout"""
    # Determine priority emoji and color
    if task.priority_score > 70:
        priority_emoji = "🔴"
        priority_label = "High"
        border_color = "#ff6b6b"
    elif task.priority_score >= 40:
        priority_emoji = "🟡"
        priority_label = "Medium"
        border_color = "#ffd93d"
    else:
        priority_emoji = "🟢"
        priority_label = "Low"
        border_color = "#6bcf7f"
    
    # Status badge color
    status_colors = {
        "pending": "#95a5a6",
        "in_progress": "#3498db",
        "completed": "#2ecc71"
    }
    status_color = status_colors.get(task.status, "#95a5a6")
    
    # Truncate description
    description = task.description
    if len(description) > 100:
        description = description[:100] + "..."
    
    # Create card with custom styling
    with st.container():
        st.markdown(
            f"""
            <div style="
                border-left: 4px solid {border_color};
                padding: 15px;
                margin-bottom: 15px;
                background-color: #f8f9fa;
                border-radius: 5px;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            ">
                <h4 style="margin: 0 0 10px 0;">{priority_emoji} {task.title}</h4>
                <p style="color: #666; font-size: 14px; margin: 5px 0;">{description}</p>
            </div>
            """,
            unsafe_allow_html=True
        )
        
        # Metrics row
        col1, col2, col3 = st.columns([2, 2, 2])
        with col1:
            st.markdown(f"⏱️ **{task.estimated_duration} min**")
        with col2:
            st.markdown(f"**Priority:** {task.priority_score:.0f}")
        with col3:
            st.markdown(
                f"<span style='background-color: {status_color}; color: white; padding: 2px 8px; border-radius: 10px; font-size: 12px;'>{task.status.replace('_', ' ').title()}</span>",
                unsafe_allow_html=True
            )
        
        # Subtasks expander
        with st.expander("📋 View Subtasks"):
            for i, subtask in enumerate(task.subtasks, 1):
                st.checkbox(subtask, key=f"subtask_{task.id}_{i}")
        
        # Start button
        if task.status != "completed":
            if st.button(
                "▶️ Start" if task.status == "pending" else "▶️ Continue",
                key=f"start_task_{task.id}",
                type="primary",
                use_container_width=True
            ):
                # Set current task
                st.session_state.current_task = task
                
                # Update task status
                task.status = "in_progress"
                
                # Initialize timer
                st.session_state.time_remaining = task.estimated_duration * 60  # Convert to seconds
                st.session_state.session_start = time.time()
                st.session_state.timer_running = True
                
                # Show success toast
                st.toast(f"Starting focus session on: {task.title}", icon="✅")
                
                # Switch to Focus Session tab
                st.session_state.active_tab = "focus"
                time.sleep(0.5)  # Brief delay for toast to show
                st.rerun()
        else:
            st.success("✅ Completed", icon="✅")


def sort_tasks(tasks, sort_by):
    """Sort tasks based on selected criteria"""
    if sort_by == "Duration":
        return sorted(tasks, key=lambda t: t.estimated_duration, reverse=True)
    elif sort_by == "Priority":
        return sorted(tasks, key=lambda t: t.priority_score, reverse=True)
    elif sort_by == "Created":
        return sorted(tasks, key=lambda t: t.created_at, reverse=True)
    elif sort_by == "Title":
        return sorted(tasks, key=lambda t: t.title.lower())
    return tasks


def filter_tasks(tasks, filter_by):
    """Filter tasks based on status"""
    if filter_by == "All":
        return tasks
    elif filter_by == "Pending":
        return [t for t in tasks if t.status == "pending"]
    elif filter_by == "In Progress":
        return [t for t in tasks if t.status == "in_progress"]
    elif filter_by == "Completed":
        return [t for t in tasks if t.status == "completed"]
    return tasks


def display_focus_session():
    """Display the focus session timer interface"""
    
    # Get client for coach messages
    client = get_snowflake_client()
    
    # Check if current task exists
    if st.session_state.current_task is None:
        st.info("👈 Select a task from the Tasks tab to start a focus session")
        
        # Show motivational message
        start_message = client.get_coach_message('session_start', {'task': 'a task', 'duration': 60})
        st.info(f"🎙️ Coach: {start_message}")
        return
    
    task = st.session_state.current_task
    
    # Display current task prominently
    st.markdown(f"## 🎯 {task.title}")
    st.caption(f"{task.description}")
    
    st.divider()
    
    # Calculate time remaining
    if st.session_state.timer_running:
        elapsed = time.time() - st.session_state.session_start
        remaining = max(0, st.session_state.time_remaining - elapsed)
    else:
        remaining = st.session_state.time_remaining
    
    # Format timer display
    minutes = int(remaining // 60)
    seconds = int(remaining % 60)
    timer_display = f"{minutes:02d}:{seconds:02d}"
    
    # Calculate progress
    total_duration = task.estimated_duration * 60  # seconds
    progress = 1 - (remaining / total_duration) if total_duration > 0 else 1.0
    progress = max(0.0, min(1.0, progress))  # Clamp between 0 and 1
    
    # Display timer in center with large font
    st.markdown(
        f"""
        <div style="text-align: center; margin: 40px 0;">
            <div style="font-size: 72px; font-weight: bold; color: #667eea; font-family: monospace;">
                {timer_display}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    # Progress bar
    st.progress(progress)
    st.caption(f"Progress: {progress * 100:.1f}%")
    
    # Show coach message at halfway point
    if 0.45 <= progress <= 0.55 and 'halfway_message_shown' not in st.session_state:
        halfway_message = client.get_coach_message(
            'halfway',
            {'task': task.title, 'duration': task.estimated_duration}
        )
        st.info(f"🎙️ Coach: {halfway_message}")
        st.session_state.halfway_message_shown = True
    
    st.divider()
    
    # Control buttons
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.session_state.timer_running:
            if st.button("⏸️ Pause", use_container_width=True):
                st.session_state.timer_running = False
                # Update time_remaining to current remaining time
                elapsed = time.time() - st.session_state.session_start
                st.session_state.time_remaining = max(0, st.session_state.time_remaining - elapsed)
                st.rerun()
    
    with col2:
        if not st.session_state.timer_running and remaining > 0:
            if st.button("▶️ Resume", use_container_width=True):
                st.session_state.timer_running = True
                st.session_state.session_start = time.time()
                st.rerun()
    
    with col3:
        if st.button("✅ Complete", type="primary", use_container_width=True):
            # Mark task as completed
            task.status = "completed"
            
            # Update statistics
            actual_time = (task.estimated_duration * 60 - remaining) // 60  # Convert back to minutes
            st.session_state.completed_sessions += 1
            st.session_state.total_focus_time += actual_time
            
            # Get completion message from coach
            completion_message = client.get_coach_message(
                'completion',
                {'task': task.title, 'duration': actual_time}
            )
            
            # Try to save task to database (if Snowflake connected)
            try:
                task_data = {
                    'task_id': task.id,
                    'title': task.title,
                    'description': task.description,
                    'estimated_duration': task.estimated_duration,
                    'subtasks': task.subtasks,
                    'status': 'completed',
                    'priority_score': task.priority_score
                }
                save_result = client.save_task(task_data)
                st.success(save_result)
            except Exception as e:
                # Database save failed - that's OK in demo mode
                pass
            
            # Reset timer state
            st.session_state.current_task = None
            st.session_state.timer_running = False
            st.session_state.time_remaining = 0
            st.session_state.session_start = None
            st.session_state.pop('halfway_message_shown', None)
            
            # Show success message with coach feedback
            st.success(f"✅ {completion_message}")
            st.balloons()
            
            time.sleep(2)
            st.rerun()
    
    # Auto-rerun every second if timer is running
    if st.session_state.timer_running and remaining > 0:
        time.sleep(1)
        st.rerun()
    
    # Timer finished
    if remaining <= 0 and st.session_state.timer_running:
        st.session_state.timer_running = False
        st.success("⏰ Time's up! Great work on this focus session!")
        st.balloons()


def main():
    # Set page configuration
    st.set_page_config(
        page_title="Focus Flow",
        page_icon="🎯",
        layout="wide"
    )
    
    # Initialize session state
    initialize_session_state()
    
    # Initialize Snowflake client (with automatic fallback to mock AI)
    client = get_snowflake_client()
    
    # Initialize active tab if not exists
    if 'active_tab' not in st.session_state:
        st.session_state.active_tab = "journal"
    
    # App header with AI badge
    col1, col2 = st.columns([4, 1])
    with col1:
        st.title("🎯 Focus Flow")
        st.subheader("AI-Powered Task Coach with Smart Time Blocking")
    with col2:
        show_ai_badge(client)
    
    # Sidebar
    with st.sidebar:
        # Connection status
        st.header("🔌 Connection")
        show_connection_status(client)
        
        # Cache clear button (for debugging)
        if st.button("🔄 Refresh Connection", help="Clear cache and reconnect"):
            st.cache_resource.clear()
            st.rerun()
        
        st.header("⚙️ Settings")
        
        # Work duration slider
        work_duration = st.slider(
            "Work Duration (minutes)",
            min_value=30,
            max_value=120,
            value=st.session_state.work_duration,
            step=15,
            key='work_duration'
        )
        
        # Break duration slider
        break_duration = st.slider(
            "Break Duration (minutes)",
            min_value=5,
            max_value=30,
            value=st.session_state.break_duration,
            step=5,
            key='break_duration'
        )
        
        # Voice coach toggle
        voice_coach = st.toggle(
            "Voice Coach",
            value=st.session_state.voice_coach,
            key='voice_coach'
        )
        
        # Add spacing
        st.divider()
        
        # Today's Stats section
        st.header("📊 Today's Stats")
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric(
                "Focus Sessions", 
                st.session_state.completed_sessions, 
                delta=None
            )
            st.metric(
                "Tasks Done", 
                len([t for t in st.session_state.tasks if t.status == 'completed']), 
                delta=None
            )
        
        with col2:
            hours = st.session_state.total_focus_time // 60
            minutes = st.session_state.total_focus_time % 60
            st.metric(
                "Total Time", 
                f"{hours}h {minutes}m" if hours > 0 else f"{minutes}m", 
                delta=None
            )
            st.metric("Streak", "0 days", delta=None)
    
    # Main content area with tabs
    # Determine selected tab based on session state
    tab_names = ["📝 Journal", "✅ Tasks", "⏱️ Focus Session", "📊 Analytics"]
    if st.session_state.active_tab == "focus":
        default_index = 2
        st.session_state.active_tab = "journal"  # Reset for next time
    else:
        default_index = 0
    
    tab1, tab2, tab3, tab4 = st.tabs(tab_names)
    
    with tab1:
        st.write("### What's on your mind?")
        st.caption("Write naturally about what you need to do. I'll break it down into manageable tasks.")
        
        # Initialize journal_input in session state if not exists
        if 'journal_input' not in st.session_state:
            st.session_state.journal_input = ""
        
        # Journal text area
        journal_input = st.text_area(
            "Journal Entry",
            value=st.session_state.journal_input,
            height=200,
            placeholder="I need to finish the project proposal by Friday. This includes researching competitors, writing the executive summary, and creating a budget breakdown...",
            key='journal_text_area'
        )
        
        # Update session state with journal input
        st.session_state.journal_input = journal_input
        
        # Break it Down button
        if st.button("✨ Break it Down", type="primary", use_container_width=True):
            if journal_input.strip():
                # Show spinner while processing
                with st.spinner(f"🤖 {client.get_ai_source()} is analyzing your tasks..."):
                    try:
                        # Parse journal using Snowflake client (with automatic fallback)
                        parsed_tasks_data = client.parse_journal(journal_input)
                        
                        # Convert to Task objects
                        from utils.models import Task
                        parsed_tasks = []
                        for task_data in parsed_tasks_data:
                            task = Task(
                                id=task_data.get('task_id', str(uuid.uuid4())),
                                title=task_data.get('title', 'Untitled Task'),
                                description=task_data.get('description', ''),
                                estimated_duration=task_data.get('estimated_duration', 60),
                                subtasks=task_data.get('subtasks', []),
                                status=task_data.get('status', 'pending'),
                                priority_score=task_data.get('priority_score', 50.0),
                                created_at=datetime.now()
                            )
                            parsed_tasks.append(task)
                        
                        # Add tasks to session state
                        st.session_state.tasks.extend(parsed_tasks)
                        
                        # Show success message
                        st.success(f"✅ {len(parsed_tasks)} tasks created using {client.get_ai_source()}!")
                        
                        # Get a motivational coach message
                        coach_message = client.get_coach_message(
                            'session_start',
                            {'task': 'your new tasks', 'duration': sum(t.estimated_duration for t in parsed_tasks)}
                        )
                        st.info(f"🎙️ Coach: {coach_message}")
                        
                        # Display balloons animation
                        st.balloons()
                        
                        # Clear journal input
                        st.session_state.journal_input = ""
                        st.rerun()
                        
                    except Exception as e:
                        st.error(f"❌ Error parsing journal: {str(e)}")
                        st.info("💡 The app is still functional. Try again or check your connection.")
            else:
                st.warning("Please write something in your journal entry first.")
        
        # Display parsed tasks if any exist
        if st.session_state.tasks:
            st.divider()
            st.write("### 📋 Parsed Tasks")
            st.caption(f"Total: {len(st.session_state.tasks)} tasks")
            
            for task in st.session_state.tasks:
                display_task_card(task)
    
    with tab2:
        st.write("### Your Task List")
        
        # Check if tasks exist
        if not st.session_state.tasks:
            st.info("No tasks yet. Go to the Journal tab to create some!")
        else:
            # Filter and Sort Controls
            col1, col2, col3 = st.columns([2, 2, 4])
            
            with col1:
                sort_option = st.selectbox(
                    "Sort by",
                    options=["Duration", "Priority", "Created", "Title"],
                    key="task_sort"
                )
            
            with col2:
                filter_option = st.selectbox(
                    "Filter",
                    options=["All", "Pending", "In Progress", "Completed"],
                    key="task_filter"
                )
            
            st.divider()
            
            # Apply filtering and sorting
            filtered_tasks = filter_tasks(st.session_state.tasks, filter_option)
            sorted_tasks = sort_tasks(filtered_tasks, sort_option)
            
            # Display task count
            st.caption(f"Showing {len(sorted_tasks)} of {len(st.session_state.tasks)} tasks")
            
            # Display tasks in grid layout (2 columns)
            if sorted_tasks:
                for i in range(0, len(sorted_tasks), 2):
                    cols = st.columns(2)
                    
                    # First column
                    with cols[0]:
                        display_task_grid_card(sorted_tasks[i], i)
                    
                    # Second column (if task exists)
                    if i + 1 < len(sorted_tasks):
                        with cols[1]:
                            display_task_grid_card(sorted_tasks[i + 1], i + 1)
            else:
                st.info(f"No tasks match the filter: {filter_option}")
    
    with tab3:
        st.write("### Focus Session")
        display_focus_session()
    
    with tab4:
        st.write("### 📊 Analytics & Insights")
        
        # Check if connected to Snowflake for analytics
        if client and client.is_connected:
            st.info(f"📡 Connected to {client.get_ai_source()} - Real-time analytics available!")
            
            try:
                # Get session statistics from Snowflake
                stats = client.get_session_statistics()
                
                st.subheader("Today's Performance")
                
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.metric(
                        "Total Sessions",
                        stats.get('total_sessions', 0),
                        help="Number of focus sessions completed today"
                    )
                
                with col2:
                    total_min = stats.get('total_minutes', 0)
                    hours = total_min // 60
                    minutes = total_min % 60
                    st.metric(
                        "Total Time",
                        f"{hours}h {minutes}m" if hours > 0 else f"{minutes}m",
                        help="Total focus time today"
                    )
                
                with col3:
                    st.metric(
                        "Completion Rate",
                        f"{stats.get('completion_rate', 0)}%",
                        help="Percentage of sessions completed"
                    )
                
                with col4:
                    st.metric(
                        "Unique Tasks",
                        stats.get('unique_tasks', 0),
                        help="Number of different tasks worked on"
                    )
                
                st.divider()
                
                # Get all tasks from database
                try:
                    all_tasks = client.get_all_tasks()
                    
                    if all_tasks:
                        st.subheader("📋 Task History")
                        st.caption(f"Showing {len(all_tasks)} tasks from database")
                        
                        # Display recent tasks
                        for task in all_tasks[:10]:  # Show last 10 tasks
                            with st.expander(f"{'✅' if task['status'] == 'completed' else '⏳'} {task['title']}"):
                                st.write(f"**Description:** {task['description']}")
                                st.write(f"**Duration:** {task['estimated_duration']} minutes")
                                st.write(f"**Status:** {task['status']}")
                                st.write(f"**Priority:** {task['priority_score']}")
                                st.caption(f"Created: {task['created_at']}")
                    else:
                        st.info("No task history yet. Complete some tasks to see analytics!")
                
                except Exception as e:
                    st.warning(f"⚠️ Could not load task history: {str(e)}")
            
            except Exception as e:
                st.error(f"❌ Error loading analytics: {str(e)}")
        
        else:
            # Demo mode analytics
            st.warning("⚠️ Running in Demo Mode - Analytics limited to session data")
            
            st.subheader("Session Statistics")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Tasks Created", len(st.session_state.tasks))
            
            with col2:
                completed = len([t for t in st.session_state.tasks if t.status == 'completed'])
                st.metric("Tasks Completed", completed)
            
            with col3:
                hours = st.session_state.total_focus_time // 60
                minutes = st.session_state.total_focus_time % 60
                st.metric("Focus Time", f"{hours}h {minutes}m" if hours > 0 else f"{minutes}m")
            
            st.info("""
            **💡 Connect to Snowflake for:**
            - Persistent task storage
            - Historical analytics
            - Advanced insights
            - Cross-device sync
            
            Check the sidebar for connection options.
            """)
            
            # Show task breakdown
            if st.session_state.tasks:
                st.divider()
                st.subheader("Task Status Breakdown")
                
                status_counts = {
                    'pending': len([t for t in st.session_state.tasks if t.status == 'pending']),
                    'in_progress': len([t for t in st.session_state.tasks if t.status == 'in_progress']),
                    'completed': len([t for t in st.session_state.tasks if t.status == 'completed'])
                }
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("⏳ Pending", status_counts['pending'])
                with col2:
                    st.metric("▶️ In Progress", status_counts['in_progress'])
                with col3:
                    st.metric("✅ Completed", status_counts['completed'])
    
    # Footer
    st.divider()
    
    # Show current AI source
    footer_col1, footer_col2 = st.columns([3, 1])
    with footer_col1:
        st.markdown(
            "<div style='text-align: center; color: #666; padding: 20px;'>"
            "Built with Streamlit + Snowflake Cortex AI"
            "</div>",
            unsafe_allow_html=True
        )
    with footer_col2:
        if client and client.is_connected:
            st.success("🟢 Live")
            st.caption("Connected to Snowflake")
        else:
            st.warning("🟡 Demo")
            st.caption("Using Mock AI")

if __name__ == "__main__":
    main()
