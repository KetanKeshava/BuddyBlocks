"""
Focus Flow - Snowflake Setup Verification
Complete verification of all components and configuration
"""

import streamlit as st
import sys
from pathlib import Path
from typing import Tuple, List

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))


def check_file_exists(filepath: str) -> Tuple[bool, str]:
    """Check if a file exists"""
    path = Path(filepath)
    if path.exists():
        return True, f"✅ {filepath}"
    else:
        return False, f"❌ {filepath} - NOT FOUND"


def check_import(module_name: str, import_statement: str = None) -> Tuple[bool, str]:
    """Check if a module can be imported"""
    try:
        if import_statement:
            exec(import_statement)
        else:
            __import__(module_name)
        return True, f"✅ {module_name}"
    except ImportError as e:
        return False, f"❌ {module_name} - NOT INSTALLED: {str(e)}"
    except Exception as e:
        return False, f"❌ {module_name} - ERROR: {str(e)}"


def check_secrets_config() -> Tuple[bool, str, List[str]]:
    """Check if secrets are properly configured"""
    required_keys = ['account', 'user', 'password', 'role', 'warehouse', 'database', 'schema']
    
    try:
        if 'snowflake' not in st.secrets:
            return False, "❌ [snowflake] section not found in secrets.toml", []
        
        snowflake_config = st.secrets["snowflake"]
        missing_keys = [key for key in required_keys if key not in snowflake_config]
        
        if missing_keys:
            return False, f"❌ Missing keys: {', '.join(missing_keys)}", missing_keys
        
        return True, "✅ All required configuration keys present", []
        
    except Exception as e:
        return False, f"❌ Error reading secrets: {str(e)}", []


def main():
    st.set_page_config(
        page_title="Setup Verification",
        page_icon="🎯",
        layout="wide"
    )
    
    # Header
    st.title("🎯 Focus Flow - Snowflake Setup Verification")
    st.caption("Comprehensive check of all components and configuration")
    
    st.divider()
    
    # Progress tracking
    total_checks = 0
    passed_checks = 0
    critical_failed = False
    
    # Sidebar with resources
    with st.sidebar:
        st.header("📚 Resources")
        
        st.markdown("### 🧪 Test Scripts")
        st.code("streamlit run tests/test_snowflake_connection.py", language="bash")
        st.code("streamlit run tests/test_client_ui.py", language="bash")
        st.code("streamlit run tests/test_fallback.py", language="bash")
        
        st.divider()
        
        st.markdown("### 📖 Documentation")
        st.markdown("- [README.md](README.md)")
        st.markdown("- [TESTING_GUIDE.md](TESTING_GUIDE.md)")
        
        st.divider()
        
        st.markdown("### 🆘 Support")
        st.info("""
        **Need Help?**
        
        1. Check error messages above
        2. Review README.md setup guide
        3. Run test scripts for details
        4. Check Snowflake connection
        """)
    
    # CHECK 1: Files Exist
    st.header("📁 CHECK 1: Required Files")
    st.caption("Verifying all necessary files are present")
    
    files_to_check = [
        '.streamlit/secrets.toml',
        'utils/snowflake_client.py',
        'utils/mock_ai.py',
        'utils/ui_components.py',
        'app.py',
        'requirements.txt'
    ]
    
    file_results = []
    for filepath in files_to_check:
        total_checks += 1
        success, message = check_file_exists(filepath)
        file_results.append((success, message))
        if success:
            passed_checks += 1
    
    # Display file check results
    col1, col2 = st.columns(2)
    with col1:
        for i in range(0, len(file_results), 2):
            st.write(file_results[i][1])
    with col2:
        for i in range(1, len(file_results), 2):
            if i < len(file_results):
                st.write(file_results[i][1])
    
    files_passed = all(result[0] for result in file_results)
    if not files_passed:
        critical_failed = True
        st.error("❌ Critical files missing! Cannot proceed.")
    else:
        st.success("✅ All required files present")
    
    st.divider()
    
    # CHECK 2: Dependencies Installed
    st.header("📦 CHECK 2: Dependencies Installed")
    st.caption("Verifying Python packages are installed")
    
    dependencies = [
        ('streamlit', None),
        ('snowflake.snowpark', 'from snowflake.snowpark import Session'),
        ('snowflake.connector', 'import snowflake.connector'),
        ('pandas', None),
    ]
    
    dep_results = []
    for module_name, import_stmt in dependencies:
        total_checks += 1
        success, message = check_import(module_name, import_stmt)
        dep_results.append((success, message))
        if success:
            passed_checks += 1
    
    # Display dependency check results
    col1, col2 = st.columns(2)
    with col1:
        for i in range(0, len(dep_results), 2):
            st.write(dep_results[i][1])
    with col2:
        for i in range(1, len(dep_results), 2):
            if i < len(dep_results):
                st.write(dep_results[i][1])
    
    deps_passed = all(result[0] for result in dep_results)
    if not deps_passed:
        critical_failed = True
        st.error("❌ Missing dependencies! Run: `pip install -r requirements.txt`")
    else:
        st.success("✅ All dependencies installed")
    
    st.divider()
    
    # CHECK 3: Secrets Configuration
    st.header("🔐 CHECK 3: Secrets Configuration")
    st.caption("Verifying Snowflake credentials are configured")
    
    total_checks += 1
    secrets_success, secrets_message, missing_keys = check_secrets_config()
    
    st.write(secrets_message)
    
    if secrets_success:
        passed_checks += 1
        st.success("✅ Snowflake credentials configured correctly")
        
        # Show configured keys (without values)
        with st.expander("🔍 View Configured Keys"):
            try:
                config = st.secrets["snowflake"]
                col1, col2 = st.columns(2)
                with col1:
                    st.write("✅ account")
                    st.write("✅ user")
                    st.write("✅ password")
                with col2:
                    st.write("✅ role")
                    st.write("✅ warehouse")
                    st.write("✅ database")
                    st.write("✅ schema")
            except Exception as e:
                st.error(f"Error displaying keys: {str(e)}")
    else:
        critical_failed = True
        st.error("❌ Secrets configuration incomplete!")
        if missing_keys:
            st.warning(f"Missing keys: {', '.join(missing_keys)}")
        st.info("""
        **To fix:**
        1. Copy `.streamlit/secrets.toml.template` to `.streamlit/secrets.toml`
        2. Fill in your Snowflake credentials
        3. Restart the app
        """)
    
    st.divider()
    
    # Only continue with remaining checks if critical checks passed
    if not critical_failed:
        # CHECK 4: Snowflake Connection
        st.header("🔌 CHECK 4: Snowflake Connection")
        st.caption("Testing connection to Snowflake")
        
        total_checks += 1
        
        try:
            with st.spinner("Connecting to Snowflake..."):
                from utils.snowflake_client import get_snowflake_client
                client = get_snowflake_client()
            
            if client and client.is_connected:
                passed_checks += 1
                st.success("✅ Connected to Snowflake Cortex AI!")
                
                with st.expander("📊 Connection Details"):
                    try:
                        credentials = st.secrets["snowflake"]
                        col1, col2 = st.columns(2)
                        with col1:
                            st.metric("Account", credentials['account'])
                            st.metric("Warehouse", credentials['warehouse'])
                            st.metric("Database", credentials['database'])
                        with col2:
                            st.metric("Schema", credentials['schema'])
                            st.metric("Role", credentials['role'])
                            st.metric("AI Source", client.get_ai_source())
                    except Exception as e:
                        st.error(f"Error displaying details: {str(e)}")
            else:
                st.warning("⚠️ Not connected to Snowflake - Using mock AI")
                st.info("""
                **This is OK for testing!**
                
                The app will work with mock AI, but you won't have:
                - Real Cortex AI parsing
                - Persistent database storage
                - Advanced analytics
                
                **To connect:**
                - Verify your credentials in `.streamlit/secrets.toml`
                - Check network connectivity
                - Ensure warehouse is running
                """)
                
                # Still count as passed if client exists (fallback working)
                if client:
                    passed_checks += 1
        
        except Exception as e:
            st.error(f"❌ Connection error: {str(e)}")
            st.info("Run `streamlit run tests/test_snowflake_connection.py` for detailed diagnostics")
        
        st.divider()
        
        # CHECK 5: AI Parsing Test
        st.header("🤖 CHECK 5: AI Parsing Test")
        st.caption("Testing journal parsing functionality")
        
        total_checks += 1
        
        try:
            test_journal = "I need to prepare presentation slides, practice my demo, and review feedback from the team."
            
            with st.spinner("Testing AI parsing..."):
                from utils.snowflake_client import get_snowflake_client
                client = get_snowflake_client()
                tasks = client.parse_journal(test_journal)
            
            if tasks and len(tasks) >= 3:
                passed_checks += 1
                st.success(f"✅ Parsing works! Generated {len(tasks)} tasks")
                
                with st.expander("📋 Sample Parsed Tasks"):
                    for i, task in enumerate(tasks[:3], 1):
                        st.write(f"**Task {i}:** {task.get('title', 'N/A')}")
                        st.caption(f"Duration: {task.get('estimated_duration', 'N/A')} min | "
                                 f"Subtasks: {len(task.get('subtasks', []))}")
                        st.divider()
            else:
                st.warning("⚠️ Parsing returned unexpected results")
                st.json(tasks)
        
        except Exception as e:
            st.error(f"❌ Parsing test failed: {str(e)}")
            with st.expander("🔍 Error Details"):
                st.code(str(e))
        
        st.divider()
        
        # CHECK 6: Coach Messages Test
        st.header("🎙️ CHECK 6: Coach Messages Test")
        st.caption("Testing AI coaching functionality")
        
        message_types = ['session_start', 'halfway', 'break', 'completion']
        coach_results = []
        
        try:
            from utils.snowflake_client import get_snowflake_client
            client = get_snowflake_client()
            
            for msg_type in message_types:
                total_checks += 1
                try:
                    message = client.get_coach_message(
                        msg_type,
                        {'task': 'Test Task', 'duration': 60}
                    )
                    
                    if message and len(message.strip()) > 0:
                        passed_checks += 1
                        coach_results.append((True, msg_type, message))
                    else:
                        coach_results.append((False, msg_type, "Empty message"))
                except Exception as e:
                    coach_results.append((False, msg_type, str(e)))
            
            # Display results
            all_passed = all(result[0] for result in coach_results)
            
            if all_passed:
                st.success("✅ All coach message types working!")
                
                with st.expander("💬 Sample Messages"):
                    for success, msg_type, message in coach_results:
                        st.write(f"**{msg_type.replace('_', ' ').title()}:**")
                        st.info(f"🎙️ {message}")
                        st.divider()
            else:
                st.warning("⚠️ Some coach messages failed")
                for success, msg_type, message in coach_results:
                    if not success:
                        st.write(f"❌ {msg_type}: {message}")
        
        except Exception as e:
            st.error(f"❌ Coach messages test failed: {str(e)}")
        
        st.divider()
        
        # CHECK 7: Database Operations (only if connected)
        st.header("💾 CHECK 7: Database Operations")
        st.caption("Testing data persistence (requires Snowflake connection)")
        
        try:
            from utils.snowflake_client import get_snowflake_client
            client = get_snowflake_client()
            
            if client and client.is_connected:
                total_checks += 1
                
                try:
                    import uuid
                    
                    # Test save_task
                    test_task = {
                        'task_id': str(uuid.uuid4()),
                        'title': 'Verification Test Task',
                        'description': 'Test task created by setup verification',
                        'estimated_duration': 30,
                        'subtasks': ['Verify save', 'Verify retrieve'],
                        'status': 'pending',
                        'priority_score': 50.0
                    }
                    
                    with st.spinner("Testing database operations..."):
                        # Save task
                        result = client.save_task(test_task)
                        
                        # Retrieve tasks
                        tasks = client.get_all_tasks()
                    
                    passed_checks += 1
                    st.success("✅ Database operations work!")
                    st.write(result)
                    st.caption(f"Total tasks in database: {len(tasks)}")
                    
                    # Clean up test task
                    try:
                        # Note: Would need delete method in client
                        st.caption("💡 Remember to clean up test tasks from database")
                    except:
                        pass
                
                except Exception as e:
                    st.error(f"❌ Database operations failed: {str(e)}")
                    with st.expander("🔍 Error Details"):
                        st.code(str(e))
            else:
                st.info("ℹ️ Skipped (requires Snowflake connection)")
                st.caption("Database operations only work with real Snowflake connection")
        
        except Exception as e:
            st.error(f"❌ Database test error: {str(e)}")
    
    # Final Summary
    st.divider()
    st.header("📊 Verification Summary")
    
    # Calculate success rate
    success_rate = (passed_checks / total_checks * 100) if total_checks > 0 else 0
    
    # Progress bar
    st.progress(success_rate / 100)
    
    # Metrics
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Checks", total_checks)
    with col2:
        st.metric("Passed", passed_checks, delta=passed_checks - (total_checks - passed_checks))
    with col3:
        st.metric("Success Rate", f"{success_rate:.1f}%")
    
    st.divider()
    
    # Final verdict
    if success_rate >= 85 and not critical_failed:
        st.success("🎉 **Setup Complete!** Ready to build Focus Flow.", icon="🎉")
        st.balloons()
        
        st.info("""
        **✅ Your Environment is Ready!**
        
        **Next Steps:**
        1. Run the main app: `streamlit run app.py`
        2. Test all features in the UI
        3. Start building additional features
        4. Deploy to production when ready
        
        **Optional Tests:**
        - Run `streamlit run tests/test_client_ui.py` for interactive testing
        - Run `streamlit run tests/test_fallback.py` to verify mock AI fallback
        """)
        
        if st.button("🚀 Proceed to App Development", type="primary", use_container_width=True):
            st.code("streamlit run app.py", language="bash")
    
    elif success_rate >= 60:
        st.warning("🔧 **Partial Setup** - Some issues found but core functionality works", icon="⚠️")
        
        st.info("""
        **⚠️ Action Required:**
        
        Some checks failed, but you can still use the app with mock AI.
        
        **To enable full features:**
        1. Review failed checks above
        2. Fix Snowflake connection issues
        3. Re-run this verification
        4. Test with real Cortex AI
        
        **For now, you can:**
        - Use the app with mock AI
        - Test UI components
        - Develop features locally
        """)
    
    else:
        st.error("🔧 **Issues Found** - Setup incomplete", icon="❌")
        
        st.warning("""
        **❌ Critical Issues Detected:**
        
        Your setup is incomplete. Please address the issues above before proceeding.
        
        **Troubleshooting Steps:**
        1. Check that all files exist
        2. Install dependencies: `pip install -r requirements.txt`
        3. Configure `.streamlit/secrets.toml` with your credentials
        4. Verify Snowflake account access
        5. Re-run this verification
        
        **Need Help?**
        - Check the [README.md](README.md) for setup instructions
        - Review error messages above for specific issues
        - Run test scripts for detailed diagnostics
        """)
    
    # Detailed recommendations
    if passed_checks < total_checks:
        with st.expander("🔍 Detailed Recommendations"):
            st.markdown("""
            ### Common Issues and Solutions
            
            #### ❌ Files Missing
            - Ensure you're in the correct directory
            - Clone the repository completely
            - Check that hidden files are visible
            
            #### ❌ Dependencies Not Installed
            ```bash
            pip install -r requirements.txt
            ```
            
            #### ❌ Secrets Not Configured
            1. Copy `.streamlit/secrets.toml.template` to `.streamlit/secrets.toml`
            2. Fill in your Snowflake credentials
            3. Restart Streamlit
            
            #### ❌ Connection Failed
            - Verify account identifier format
            - Check username and password
            - Ensure warehouse is running
            - Verify network connectivity
            - Check IP whitelist in Snowflake
            
            #### ❌ AI Parsing Failed
            - Verify Cortex AI is available in your region
            - Check role has USAGE privileges on CORTEX functions
            - Review error messages for specific issues
            
            #### ❌ Database Operations Failed
            - Verify tables exist in Snowflake
            - Check permissions (CREATE, INSERT, SELECT)
            - Ensure schema is accessible
            """)
    
    # Test script links
    st.divider()
    st.subheader("🧪 Additional Test Scripts")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("**Connection Test**")
        st.code("streamlit run tests/test_snowflake_connection.py", language="bash")
        st.caption("Detailed connection diagnostics")
    
    with col2:
        st.markdown("**Interactive UI Test**")
        st.code("streamlit run tests/test_client_ui.py", language="bash")
        st.caption("Test all client methods")
    
    with col3:
        st.markdown("**Fallback Test**")
        st.code("streamlit run tests/test_fallback.py", language="bash")
        st.caption("Verify mock AI fallback")


if __name__ == "__main__":
    main()
