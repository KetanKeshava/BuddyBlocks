"""
UI Components Test App
Demonstrates all reusable UI components from utils/ui_components.py
"""

import streamlit as st
import sys
from pathlib import Path

# Add parent directory to path to import utils
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
    """Mock Snowflake client for testing UI components"""
    
    def __init__(self, connected=True):
        self.is_connected = connected
        self.session = None if not connected else "mock_session"
    
    def get_ai_source(self):
        return "Snowflake Cortex AI" if self.is_connected else "Mock AI (Demo Mode)"


def main():
    st.set_page_config(
        page_title="UI Components Test",
        page_icon="🎨",
        layout="wide"
    )
    
    st.title("🎨 Focus Flow UI Components Test")
    st.caption("Visual test of all reusable UI components")
    
    # Toggle to switch between connected/disconnected states
    st.sidebar.header("⚙️ Test Settings")
    is_connected = st.sidebar.toggle(
        "Simulate Snowflake Connection",
        value=False,
        help="Toggle to test connected vs disconnected states"
    )
    
    # Create mock client based on toggle
    client = MockClient(connected=is_connected)
    
    st.sidebar.divider()
    st.sidebar.info(f"""
    **Current State:**
    - Connected: {is_connected}
    - AI Source: {client.get_ai_source()}
    """)
    
    st.divider()
    
    # Test 1: Connection Status
    st.header("1️⃣ Connection Status Component")
    st.caption("`show_connection_status(client)`")
    
    show_connection_status(client)
    
    st.divider()
    
    # Test 2: AI Badge
    st.header("2️⃣ AI Badge Component")
    st.caption("`show_ai_badge(client)`")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        show_ai_badge(client)
    
    st.divider()
    
    # Test 3: Feature Comparison
    st.header("3️⃣ Feature Comparison Table")
    st.caption("`show_feature_comparison()`")
    
    show_feature_comparison()
    
    st.divider()
    
    # Test 4: Connection Troubleshooting
    st.header("4️⃣ Troubleshooting Guide")
    st.caption("`show_connection_troubleshooting()`")
    
    show_connection_troubleshooting()
    
    st.divider()
    
    # Test 5: Quick Actions
    st.header("5️⃣ Quick Actions Buttons")
    st.caption("`show_quick_actions(client)`")
    
    show_quick_actions(client)
    
    st.divider()
    
    # Test 6: Configuration Form (optional - can be heavy)
    st.header("6️⃣ Configuration Form")
    st.caption("`show_snowflake_config_form()`")
    
    show_config = st.checkbox("Show Configuration Form", value=False)
    
    if show_config:
        config = show_snowflake_config_form()
        if config:
            st.success("Configuration returned!")
            st.json(config)
    else:
        st.info("👆 Check the box above to test the configuration form")
    
    st.divider()
    
    # Summary
    st.success("✅ All UI components rendered successfully!")
    
    st.info("""
    **Test Instructions:**
    
    1. ✅ Use the sidebar toggle to switch between connected/disconnected states
    2. ✅ Verify all components render correctly
    3. ✅ Check that badges show correct colors and text
    4. ✅ Test expandable sections (Connection Details, Troubleshooting, etc.)
    5. ✅ Click buttons to verify they work (some will show info messages)
    6. ✅ Enable configuration form and test the form inputs
    
    **Expected Results:**
    - Connected state: Green success, purple badge
    - Disconnected state: Yellow warning, orange badge
    - All text should be readable and well-formatted
    - Gradients should look smooth
    - Tables should be properly aligned
    """)


if __name__ == "__main__":
    main()
