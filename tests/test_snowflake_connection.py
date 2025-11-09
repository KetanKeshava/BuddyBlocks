"""
Comprehensive Snowflake Connection Test Script for Focus Flow
Tests connection, Cortex AI, task parsing, and data storage
"""

import streamlit as st
import json
import sys
from datetime import datetime
import uuid


def mask_password(password):
    """Mask password for safe display"""
    if not password or len(password) <= 4:
        return "****"
    return password[:2] + "*" * (len(password) - 4) + password[-2:]


def clean_json_response(response):
    """Clean AI response to extract valid JSON"""
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


def test_snowflake_connection():
    """Main test function"""
    
    print("\n" + "=" * 60)
    print("🧪 FOCUS FLOW - SNOWFLAKE CONNECTION TEST SUITE")
    print("=" * 60 + "\n")
    
    # Track test results
    tests_passed = 0
    tests_failed = 0
    
    # ========================================
    # TEST 1: Load Credentials
    # ========================================
    print("📋 TEST 1: Loading Snowflake Credentials")
    print("-" * 60)
    
    try:
        # Check if running in Streamlit context
        if 'snowflake' not in st.secrets:
            print("❌ ERROR: Snowflake credentials not found in st.secrets")
            print("💡 TIP: Make sure .streamlit/secrets.toml exists with [snowflake] section")
            return
        
        credentials = st.secrets["snowflake"]
        
        # Print credentials (mask password)
        print("✅ Credentials loaded successfully!")
        print(f"   Account:   {credentials['account']}")
        print(f"   User:      {credentials['user']}")
        print(f"   Password:  {mask_password(credentials['password'])}")
        print(f"   Role:      {credentials['role']}")
        print(f"   Warehouse: {credentials['warehouse']}")
        print(f"   Database:  {credentials['database']}")
        print(f"   Schema:    {credentials['schema']}")
        print()
        
        tests_passed += 1
        
    except Exception as e:
        print(f"❌ FAILED: {str(e)}")
        print("💡 TIP: Ensure secrets.toml is properly formatted")
        tests_failed += 1
        return
    
    # ========================================
    # TEST 2: Establish Connection
    # ========================================
    print("🔌 TEST 2: Establishing Snowflake Connection")
    print("-" * 60)
    
    try:
        from snowflake.snowpark import Session
        
        # Create connection parameters
        connection_parameters = {
            "account": credentials['account'],
            "user": credentials['user'],
            "password": credentials['password'],
            "role": credentials['role'],
            "warehouse": credentials['warehouse'],
            "database": credentials['database'],
            "schema": credentials['schema']
        }
        
        print("🔌 Attempting to connect to Snowflake...")
        session = Session.builder.configs(connection_parameters).create()
        
        print("✅ Connection established successfully!")
        print(f"   Session ID: {session.get_current_account()}")
        print()
        
        tests_passed += 1
        
    except ImportError as e:
        print(f"❌ FAILED: Snowflake Snowpark library not installed")
        print(f"💡 TIP: Run 'pip install snowflake-snowpark-python'")
        tests_failed += 1
        return
    except Exception as e:
        print(f"❌ FAILED: {str(e)}")
        print("💡 TIP: Check your credentials and network connectivity")
        print("💡 TIP: Verify warehouse is not suspended")
        tests_failed += 1
        return
    
    # ========================================
    # TEST 3: Verify Snowflake Version
    # ========================================
    print("🔍 TEST 3: Verifying Snowflake Version")
    print("-" * 60)
    
    try:
        print("🔍 Running: SELECT CURRENT_VERSION()")
        
        version_df = session.sql("SELECT CURRENT_VERSION() as version").collect()
        version = version_df[0]['VERSION']
        
        print(f"✅ Snowflake version: {version}")
        print()
        
        tests_passed += 1
        
    except Exception as e:
        print(f"❌ FAILED: {str(e)}")
        tests_failed += 1
    
    # ========================================
    # TEST 4: Test Cortex AI Availability
    # ========================================
    print("🤖 TEST 4: Testing Cortex AI Availability")
    print("-" * 60)
    
    try:
        print("🤖 Testing Cortex AI with simple greeting...")
        
        test_query = """
        SELECT SNOWFLAKE.CORTEX.COMPLETE(
            'mistral-large',
            'Say hello in an encouraging way'
        ) as response
        """
        
        response_df = session.sql(test_query).collect()
        ai_response = response_df[0]['RESPONSE']
        
        print("✅ Cortex AI is available and working!")
        print(f"   AI Response: {ai_response}")
        print()
        
        tests_passed += 1
        
    except Exception as e:
        print(f"❌ FAILED: {str(e)}")
        print("💡 TIP: Cortex AI may not be available in your region")
        print("💡 TIP: Ensure you have USAGE privileges on CORTEX functions")
        print("💡 TIP: Run: GRANT USAGE ON FUNCTION SNOWFLAKE.CORTEX.COMPLETE TO ROLE YOUR_ROLE;")
        tests_failed += 1
    
    # ========================================
    # TEST 5: Test Task Parsing with AI
    # ========================================
    print("📝 TEST 5: Testing AI Task Parsing")
    print("-" * 60)
    
    try:
        journal_text = "I need to prepare for my Microsoft interview. This includes reviewing system design, practicing coding problems, and researching the company culture."
        
        print(f"📝 Journal Entry: {journal_text}")
        print()
        print("🤖 Parsing with Cortex AI...")
        
        # Create the AI parsing prompt
        prompt = f"""Parse this journal entry into 3 tasks. Return ONLY valid JSON array with fields: title, description, estimated_duration (30-120 minutes), subtasks (2-3 items).
Journal: {journal_text}
Return ONLY the JSON array, no markdown, no explanation."""
        
        # Escape single quotes in prompt
        prompt_escaped = prompt.replace("'", "''")
        
        parse_query = f"""
        SELECT SNOWFLAKE.CORTEX.COMPLETE(
            'mistral-large',
            '{prompt_escaped}'
        ) as response
        """
        
        response_df = session.sql(parse_query).collect()
        raw_response = response_df[0]['RESPONSE']
        
        # Clean the response
        cleaned_response = clean_json_response(raw_response)
        
        # Parse as JSON
        parsed_tasks = json.loads(cleaned_response)
        
        print(f"✅ Successfully parsed {len(parsed_tasks)} tasks!")
        print()
        
        # Display each task
        for i, task in enumerate(parsed_tasks, 1):
            print(f"   Task {i}:")
            print(f"      Title:    {task.get('title', 'N/A')}")
            print(f"      Duration: {task.get('estimated_duration', 'N/A')} minutes")
            print(f"      Subtasks: {len(task.get('subtasks', []))} items")
            
            # Display subtasks
            for j, subtask in enumerate(task.get('subtasks', []), 1):
                print(f"         {j}. {subtask}")
            print()
        
        tests_passed += 1
        
    except json.JSONDecodeError as e:
        print(f"❌ FAILED: Invalid JSON response from AI")
        print(f"   Raw response: {raw_response[:200]}...")
        print(f"   Error: {str(e)}")
        print("💡 TIP: AI response format may vary, adjust cleaning logic")
        tests_failed += 1
    except Exception as e:
        print(f"❌ FAILED: {str(e)}")
        tests_failed += 1
    
    # ========================================
    # TEST 6: Test Database Table Operations
    # ========================================
    print("💾 TEST 6: Testing Database Table Operations")
    print("-" * 60)
    
    try:
        # First, create the tasks table if it doesn't exist
        print("💾 Creating tasks table (if not exists)...")
        
        create_table_sql = """
        CREATE TABLE IF NOT EXISTS tasks (
            task_id VARCHAR(36) PRIMARY KEY,
            title VARCHAR(500),
            description TEXT,
            estimated_duration INTEGER,
            status VARCHAR(50),
            priority_score FLOAT,
            created_at TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP()
        )
        """
        
        session.sql(create_table_sql).collect()
        print("✅ Tasks table ready")
        print()
        
        # Insert a test task
        print("💾 Inserting test task...")
        
        test_task_id = str(uuid.uuid4())
        test_task = {
            'task_id': test_task_id,
            'title': 'Test Task - Connection Verification',
            'description': 'This is a test task created by the connection test script',
            'estimated_duration': 30,
            'status': 'pending',
            'priority_score': 75.0
        }
        
        insert_sql = f"""
        INSERT INTO tasks (task_id, title, description, estimated_duration, status, priority_score)
        VALUES (
            '{test_task['task_id']}',
            '{test_task['title']}',
            '{test_task['description']}',
            {test_task['estimated_duration']},
            '{test_task['status']}',
            {test_task['priority_score']}
        )
        """
        
        session.sql(insert_sql).collect()
        print(f"✅ Test task inserted with ID: {test_task_id}")
        print()
        
        # Verify the insert
        print("💾 Verifying task count...")
        
        count_df = session.sql("SELECT COUNT(*) as task_count FROM tasks").collect()
        task_count = count_df[0]['TASK_COUNT']
        
        print(f"✅ Total tasks in database: {task_count}")
        print()
        
        # Query the test task
        print("💾 Retrieving test task...")
        
        query_sql = f"SELECT * FROM tasks WHERE task_id = '{test_task_id}'"
        task_df = session.sql(query_sql).collect()
        
        if len(task_df) > 0:
            retrieved_task = task_df[0]
            print("✅ Test task retrieved successfully!")
            print(f"   Title:    {retrieved_task['TITLE']}")
            print(f"   Status:   {retrieved_task['STATUS']}")
            print(f"   Duration: {retrieved_task['ESTIMATED_DURATION']} minutes")
            print(f"   Priority: {retrieved_task['PRIORITY_SCORE']}")
            print()
        else:
            raise Exception("Test task not found after insert")
        
        # Clean up test task
        print("💾 Cleaning up test task...")
        delete_sql = f"DELETE FROM tasks WHERE task_id = '{test_task_id}'"
        session.sql(delete_sql).collect()
        print("✅ Test task deleted")
        print()
        
        tests_passed += 1
        
    except Exception as e:
        print(f"❌ FAILED: {str(e)}")
        print("💡 TIP: Ensure you have CREATE TABLE and INSERT privileges")
        print("💡 TIP: Verify the schema exists and is accessible")
        tests_failed += 1
    
    # ========================================
    # TEST 7: Test Work Sessions Table
    # ========================================
    print("⏱️ TEST 7: Testing Work Sessions Table")
    print("-" * 60)
    
    try:
        print("⏱️ Creating work_sessions table (if not exists)...")
        
        create_sessions_sql = """
        CREATE TABLE IF NOT EXISTS work_sessions (
            session_id VARCHAR(36) PRIMARY KEY,
            task_id VARCHAR(36),
            start_time TIMESTAMP_NTZ,
            duration_minutes INTEGER,
            completed BOOLEAN,
            created_at TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP()
        )
        """
        
        session.sql(create_sessions_sql).collect()
        print("✅ Work sessions table ready")
        print()
        
        # Insert test session
        test_session_id = str(uuid.uuid4())
        test_task_id = str(uuid.uuid4())
        
        insert_session_sql = f"""
        INSERT INTO work_sessions (session_id, task_id, start_time, duration_minutes, completed)
        VALUES (
            '{test_session_id}',
            '{test_task_id}',
            CURRENT_TIMESTAMP(),
            45,
            TRUE
        )
        """
        
        session.sql(insert_session_sql).collect()
        print(f"✅ Test session inserted with ID: {test_session_id}")
        print()
        
        # Query sessions count
        session_count_df = session.sql("SELECT COUNT(*) as session_count FROM work_sessions").collect()
        session_count = session_count_df[0]['SESSION_COUNT']
        
        print(f"✅ Total work sessions in database: {session_count}")
        print()
        
        # Clean up
        delete_session_sql = f"DELETE FROM work_sessions WHERE session_id = '{test_session_id}'"
        session.sql(delete_session_sql).collect()
        print("✅ Test session deleted")
        print()
        
        tests_passed += 1
        
    except Exception as e:
        print(f"❌ FAILED: {str(e)}")
        tests_failed += 1
    
    # ========================================
    # Close Session
    # ========================================
    try:
        session.close()
        print("🔌 Session closed successfully")
        print()
    except Exception as e:
        print(f"⚠️  Warning: Could not close session: {str(e)}")
        print()
    
    # ========================================
    # Final Summary
    # ========================================
    print("=" * 60)
    print("📊 TEST SUMMARY")
    print("=" * 60)
    print(f"✅ Tests Passed: {tests_passed}")
    print(f"❌ Tests Failed: {tests_failed}")
    print(f"📈 Success Rate: {(tests_passed / (tests_passed + tests_failed) * 100):.1f}%")
    print()
    
    if tests_failed == 0:
        print("🎉 ALL TESTS PASSED! 🎉")
        print()
        print("✅ Your Snowflake connection is fully configured")
        print("✅ Cortex AI is available and working")
        print("✅ Database tables are ready")
        print("✅ You're ready to run Focus Flow!")
        print()
    else:
        print("⚠️  Some tests failed. Please review the errors above.")
        print()
        print("📚 Common Troubleshooting Tips:")
        print("   1. Verify all credentials in .streamlit/secrets.toml")
        print("   2. Ensure warehouse is not suspended")
        print("   3. Check that Cortex AI is available in your region")
        print("   4. Verify you have necessary privileges (CREATE, INSERT, SELECT)")
        print("   5. Confirm network connectivity to Snowflake")
        print()
    
    print("=" * 60)
    print()


def main():
    """Entry point for the test script"""
    
    # Check if running in Streamlit context
    try:
        # Try to access st.secrets to check if in Streamlit context
        _ = st.secrets
        test_snowflake_connection()
    except AttributeError:
        print("❌ ERROR: This script must be run in a Streamlit context")
        print()
        print("💡 How to run this script:")
        print("   1. Make sure .streamlit/secrets.toml exists with your credentials")
        print("   2. Run: streamlit run tests/test_snowflake_connection.py")
        print()
        sys.exit(1)


if __name__ == "__main__":
    main()
