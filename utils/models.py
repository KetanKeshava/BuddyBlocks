"""
Data models for Focus Flow
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional
import uuid
import streamlit as st


@dataclass
class Task:
    """Task model for Focus Flow"""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    title: str = ""
    description: str = ""
    estimated_duration: int = 30  # minutes
    subtasks: List[str] = field(default_factory=list)
    status: str = "pending"  # pending/in_progress/completed
    priority_score: float = 50.0  # 0-100
    created_at: datetime = field(default_factory=datetime.now)


@dataclass
class WorkSession:
    """Work session model for Focus Flow"""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    task_id: str = ""
    start_time: datetime = field(default_factory=datetime.now)
    duration_minutes: int = 0
    completed: bool = False


def initialize_session_state():
    """Initialize session state variables for the app"""
    
    # User settings
    if 'work_duration' not in st.session_state:
        st.session_state.work_duration = 90
    if 'break_duration' not in st.session_state:
        st.session_state.break_duration = 15
    if 'voice_coach' not in st.session_state:
        st.session_state.voice_coach = True
    
    # Task management
    if 'tasks' not in st.session_state:
        st.session_state.tasks = []
    if 'current_task' not in st.session_state:
        st.session_state.current_task = None
    
    # Timer and session tracking
    if 'timer_running' not in st.session_state:
        st.session_state.timer_running = False
    if 'time_remaining' not in st.session_state:
        st.session_state.time_remaining = 0
    if 'session_start' not in st.session_state:
        st.session_state.session_start = None
    
    # Statistics
    if 'completed_sessions' not in st.session_state:
        st.session_state.completed_sessions = 0
    if 'total_focus_time' not in st.session_state:
        st.session_state.total_focus_time = 0
