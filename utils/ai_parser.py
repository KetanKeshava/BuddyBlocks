"""
AI Parser utilities for Focus Flow
Parses journal entries into structured tasks
"""

import random
import re
from typing import List
from datetime import datetime
import uuid
from utils.models import Task


def parse_journal_mock(journal_text: str) -> List[Task]:
    """
    Parse journal text and create Task objects (mock implementation)
    
    Args:
        journal_text: Raw journal entry text
        
    Returns:
        List of Task objects parsed from the journal
    """
    if not journal_text or not journal_text.strip():
        return []
    
    # Split text into sentences
    sentences = re.split(r'[.!?]+', journal_text)
    sentences = [s.strip() for s in sentences if s.strip() and len(s.strip()) > 10]
    
    # Limit to 3-5 tasks
    num_tasks = min(len(sentences), random.randint(3, 5))
    selected_sentences = sentences[:num_tasks]
    
    tasks = []
    
    for sentence in selected_sentences:
        # Extract title (first 5-7 words)
        words = sentence.split()
        title_length = min(len(words), random.randint(5, 7))
        title = ' '.join(words[:title_length])
        
        # Clean up title (remove common starting words)
        title = re.sub(r'^(I need to|I have to|I must|I should|I will|I want to)\s+', '', title, flags=re.IGNORECASE)
        title = title.capitalize()
        if not title.endswith('...') and len(words) > title_length:
            title += '...'
        
        # Use full sentence as description
        description = sentence.strip()
        
        # Random estimated duration (30-120 minutes)
        estimated_duration = random.choice([30, 45, 60, 75, 90, 120])
        
        # Generate 2-4 subtasks
        num_subtasks = random.randint(2, 4)
        subtask_templates = [
            "Research and gather information",
            "Create initial draft or outline",
            "Review and refine content",
            "Get feedback from stakeholders",
            "Make final revisions",
            "Prepare supporting materials",
            "Schedule follow-up meeting",
            "Document findings and results"
        ]
        subtasks = random.sample(subtask_templates, min(num_subtasks, len(subtask_templates)))
        
        # Random priority score (40-80)
        priority_score = round(random.uniform(40, 80), 1)
        
        # Create Task object
        task = Task(
            id=str(uuid.uuid4()),
            title=title,
            description=description,
            estimated_duration=estimated_duration,
            subtasks=subtasks,
            status="pending",
            priority_score=priority_score,
            created_at=datetime.now()
        )
        
        tasks.append(task)
    
    return tasks
