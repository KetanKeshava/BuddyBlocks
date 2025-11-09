"""
Mock AI Parser for Focus Flow
Fallback functions when Snowflake Cortex AI is not available
Provides realistic task parsing and coaching messages for demos and offline use
"""

import random
import re
from typing import List, Dict
import uuid


def parse_journal_mock(journal_text: str) -> List[Dict]:
    """
    Mock implementation of journal parsing (fallback when Cortex AI unavailable)
    
    Parses journal text into structured tasks with realistic-looking data.
    This function attempts to intelligently break down journal entries into
    actionable tasks with reasonable time estimates and subtasks.
    
    Args:
        journal_text: Raw journal entry text to parse
        
    Returns:
        List[Dict]: List of task dictionaries with structure:
            - task_id: Unique identifier (UUID)
            - title: Task title (first 5-7 words)
            - description: Full sentence or paragraph
            - estimated_duration: Duration in minutes (30-120)
            - subtasks: List of 2-4 subtask strings
            - status: Always "pending" for new tasks
            - priority_score: Priority score (40-80)
    
    Example:
        >>> journal = "I need to prepare slides for my presentation."
        >>> tasks = parse_journal_mock(journal)
        >>> len(tasks)
        1
        >>> tasks[0]['title']
        'Prepare slides for my presentation'
    """
    
    if not journal_text or not journal_text.strip():
        return []
    
    # Split text into sentences using multiple delimiters
    # Handle periods, exclamation marks, question marks, and newlines
    sentences = re.split(r'[.!?\n]+', journal_text)
    
    # Filter out empty sentences and very short ones
    sentences = [s.strip() for s in sentences if s.strip() and len(s.strip()) > 10]
    
    if not sentences:
        return []
    
    # Determine number of tasks to create (3-5, but not more than available sentences)
    num_tasks = min(len(sentences), random.randint(3, 5))
    
    # Select sentences to convert into tasks
    selected_sentences = sentences[:num_tasks]
    
    tasks = []
    
    # Common action words that indicate subtasks
    action_words = [
        "Research", "Draft", "Review", "Write", "Create", "Design",
        "Implement", "Test", "Debug", "Document", "Analyze", "Plan",
        "Organize", "Schedule", "Prepare", "Finalize", "Edit", "Revise"
    ]
    
    for sentence in selected_sentences:
        # Extract title (first 5-7 words of sentence)
        words = sentence.split()
        title_length = min(len(words), random.randint(5, 7))
        title_words = words[:title_length]
        
        # Clean up title by removing common starting phrases
        title = ' '.join(title_words)
        title = re.sub(
            r'^(I need to|I have to|I must|I should|I will|I want to|I am going to|I plan to)\s+',
            '',
            title,
            flags=re.IGNORECASE
        )
        
        # Capitalize first letter
        if title:
            title = title[0].upper() + title[1:] if len(title) > 1 else title.upper()
        
        # Add ellipsis if sentence was truncated
        if len(words) > title_length and not title.endswith('...'):
            title += '...'
        
        # Use full sentence as description
        description = sentence.strip()
        
        # Generate realistic estimated duration (30, 45, 60, 75, 90, 120 minutes)
        duration_options = [30, 45, 60, 75, 90, 120]
        estimated_duration = random.choice(duration_options)
        
        # Generate 2-4 subtasks based on the task context
        num_subtasks = random.randint(2, 4)
        
        # Create contextual subtasks
        subtasks = []
        
        # Try to extract key concepts from the sentence for more relevant subtasks
        key_words = [w for w in words if len(w) > 4 and w.lower() not in 
                     ['need', 'have', 'must', 'should', 'will', 'want', 'going', 'plan']]
        
        if len(key_words) >= 2:
            # Create contextual subtasks based on sentence content
            context = ' '.join(key_words[:2])
            
            subtask_templates = [
                f"Research and gather information about {context}",
                f"Create initial outline or plan for {context}",
                f"Draft the main content for {context}",
                f"Review and refine {context}",
                f"Get feedback on {context}",
                f"Make final revisions to {context}",
                f"Prepare supporting materials for {context}",
                f"Test and validate {context}"
            ]
        else:
            # Use generic but realistic subtask templates
            subtask_templates = [
                "Research and gather necessary information",
                "Create initial draft or outline",
                "Review and refine the content",
                "Get stakeholder feedback",
                "Make final revisions and improvements",
                "Prepare supporting documentation",
                "Schedule follow-up meeting if needed",
                "Document findings and results",
                "Organize and structure materials",
                "Test and validate the approach"
            ]
        
        # Randomly select subtasks without replacement
        available_subtasks = subtask_templates.copy()
        random.shuffle(available_subtasks)
        subtasks = available_subtasks[:num_subtasks]
        
        # Generate priority score (40-80 range for moderate priorities)
        # Tasks with longer durations tend to have slightly higher priority
        base_priority = random.uniform(40, 80)
        
        # Adjust priority based on duration (longer tasks slightly higher priority)
        duration_factor = (estimated_duration - 30) / 90  # Normalize to 0-1
        priority_adjustment = duration_factor * 10  # Add up to 10 points
        
        priority_score = min(80, base_priority + priority_adjustment)
        priority_score = round(priority_score, 1)
        
        # Create task dictionary
        task = {
            'task_id': str(uuid.uuid4()),
            'title': title,
            'description': description,
            'estimated_duration': estimated_duration,
            'subtasks': subtasks,
            'status': 'pending',
            'priority_score': priority_score
        }
        
        tasks.append(task)
    
    return tasks


def get_coach_message_mock(message_type: str, context: Dict = None) -> str:
    """
    Mock implementation of coaching messages (fallback when Cortex AI unavailable)
    
    Generates motivational coaching messages for different session events.
    Messages are contextually appropriate and use task/duration information
    when available.
    
    Args:
        message_type: Type of coaching message to generate
                     ('session_start', 'halfway', 'break', 'completion')
        context: Optional dictionary with 'task' and 'duration' keys
                Default: {'task': 'this task', 'duration': 90}
        
    Returns:
        str: Formatted coaching message appropriate for the message type
    
    Example:
        >>> msg = get_coach_message_mock('session_start', {'task': 'Write Report', 'duration': 60})
        >>> 'Write Report' in msg or '60' in msg
        True
    """
    
    if context is None:
        context = {}
    
    # Get context values with defaults
    task_name = context.get('task', 'this task')
    duration = context.get('duration', 90)
    
    # Define message templates for each message type
    templates = {
        'session_start': [
            "Let's crush this {duration}-minute session on {task}! You've got this! 💪",
            "Ready to focus on {task}? Let's make these {duration} minutes count!",
            "Time to dive deep into {task}. Stay focused for {duration} minutes!",
            "Starting your {duration}-minute focus session on {task}. Let's go! 🚀",
            "Focus mode activated! {duration} minutes of pure productivity on {task}.",
            "Great choice working on {task}! Let's make progress in {duration} minutes.",
            "You've dedicated {duration} minutes to {task}. Let's make them matter!",
            "{duration} minutes of focused work ahead. {task} won't know what hit it! ⚡",
            "Ready, set, focus! {duration} minutes on {task} starts now.",
            "Block out distractions. {duration} minutes of deep work on {task} begins!"
        ],
        
        'halfway': [
            "You're halfway there! Keep that momentum going! 💪",
            "Great progress on {task}! You've got this! 🌟",
            "50% complete! Stay focused and finish strong!",
            "Awesome work so far! Keep pushing through on {task}!",
            "You're doing great! Halfway through your focus session! 🎯",
            "Strong work! Stay in the zone for the second half!",
            "Excellent progress! {task} is coming together nicely!",
            "You're crushing it! Keep that focus for the rest!",
            "Halfway done with {task}! Maintain that focus! 🔥",
            "Great pace! Stay strong for the final half!"
        ],
        
        'break': [
            "Time for a break! Stand up, stretch, and recharge. You've earned it! ☕",
            "Great work! Take 15 minutes to rest and rejuvenate. 🌟",
            "Break time! Grab some water and give your eyes a rest. 💧",
            "Well done! Step away from your screen and take a mindful break. 🧘",
            "Excellent session! Take a walk and let your mind wander. 🚶",
            "You've earned a break! Stretch, hydrate, and prepare for the next session. 💪",
            "Time to recharge! Take a short walk or do some light stretching. 🌿",
            "Break time! Do something completely different for 15 minutes. 🎨",
            "Great focus! Now rest your mind with a proper break. ☀️",
            "Session complete! Take time to breathe and reset. 🌊"
        ],
        
        'completion': [
            "Excellent work! You've successfully completed {task}! 🎉",
            "Task completed! Another win in the books! You're on fire! 🔥",
            "Boom! {task} is done! Great job staying focused! ⭐",
            "Mission accomplished! {task} is checked off your list! ✅",
            "Fantastic! You crushed {task}! Keep up the momentum! 🚀",
            "Well done! {task} is complete! You're making great progress! 💯",
            "Success! Another task conquered! You're unstoppable! 💪",
            "{task} is finished! Take a moment to celebrate your achievement! 🎊",
            "Outstanding work on {task}! You stayed focused and delivered! 🌟",
            "Complete! {task} is done and dusted! Keep riding this wave! 🏄"
        ]
    }
    
    # Get templates for the requested message type
    message_templates = templates.get(message_type, [
        "Keep up the great work! You're doing awesome! 🌟"
    ])
    
    # Randomly select a message template
    message = random.choice(message_templates)
    
    # Replace placeholders with actual values
    message = message.replace('{task}', task_name)
    message = message.replace('{duration}', str(duration))
    
    return message


def generate_mock_task(
    title: str = "Sample Task",
    duration_range: tuple = (30, 120)
) -> Dict:
    """
    Generate a single mock task with realistic data
    
    Useful for testing and demonstrations.
    
    Args:
        title: Title for the task
        duration_range: Tuple of (min_duration, max_duration) in minutes
        
    Returns:
        Dict: Task dictionary with all required fields
    """
    
    # Generate estimated duration within range
    min_duration, max_duration = duration_range
    duration_options = [d for d in [30, 45, 60, 75, 90, 120] 
                       if min_duration <= d <= max_duration]
    
    if not duration_options:
        estimated_duration = random.randint(min_duration, max_duration)
    else:
        estimated_duration = random.choice(duration_options)
    
    # Generate subtasks
    subtask_templates = [
        "Research and gather information",
        "Create initial outline or draft",
        "Review and refine content",
        "Get feedback from stakeholders",
        "Make final revisions",
        "Document results and findings"
    ]
    
    num_subtasks = random.randint(2, 4)
    subtasks = random.sample(subtask_templates, num_subtasks)
    
    # Generate priority
    priority_score = round(random.uniform(40, 80), 1)
    
    return {
        'task_id': str(uuid.uuid4()),
        'title': title,
        'description': f"Complete the task: {title}",
        'estimated_duration': estimated_duration,
        'subtasks': subtasks,
        'status': 'pending',
        'priority_score': priority_score
    }


def generate_demo_tasks(num_tasks: int = 5) -> List[Dict]:
    """
    Generate multiple demo tasks for testing and demonstrations
    
    Args:
        num_tasks: Number of tasks to generate
        
    Returns:
        List[Dict]: List of generated task dictionaries
    """
    
    demo_task_titles = [
        "Prepare presentation slides",
        "Review code implementation",
        "Write project documentation",
        "Conduct team standup meeting",
        "Research new technologies",
        "Update project roadmap",
        "Fix critical bugs",
        "Design system architecture",
        "Create test cases",
        "Analyze performance metrics"
    ]
    
    # Select random titles
    selected_titles = random.sample(
        demo_task_titles,
        min(num_tasks, len(demo_task_titles))
    )
    
    tasks = []
    for title in selected_titles:
        task = generate_mock_task(title)
        tasks.append(task)
    
    return tasks


# Test the functions if run directly
if __name__ == "__main__":
    # Test journal parsing
    print("Testing parse_journal_mock:")
    print("=" * 60)
    
    test_journal = """
    I need to prepare slides for my upcoming presentation.
    I also need to review the code implementation and fix any bugs.
    Finally, I should write comprehensive documentation for the project.
    """
    
    tasks = parse_journal_mock(test_journal)
    print(f"Parsed {len(tasks)} tasks:\n")
    
    for i, task in enumerate(tasks, 1):
        print(f"{i}. {task['title']}")
        print(f"   Duration: {task['estimated_duration']} minutes")
        print(f"   Priority: {task['priority_score']}")
        print(f"   Subtasks: {len(task['subtasks'])}")
        print()
    
    # Test coach messages
    print("\nTesting get_coach_message_mock:")
    print("=" * 60)
    
    message_types = ['session_start', 'halfway', 'break', 'completion']
    context = {'task': 'Write Report', 'duration': 60}
    
    for msg_type in message_types:
        message = get_coach_message_mock(msg_type, context)
        print(f"{msg_type}:")
        print(f"  {message}\n")
    
    # Test demo task generation
    print("\nTesting generate_demo_tasks:")
    print("=" * 60)
    
    demo_tasks = generate_demo_tasks(3)
    for i, task in enumerate(demo_tasks, 1):
        print(f"{i}. {task['title']} ({task['estimated_duration']} min)")
