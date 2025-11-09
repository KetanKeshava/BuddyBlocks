"""
Snowflake Client for Focus Flow
Provides centralized connection management and AI operations
"""

import streamlit as st
import json
import re
from typing import List, Dict, Optional
from datetime import datetime


class SnowflakeClient:
    """
    Centralized Snowflake client for Focus Flow
    Manages connection, AI operations, and database interactions
    """
    
    def __init__(self):
        """Initialize Snowflake client with default state"""
        self.session = None
        self.is_connected = False
    
    def connect(self) -> bool:
        """
        Establish connection to Snowflake using credentials from secrets
        
        Returns:
            bool: True if connection successful, False otherwise
        """
        try:
            from snowflake.snowpark import Session
            
            # Check if secrets exist
            if 'snowflake' not in st.secrets:
                st.error("❌ Snowflake credentials not found in secrets.toml")
                st.info("💡 **Troubleshooting:**\n"
                       "- Check that `.streamlit/secrets.toml` exists\n"
                       "- Ensure it has a `[snowflake]` section\n"
                       "- Verify all required credentials are present")
                return False
            
            # Load configuration from secrets
            config = st.secrets["snowflake"]
            
            # Create connection parameters
            connection_parameters = {
                "account": config['account'],
                "user": config['user'],
                "password": config['password'],
                "role": config['role'],
                "warehouse": config['warehouse'],
                "database": config['database'],
                "schema": config['schema']
            }
            
            # Create Snowpark session
            self.session = Session.builder.configs(connection_parameters).create()
            self.is_connected = True
            
            return True
            
        except ImportError:
            st.error("❌ Snowflake Snowpark library not installed")
            st.info("💡 **To install:** `pip install snowflake-snowpark-python`")
            return False
        except KeyError as e:
            st.error(f"❌ Missing configuration key: {str(e)}")
            st.info("💡 **Check your secrets.toml:**\n"
                   "Required keys: account, user, password, role, warehouse, database, schema")
            return False
        except Exception as e:
            error_msg = str(e).lower()
            st.error(f"❌ Failed to connect to Snowflake: {str(e)}")
            
            # Provide specific troubleshooting tips
            st.info("💡 **Troubleshooting:**")
            if "incorrect username or password" in error_msg or "authentication" in error_msg:
                st.write("- ✓ Check your credentials in `.streamlit/secrets.toml`")
                st.write("- ✓ Verify username and password are correct")
            elif "account" in error_msg or "invalid" in error_msg:
                st.write("- ✓ Verify account identifier format: `orgname-accountname` or `account.region`")
                st.write("- ✓ Example: `abc12345.us-east-1`")
            elif "network" in error_msg or "timeout" in error_msg:
                st.write("- ✓ Check your internet connection")
                st.write("- ✓ Verify your IP is not blocked in Snowflake")
            elif "warehouse" in error_msg:
                st.write("- ✓ Verify the warehouse exists and is running")
                st.write("- ✓ Ensure warehouse is not suspended")
            else:
                st.write("- ✓ Check your credentials in `.streamlit/secrets.toml`")
                st.write("- ✓ Verify your IP is not blocked in Snowflake")
                st.write("- ✓ Ensure warehouse is running")
            
            return False
    
    def _ensure_connected(self):
        """
        Ensure client is connected before operations
        
        Raises:
            Exception: If not connected to Snowflake
        """
        if not self.is_connected or self.session is None:
            raise Exception("Not connected to Snowflake. Call connect() first.")
    
    def _clean_json_response(self, response: str) -> str:
        """
        Clean AI response to extract valid JSON
        
        Args:
            response: Raw AI response string
            
        Returns:
            str: Cleaned JSON string
        """
        # Remove markdown code blocks if present
        if response.startswith("```json"):
            response = response[7:]
        elif response.startswith("```"):
            response = response[3:]
        
        if response.endswith("```"):
            response = response[:-3]
        
        # Strip whitespace
        response = response.strip()
        
        return response
    
    def _escape_sql_string(self, text: str) -> str:
        """
        Escape single quotes in SQL strings
        
        Args:
            text: String to escape
            
        Returns:
            str: Escaped string safe for SQL
        """
        return text.replace("'", "''")
    
    def get_ai_source(self) -> str:
        """
        Get the current AI source being used
        
        Returns:
            str: AI source description
        """
        if self.is_connected:
            return "Snowflake Cortex AI"
        else:
            return "Mock AI (Demo Mode)"
    
    def parse_journal(self, journal_text: str) -> List[Dict]:
        """
        Parse journal entry into structured tasks using Cortex AI
        Falls back to mock AI if Snowflake is unavailable
        
        Args:
            journal_text: Raw journal entry text
            
        Returns:
            List[Dict]: List of parsed task dictionaries
        """
        # Try Snowflake Cortex AI first
        if self.is_connected and self.session is not None:
            try:
                # Build the exact prompt
                prompt = f"""Parse this journal entry into 3-5 actionable tasks.

Return ONLY a valid JSON array with this exact structure:
[
  {{
    "title": "task name",
    "description": "what needs to be done",
    "estimated_duration": 60,
    "subtasks": ["subtask 1", "subtask 2", "subtask 3"]
  }}
]

Rules:
- estimated_duration must be between 30 and 120 minutes
- Include 2-4 subtasks for each task
- Return ONLY the JSON array, no markdown, no explanation

Journal entry: {journal_text}"""
                
                # Escape single quotes for SQL
                prompt_escaped = self._escape_sql_string(prompt)
                
                # Execute Cortex AI query
                query = f"""
                SELECT SNOWFLAKE.CORTEX.COMPLETE(
                    'mistral-large',
                    '{prompt_escaped}'
                ) as response
                """
                
                result = self.session.sql(query).collect()
                
                if not result or not result[0]['RESPONSE']:
                    raise Exception("Empty response from Cortex AI")
                
                raw_response = result[0]['RESPONSE']
                
                # Clean the response
                cleaned_response = self._clean_json_response(raw_response)
                
                # Parse as JSON
                parsed_tasks = json.loads(cleaned_response)
                
                # Validate it's a list
                if not isinstance(parsed_tasks, list):
                    raise Exception("AI response is not a valid JSON array")
                
                return parsed_tasks
                
            except Exception as e:
                # Log the error but continue with fallback
                print(f"Snowflake Cortex AI error: {str(e)}")
                # Fall through to mock AI
        
        # Fallback to mock AI
        try:
            from utils.mock_ai import parse_journal_mock
            
            # Show warning to user that we're using mock AI
            st.warning("⚠️ Using mock AI (Snowflake Cortex unavailable). Results may vary.")
            
            # Call mock parser
            return parse_journal_mock(journal_text)
            
        except Exception as e:
            # If even mock AI fails, raise the error
            raise Exception(f"Failed to parse journal with both Cortex and mock AI: {str(e)}")
    
    def get_coach_message(self, message_type: str, context: Dict = {}) -> str:
        """
        Get AI-generated coaching message for different session events
        Falls back to mock AI if Snowflake is unavailable
        
        Args:
            message_type: Type of message ('session_start', 'halfway', 'break', 'completion')
            context: Dictionary with 'task' and 'duration' keys
            
        Returns:
            str: Coaching message from AI
        """
        # Try Snowflake Cortex AI first
        if self.is_connected and self.session is not None:
            try:
                # Get context values
                task_name = context.get('task', 'this task')
                duration = context.get('duration', 90)
                
                # Define prompts for different message types
                prompts = {
                    'session_start': f"You're starting a {duration}-minute focus session on '{task_name}'. Give an encouraging 15-word message to begin.",
                    'halfway': f"You're halfway through your focus session on '{task_name}'. Give a motivating 15-word check-in message.",
                    'break': f"You just completed a focus session. Suggest a healthy 15-word break activity.",
                    'completion': f"You completed '{task_name}'! Give a celebratory 15-word message recognizing the achievement."
                }
                
                # Get prompt for message type
                prompt = prompts.get(message_type, "Give an encouraging 15-word message about staying focused.")
                
                # Escape single quotes for SQL
                prompt_escaped = self._escape_sql_string(prompt)
                
                # Execute Cortex AI query
                query = f"""
                SELECT SNOWFLAKE.CORTEX.COMPLETE(
                    'mistral-large',
                    '{prompt_escaped}'
                ) as response
                """
                
                result = self.session.sql(query).collect()
                
                if not result or not result[0]['RESPONSE']:
                    raise Exception("Empty response from Cortex AI")
                
                message = result[0]['RESPONSE']
                
                # Clean the message (strip quotes and whitespace)
                message = message.strip().strip('"').strip("'")
                
                return message
                
            except Exception as e:
                # Log error but continue with fallback (silently)
                print(f"Snowflake Cortex AI error: {str(e)}")
                # Fall through to mock AI
        
        # Fallback to mock AI (no warning for coach messages to avoid noise)
        try:
            from utils.mock_ai import get_coach_message_mock
            
            # Call mock coach
            return get_coach_message_mock(message_type, context)
            
        except Exception as e:
            # Return generic fallback message
            fallback_messages = {
                'session_start': "Let's focus and make great progress on this task!",
                'halfway': "You're doing great! Keep up the momentum!",
                'break': "Take a short walk and stretch. You've earned it!",
                'completion': "Excellent work! You've successfully completed this task!"
            }
            return fallback_messages.get(message_type, "Keep up the great work!")
    
    def save_task(self, task: Dict) -> str:
        """
        Save a task to the Snowflake database
        
        Args:
            task: Dictionary containing task data with keys:
                  - task_id: Unique identifier
                  - title: Task title
                  - description: Task description
                  - estimated_duration: Duration in minutes
                  - subtasks: List of subtask strings
                  - status: Task status (pending/in_progress/completed)
                  - priority_score: Priority score (0-100)
                  
        Returns:
            str: Success message
            
        Raises:
            Exception: If not connected or save fails
        """
        self._ensure_connected()
        
        try:
            # Escape string fields
            title = self._escape_sql_string(task.get('title', ''))
            description = self._escape_sql_string(task.get('description', ''))
            status = self._escape_sql_string(task.get('status', 'pending'))
            
            # Convert subtasks list to JSON string
            subtasks_json = json.dumps(task.get('subtasks', []))
            subtasks_json_escaped = self._escape_sql_string(subtasks_json)
            
            # Build INSERT query
            insert_query = f"""
            INSERT INTO tasks (
                task_id,
                title,
                description,
                estimated_duration,
                subtasks,
                status,
                priority_score,
                created_at
            )
            VALUES (
                '{task.get('task_id')}',
                '{title}',
                '{description}',
                {task.get('estimated_duration', 60)},
                PARSE_JSON('{subtasks_json_escaped}'),
                '{status}',
                {task.get('priority_score', 50.0)},
                CURRENT_TIMESTAMP()
            )
            """
            
            # Execute insert
            self.session.sql(insert_query).collect()
            
            return f"✅ Task '{task.get('title', 'Untitled')}' saved successfully"
            
        except Exception as e:
            raise Exception(f"Failed to save task: {str(e)}")
    
    def get_all_tasks(self) -> List[Dict]:
        """
        Retrieve all tasks from the database
        
        Returns:
            List[Dict]: List of task dictionaries
            
        Raises:
            Exception: If not connected or query fails
        """
        self._ensure_connected()
        
        try:
            # Query all tasks
            query = """
            SELECT 
                task_id,
                title,
                description,
                estimated_duration,
                subtasks,
                status,
                priority_score,
                created_at
            FROM tasks
            ORDER BY created_at DESC
            """
            
            result = self.session.sql(query).collect()
            
            # Convert to list of dictionaries
            tasks = []
            for row in result:
                task = {
                    'task_id': row['TASK_ID'],
                    'title': row['TITLE'],
                    'description': row['DESCRIPTION'],
                    'estimated_duration': row['ESTIMATED_DURATION'],
                    'status': row['STATUS'],
                    'priority_score': row['PRIORITY_SCORE'],
                    'created_at': row['CREATED_AT']
                }
                
                # Parse subtasks JSON field
                try:
                    if row['SUBTASKS']:
                        # Handle if subtasks is already parsed or is a string
                        if isinstance(row['SUBTASKS'], str):
                            task['subtasks'] = json.loads(row['SUBTASKS'])
                        else:
                            task['subtasks'] = row['SUBTASKS']
                    else:
                        task['subtasks'] = []
                except (json.JSONDecodeError, TypeError):
                    task['subtasks'] = []
                
                tasks.append(task)
            
            return tasks
            
        except Exception as e:
            raise Exception(f"Failed to retrieve tasks: {str(e)}")
    
    def update_task_status(self, task_id: str, status: str) -> str:
        """
        Update the status of a task
        
        Args:
            task_id: Unique task identifier
            status: New status (pending/in_progress/completed)
            
        Returns:
            str: Success message
            
        Raises:
            Exception: If not connected or update fails
        """
        self._ensure_connected()
        
        try:
            status_escaped = self._escape_sql_string(status)
            
            update_query = f"""
            UPDATE tasks
            SET status = '{status_escaped}',
                updated_at = CURRENT_TIMESTAMP()
            WHERE task_id = '{task_id}'
            """
            
            self.session.sql(update_query).collect()
            
            return f"✅ Task status updated to '{status}'"
            
        except Exception as e:
            raise Exception(f"Failed to update task status: {str(e)}")
    
    def save_work_session(self, session_data: Dict) -> str:
        """
        Save a completed work session to the database
        
        Args:
            session_data: Dictionary containing session data with keys:
                         - session_id: Unique identifier
                         - task_id: Associated task ID
                         - duration_minutes: Session duration
                         - completed: Whether session was completed
                         
        Returns:
            str: Success message
            
        Raises:
            Exception: If not connected or save fails
        """
        self._ensure_connected()
        
        try:
            insert_query = f"""
            INSERT INTO work_sessions (
                session_id,
                task_id,
                start_time,
                duration_minutes,
                completed
            )
            VALUES (
                '{session_data.get('session_id')}',
                '{session_data.get('task_id')}',
                '{session_data.get('start_time', datetime.now().isoformat())}',
                {session_data.get('duration_minutes', 0)},
                {session_data.get('completed', False)}
            )
            """
            
            self.session.sql(insert_query).collect()
            
            return "✅ Work session saved successfully"
            
        except Exception as e:
            raise Exception(f"Failed to save work session: {str(e)}")
    
    def get_session_statistics(self) -> Dict:
        """
        Get statistics about work sessions
        
        Returns:
            Dict: Statistics including total sessions, total time, completion rate
            
        Raises:
            Exception: If not connected or query fails
        """
        self._ensure_connected()
        
        try:
            query = """
            SELECT 
                COUNT(*) as total_sessions,
                SUM(duration_minutes) as total_minutes,
                AVG(CASE WHEN completed THEN 1 ELSE 0 END) as completion_rate,
                COUNT(DISTINCT task_id) as unique_tasks
            FROM work_sessions
            WHERE DATE(start_time) = CURRENT_DATE()
            """
            
            result = self.session.sql(query).collect()
            
            if result:
                row = result[0]
                return {
                    'total_sessions': row['TOTAL_SESSIONS'] or 0,
                    'total_minutes': row['TOTAL_MINUTES'] or 0,
                    'completion_rate': round((row['COMPLETION_RATE'] or 0) * 100, 1),
                    'unique_tasks': row['UNIQUE_TASKS'] or 0
                }
            
            return {
                'total_sessions': 0,
                'total_minutes': 0,
                'completion_rate': 0.0,
                'unique_tasks': 0
            }
            
        except Exception as e:
            raise Exception(f"Failed to get session statistics: {str(e)}")
    
    def close(self):
        """
        Close the Snowflake session and cleanup resources
        """
        try:
            if self.session is not None:
                self.session.close()
            self.is_connected = False
        except Exception as e:
            # Log error but don't raise - cleanup should be graceful
            print(f"Warning: Error closing Snowflake session: {str(e)}")


@st.cache_resource
def get_snowflake_client() -> SnowflakeClient:
    """
    Get or create a cached Snowflake client singleton
    
    Always returns a client instance, even if connection fails.
    The client will automatically use mock AI if Snowflake is unavailable.
    
    Returns:
        SnowflakeClient: Snowflake client instance (may or may not be connected)
    """
    try:
        # Create client instance
        client = SnowflakeClient()
        
        # Attempt connection (but don't fail if it doesn't work)
        connection_success = client.connect()
        
        if connection_success:
            st.success("✅ Connected to Snowflake Cortex AI!", icon="✅")
        else:
            st.info("ℹ️ Running in Demo Mode with Mock AI. Full features require Snowflake connection.", icon="ℹ️")
        
        # Always return the client (it will use mock AI as fallback)
        return client
            
    except Exception as e:
        # Even if initialization fails, return a basic client
        st.warning(f"⚠️ Error initializing client: {str(e)}. Using Mock AI.", icon="⚠️")
        client = SnowflakeClient()
        return client
