"""
Reusable UI Components for Focus Flow
Streamlit components for connection status, badges, and configuration
"""

import streamlit as st
from typing import Optional, Dict
from pathlib import Path


def show_connection_status(client) -> None:
    """
    Display Snowflake connection status with details
    
    Shows a success message if connected to Snowflake with expandable
    connection details, or a warning if running in demo mode.
    
    Args:
        client: SnowflakeClient instance to check connection status
    
    Example:
        >>> from utils.snowflake_client import get_snowflake_client
        >>> client = get_snowflake_client()
        >>> show_connection_status(client)
    """
    
    if client and client.is_connected:
        # Connected to Snowflake
        st.success("🟢 Connected to Snowflake Cortex", icon="✅")
        
        # Show connection details in expander
        with st.expander("🔍 Connection Details"):
            try:
                # Load credentials from secrets
                credentials = st.secrets.get("snowflake", {})
                
                # Create metrics in columns
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("**Account**")
                    st.code(credentials.get('account', 'N/A'), language=None)
                    
                    st.markdown("**Warehouse**")
                    st.code(credentials.get('warehouse', 'N/A'), language=None)
                    
                    st.markdown("**Database**")
                    st.code(credentials.get('database', 'N/A'), language=None)
                
                with col2:
                    st.markdown("**Schema**")
                    st.code(credentials.get('schema', 'N/A'), language=None)
                    
                    st.markdown("**Role**")
                    st.code(credentials.get('role', 'N/A'), language=None)
                    
                    st.markdown("**User**")
                    st.code(credentials.get('user', 'N/A'), language=None)
                
                st.divider()
                
                # AI source indicator
                st.markdown(
                    """
                    <div style='text-align: center; padding: 10px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 10px; color: white;'>
                        <h4 style='margin: 0;'>⚡ Using Snowflake Cortex AI</h4>
                        <p style='margin: 5px 0 0 0; font-size: 14px;'>Real-time AI-powered task parsing and coaching</p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
                
            except Exception as e:
                st.error(f"Error loading connection details: {str(e)}")
    
    else:
        # Not connected - using demo mode
        st.warning("🟡 Running in Demo Mode", icon="⚠️")
        
        # Show information about demo mode
        st.info(
            """
            **Demo Mode Active**
            
            ✅ Task parsing works with mock AI
            ✅ Coach messages work with mock AI
            ⚠️ Database operations require Snowflake connection
            
            Connect to Snowflake for:
            - Real Cortex AI-powered parsing
            - Persistent task storage
            - Advanced analytics
            """,
            icon="ℹ️"
        )
        
        # Show how to connect
        with st.expander("🔌 How to Connect to Snowflake"):
            st.markdown("""
            ### Setup Instructions
            
            1. **Create `.streamlit/secrets.toml` file** (if it doesn't exist)
            
            2. **Add your Snowflake credentials:**
            
            ```toml
            [snowflake]
            account = "your-account.region"
            user = "YOUR_USERNAME"
            password = "YOUR_PASSWORD"
            role = "YOUR_ROLE"
            warehouse = "YOUR_WAREHOUSE"
            database = "YOUR_DATABASE"
            schema = "YOUR_SCHEMA"
            ```
            
            3. **Restart the Streamlit app**
            
            4. **Connection will be established automatically**
            
            ---
            
            📚 **Need help?** Check out the [README.md](README.md) for detailed setup instructions.
            
            🔒 **Security Note:** Never commit `secrets.toml` to version control!
            """)
            
            # Quick link to create config
            if st.button("🛠️ Configure Snowflake Connection", type="secondary", use_container_width=True):
                st.session_state.show_config_form = True


def show_ai_badge(client) -> None:
    """
    Display a badge showing the current AI source
    
    Shows a colorful badge indicating whether using Snowflake Cortex AI
    or Mock AI for demo mode.
    
    Args:
        client: SnowflakeClient instance to check AI source
    
    Example:
        >>> from utils.snowflake_client import get_snowflake_client
        >>> client = get_snowflake_client()
        >>> show_ai_badge(client)
    """
    
    # Get AI source
    ai_source = client.get_ai_source() if client else "Mock AI (Demo Mode)"
    
    if client and client.is_connected:
        # Snowflake Cortex AI badge (purple gradient)
        st.markdown(
            """
            <div style='
                display: inline-block;
                padding: 8px 16px;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                border-radius: 20px;
                color: white;
                font-weight: 600;
                font-size: 14px;
                box-shadow: 0 4px 6px rgba(102, 126, 234, 0.3);
            '>
                ⚡ Powered by Snowflake Cortex AI
            </div>
            """,
            unsafe_allow_html=True
        )
    else:
        # Demo Mode badge (orange)
        st.markdown(
            """
            <div style='
                display: inline-block;
                padding: 8px 16px;
                background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
                border-radius: 20px;
                color: white;
                font-weight: 600;
                font-size: 14px;
                box-shadow: 0 4px 6px rgba(245, 158, 11, 0.3);
            '>
                🎭 Demo Mode
            </div>
            """,
            unsafe_allow_html=True
        )


def show_snowflake_config_form() -> Optional[Dict]:
    """
    Display a configuration form for Snowflake credentials
    
    Shows an interactive form where users can enter their Snowflake
    credentials and test the connection. Provides instructions for
    saving credentials to secrets.toml.
    
    Returns:
        Optional[Dict]: Configuration dictionary if form is submitted, None otherwise
    
    Example:
        >>> config = show_snowflake_config_form()
        >>> if config:
        >>>     print(f"Account: {config['account']}")
    """
    
    with st.expander("🔌 Snowflake Configuration", expanded=True):
        st.markdown("""
        ### Configure Your Snowflake Connection
        
        Enter your Snowflake credentials below. These will need to be saved
        to `.streamlit/secrets.toml` for the connection to persist.
        """)
        
        st.divider()
        
        # Configuration form
        with st.form("snowflake_config_form"):
            st.markdown("#### Connection Details")
            
            # Account and User in columns
            col1, col2 = st.columns(2)
            
            with col1:
                account = st.text_input(
                    "Account Identifier",
                    placeholder="abc12345.us-east-1",
                    help="Format: account.region or orgname-accountname"
                )
                
                user = st.text_input(
                    "Username",
                    placeholder="YOUR_USERNAME",
                    help="Your Snowflake username"
                )
                
                warehouse = st.text_input(
                    "Warehouse",
                    value="FOCUS_FLOW_WH",
                    help="Compute warehouse name"
                )
            
            with col2:
                role = st.text_input(
                    "Role",
                    value="ACCOUNTADMIN",
                    help="Your Snowflake role"
                )
                
                database = st.text_input(
                    "Database",
                    value="FOCUS_FLOW_DB",
                    help="Database name"
                )
                
                schema = st.text_input(
                    "Schema",
                    value="TASK_MANAGEMENT",
                    help="Schema name"
                )
            
            # Password field (full width)
            password = st.text_input(
                "Password",
                type="password",
                placeholder="Enter your password",
                help="Your Snowflake password (will not be displayed)"
            )
            
            st.divider()
            
            # Form buttons
            col1, col2, col3 = st.columns([2, 2, 2])
            
            with col1:
                test_button = st.form_submit_button(
                    "🧪 Test Connection",
                    type="secondary",
                    use_container_width=True
                )
            
            with col2:
                generate_button = st.form_submit_button(
                    "📋 Generate Config",
                    type="primary",
                    use_container_width=True
                )
            
            with col3:
                clear_button = st.form_submit_button(
                    "🗑️ Clear",
                    use_container_width=True
                )
        
        # Create config dictionary
        config = {
            'account': account,
            'user': user,
            'password': password,
            'role': role,
            'warehouse': warehouse,
            'database': database,
            'schema': schema
        }
        
        # Handle form submission
        if test_button:
            # Validate all fields are filled
            if all(config.values()):
                with st.spinner("Testing connection to Snowflake..."):
                    try:
                        from snowflake.snowpark import Session
                        
                        # Attempt connection
                        test_session = Session.builder.configs(config).create()
                        
                        # Test query
                        result = test_session.sql("SELECT CURRENT_VERSION()").collect()
                        version = result[0][0] if result else "Unknown"
                        
                        # Close test session
                        test_session.close()
                        
                        st.success(f"✅ Connection successful! Snowflake version: {version}")
                        
                    except Exception as e:
                        st.error(f"❌ Connection failed: {str(e)}")
                        st.info("💡 **Troubleshooting:**\n"
                               "- Verify your credentials are correct\n"
                               "- Check your account identifier format\n"
                               "- Ensure your IP is not blocked\n"
                               "- Verify the warehouse is running")
            else:
                st.warning("⚠️ Please fill in all fields before testing")
        
        if generate_button:
            # Validate all fields are filled
            if all(config.values()):
                # Generate secrets.toml content
                secrets_content = f"""# Focus Flow - Snowflake Configuration
# NEVER commit this file to version control!

[snowflake]
account = "{account}"
user = "{user}"
password = "{password}"
role = "{role}"
warehouse = "{warehouse}"
database = "{database}"
schema = "{schema}"
"""
                
                st.success("✅ Configuration generated!")
                
                st.markdown("### 📋 Copy this to `.streamlit/secrets.toml`")
                
                st.code(secrets_content, language="toml")
                
                # Instructions
                st.info("""
                **Next Steps:**
                
                1. **Create/Edit** `.streamlit/secrets.toml` in your project root
                2. **Paste** the configuration above into the file
                3. **Save** the file
                4. **Restart** the Streamlit app
                5. **Connection** will be established automatically!
                
                ⚠️ **Important:** Add `secrets.toml` to your `.gitignore` file!
                """)
                
                # Try to write to file (if possible)
                secrets_path = Path(".streamlit/secrets.toml")
                
                if st.button("💾 Save to File (Advanced)", type="secondary"):
                    try:
                        # Create .streamlit directory if it doesn't exist
                        secrets_path.parent.mkdir(parents=True, exist_ok=True)
                        
                        # Write to file
                        with open(secrets_path, 'w') as f:
                            f.write(secrets_content)
                        
                        st.success(f"✅ Configuration saved to `{secrets_path}`!")
                        st.info("🔄 Please restart the app for changes to take effect.")
                        
                    except Exception as e:
                        st.error(f"❌ Error saving file: {str(e)}")
                        st.info("💡 You may need to manually create the file with the configuration above.")
                
                return config
            else:
                st.warning("⚠️ Please fill in all fields before generating config")
        
        if clear_button:
            st.rerun()
        
        return None


def show_feature_comparison() -> None:
    """
    Display a comparison table of features available in different modes
    
    Shows what features work with Snowflake Cortex AI vs Mock AI.
    """
    
    st.markdown("### 📊 Feature Comparison")
    
    # Create comparison table
    comparison_data = {
        "Feature": [
            "Journal Parsing",
            "Task Breakdown",
            "Coach Messages",
            "Task Storage",
            "Analytics",
            "Session Tracking",
            "AI Quality",
            "Response Time"
        ],
        "🟢 Snowflake Cortex": [
            "✅ Advanced AI",
            "✅ Intelligent",
            "✅ Contextual",
            "✅ Persistent",
            "✅ Full",
            "✅ Yes",
            "🌟 Excellent",
            "⚡ Fast"
        ],
        "🟡 Demo Mode": [
            "✅ Mock AI",
            "✅ Basic",
            "✅ Template",
            "❌ In-Memory Only",
            "❌ Limited",
            "❌ No",
            "⭐ Good",
            "⚡ Fast"
        ]
    }
    
    # Display as a formatted table
    st.table(comparison_data)
    
    st.caption("✅ = Available | ❌ = Not Available")


def show_connection_troubleshooting() -> None:
    """
    Display troubleshooting guide for connection issues
    
    Provides common solutions for Snowflake connection problems.
    """
    
    with st.expander("🔧 Connection Troubleshooting"):
        st.markdown("""
        ### Common Connection Issues
        
        #### 1. Authentication Failed
        **Symptoms:** "Incorrect username or password"
        
        **Solutions:**
        - ✓ Double-check username and password in `secrets.toml`
        - ✓ Verify your Snowflake account is active
        - ✓ Ensure you're not locked out due to failed login attempts
        
        ---
        
        #### 2. Invalid Account Identifier
        **Symptoms:** "Invalid account" or "account not found"
        
        **Solutions:**
        - ✓ Verify account identifier format
        - ✓ Old format: `account.region` (e.g., `abc12345.us-east-1`)
        - ✓ New format: `orgname-accountname`
        - ✓ Check the URL when logged into Snowflake
        
        ---
        
        #### 3. Network/Timeout Issues
        **Symptoms:** "Connection timeout" or "Network error"
        
        **Solutions:**
        - ✓ Check your internet connection
        - ✓ Verify firewall settings allow Snowflake connections
        - ✓ Ensure your IP is whitelisted in Snowflake network policies
        - ✓ Try connecting from a different network
        
        ---
        
        #### 4. Warehouse Issues
        **Symptoms:** "Warehouse not found" or "suspended"
        
        **Solutions:**
        - ✓ Verify warehouse name in `secrets.toml`
        - ✓ Ensure warehouse exists in your Snowflake account
        - ✓ Resume warehouse if suspended
        - ✓ Check you have permission to use the warehouse
        
        ---
        
        #### 5. Cortex AI Unavailable
        **Symptoms:** AI queries fail but connection works
        
        **Solutions:**
        - ✓ Verify Cortex AI is available in your region
        - ✓ Check privileges: `GRANT USAGE ON FUNCTION SNOWFLAKE.CORTEX.COMPLETE TO ROLE YOUR_ROLE;`
        - ✓ Contact Snowflake support to enable Cortex AI
        
        ---
        
        ### Still Having Issues?
        
        1. Run the connection test script:
           ```bash
           streamlit run tests/test_snowflake_connection.py
           ```
        
        2. Check Snowflake logs in your account
        
        3. Review the [README.md](README.md) for detailed setup
        
        4. Contact support or open an issue on GitHub
        """)


def show_quick_actions(client) -> None:
    """
    Display quick action buttons based on connection status
    
    Args:
        client: SnowflakeClient instance
    """
    
    st.markdown("### ⚡ Quick Actions")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if not (client and client.is_connected):
            if st.button("🔌 Configure Connection", type="primary", use_container_width=True):
                st.session_state.show_config_form = True
                st.rerun()
    
    with col2:
        if st.button("🧪 Run Tests", type="secondary", use_container_width=True):
            st.info("Run: `streamlit run tests/test_snowflake_connection.py`")
    
    with col3:
        if st.button("📖 View Docs", type="secondary", use_container_width=True):
            st.info("Check out README.md for detailed documentation")


# Example usage in main app
if __name__ == "__main__":
    st.set_page_config(page_title="UI Components Demo", page_icon="🎨", layout="wide")
    
    st.title("🎨 Focus Flow UI Components")
    st.caption("Demonstration of reusable UI components")
    
    # Mock client for demo
    class MockClient:
        def __init__(self, connected=True):
            self.is_connected = connected
        
        def get_ai_source(self):
            return "Snowflake Cortex AI" if self.is_connected else "Mock AI (Demo Mode)"
    
    # Demo connected state
    st.header("Connected State")
    connected_client = MockClient(connected=True)
    show_connection_status(connected_client)
    show_ai_badge(connected_client)
    
    st.divider()
    
    # Demo disconnected state
    st.header("Disconnected State (Demo Mode)")
    disconnected_client = MockClient(connected=False)
    show_connection_status(disconnected_client)
    show_ai_badge(disconnected_client)
    
    st.divider()
    
    # Configuration form
    st.header("Configuration Form")
    config = show_snowflake_config_form()
    
    st.divider()
    
    # Feature comparison
    show_feature_comparison()
    
    st.divider()
    
    # Troubleshooting
    show_connection_troubleshooting()
    
    st.divider()
    
    # Quick actions
    show_quick_actions(disconnected_client)
