"""
Test UI Components
Simple test app to verify all UI components render correctly
"""

import streamlit as st
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.ui_components import (
    show_connection_status,
    show_ai_badge,
    show_snowflake_config_form,
    show_feature_comparison,
    show_connection_troubleshooting,
    show_quick_actions
)


# Mock client for testing
class MockClient:
    """Mock SnowflakeClient for testing UI components"""
    
    def __init__(self, connected=True):
        self.is_connected = connected
        self.session = None if not connected else "mock_session"
    
    def get_ai_source(self):
        """Return AI source based on connection status"""
        return "Snowflake Cortex AI" if self.is_connected else "Mock AI (Demo Mode)"


def main():
    """Main test application"""
    
    st.set_page_config(
        page_title="UI Components Test",
        page_icon="🎨",
        layout="wide"
    )
    
    st.title("🎨 UI Components Test Suite")
    st.caption("Verify all UI components render correctly")
    
    # Sidebar for test controls
    st.sidebar.title("🧪 Test Controls")
    
    connection_state = st.sidebar.radio(
        "Simulate Connection State:",
        ["✅ Connected", "❌ Disconnected"],
        index=0
    )
    
    is_connected = connection_state == "✅ Connected"
    
    st.sidebar.divider()
    
    # Component selection
    st.sidebar.markdown("### Select Components to Test")
    
    test_status = st.sidebar.checkbox("Connection Status", value=True)
    test_badge = st.sidebar.checkbox("AI Badge", value=True)
    test_config = st.sidebar.checkbox("Config Form", value=False)
    test_comparison = st.sidebar.checkbox("Feature Comparison", value=True)
    test_troubleshooting = st.sidebar.checkbox("Troubleshooting", value=False)
    test_quick_actions = st.sidebar.checkbox("Quick Actions", value=True)
    
    st.sidebar.divider()
    st.sidebar.info("💡 Toggle components on/off to test individual elements")
    
    # Create mock client
    client = MockClient(connected=is_connected)
    
    # Main content area
    st.header(f"Current State: {'🟢 Connected' if is_connected else '🔴 Disconnected'}")
    
    st.divider()
    
    # Test 1: Connection Status
    if test_status:
        st.subheader("1️⃣ Connection Status Component")
        show_connection_status(client)
        st.divider()
    
    # Test 2: AI Badge
    if test_badge:
        st.subheader("2️⃣ AI Badge Component")
        col1, col2, col3 = st.columns([1, 1, 2])
        with col1:
            show_ai_badge(client)
        st.divider()
    
    # Test 3: Configuration Form
    if test_config:
        st.subheader("3️⃣ Configuration Form Component")
        config = show_snowflake_config_form()
        if config:
            st.success("✅ Configuration form submitted!")
            st.json(config)
        st.divider()
    
    # Test 4: Feature Comparison
    if test_comparison:
        st.subheader("4️⃣ Feature Comparison Component")
        show_feature_comparison()
        st.divider()
    
    # Test 5: Troubleshooting
    if test_troubleshooting:
        st.subheader("5️⃣ Troubleshooting Component")
        show_connection_troubleshooting()
        st.divider()
    
    # Test 6: Quick Actions
    if test_quick_actions:
        st.subheader("6️⃣ Quick Actions Component")
        show_quick_actions(client)
        st.divider()
    
    # Summary
    st.success("✅ All selected components rendered successfully!")
    
    # Show component stats
    components_tested = sum([
        test_status, test_badge, test_config,
        test_comparison, test_troubleshooting, test_quick_actions
    ])
    
    st.metric(
        label="Components Tested",
        value=f"{components_tested}/6",
        delta=f"{components_tested} active"
    )
    
    # Visual test checklist
    with st.expander("📋 Visual Test Checklist"):
        st.markdown("""
        ### Manual Verification Checklist
        
        #### Connection Status Component
        - [ ] Success message shows when connected
        - [ ] Warning message shows when disconnected
        - [ ] Expander shows connection details (connected mode)
        - [ ] Expander shows setup instructions (disconnected mode)
        - [ ] Purple gradient AI badge displays correctly (connected mode)
        - [ ] Info boxes have proper icons and formatting
        
        #### AI Badge Component
        - [ ] Purple gradient badge for Snowflake Cortex (connected)
        - [ ] Orange gradient badge for Demo Mode (disconnected)
        - [ ] Badges have proper shadows and styling
        - [ ] Text is readable and properly formatted
        
        #### Configuration Form Component
        - [ ] All input fields render correctly
        - [ ] Form has proper layout (2 columns)
        - [ ] Test Connection button works
        - [ ] Generate Config button works
        - [ ] Generated TOML is properly formatted
        - [ ] Instructions are clear and helpful
        - [ ] Error messages display when validation fails
        
        #### Feature Comparison Component
        - [ ] Table displays all features
        - [ ] Columns are properly aligned
        - [ ] Emojis and checkmarks display correctly
        - [ ] Caption is visible
        
        #### Troubleshooting Component
        - [ ] Expander collapses/expands properly
        - [ ] All 5 issues are listed with solutions
        - [ ] Code blocks are formatted correctly
        - [ ] Links are properly formatted
        
        #### Quick Actions Component
        - [ ] Buttons render in 3 columns
        - [ ] Buttons have proper styling
        - [ ] Configure button shows when disconnected
        - [ ] All buttons are clickable
        - [ ] Messages display when buttons are clicked
        
        ---
        
        ### Overall UI Quality
        - [ ] Colors are consistent across components
        - [ ] Spacing and padding are appropriate
        - [ ] Icons and emojis display correctly
        - [ ] Text is readable on all backgrounds
        - [ ] Components are responsive (try different window sizes)
        - [ ] No visual glitches or overlaps
        """)
    
    # Test results
    st.divider()
    
    st.info("""
    **🧪 Testing Tips:**
    
    1. Toggle between Connected/Disconnected states in the sidebar
    2. Enable/disable individual components to test isolation
    3. Try different window sizes to test responsiveness
    4. Fill out the config form and test validation
    5. Expand all expanders to verify content
    6. Click all buttons to verify interactions
    
    **✅ What to Verify:**
    - All colors display correctly (purple for Snowflake, orange for demo)
    - Gradients render smoothly
    - Text is readable on all backgrounds
    - Icons and emojis display properly
    - Buttons and forms work correctly
    - No layout issues or overlaps
    """)


if __name__ == "__main__":
    main()
