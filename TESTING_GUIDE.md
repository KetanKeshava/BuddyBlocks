# 🧪 Snowflake Client Test Suite - Testing Checklist

## 🌐 App Access
- **URL:** http://localhost:8502
- **Status:** ✅ Running

## 📋 Testing Checklist

### ✅ **Connection Verification**
- [ ] App loads without errors
- [ ] Green success message: "✅ Connected to Snowflake Cortex!"
- [ ] Connection details expandable shows:
  - Account: onc84192.us-east-1
  - Warehouse: FOCUS_FLOW_WH
  - Database: FOCUS_FLOW_DB
  - Schema: TASK_MANAGEMENT
  - Role: ACCOUNTADMIN

---

### 📝 **Test 1: Journal Parsing**

**Test Case 1.1: Default Journal Entry**
- [ ] Default text appears: "I need to prepare slides for my presentation, practice my demo, and send follow-up emails to attendees"
- [ ] Click "🤖 Parse with AI" button
- [ ] Spinner shows "⏳ Parsing with Snowflake Cortex AI..."
- [ ] Success message shows with task count
- [ ] Tasks display with:
  - [ ] Task titles
  - [ ] Descriptions
  - [ ] Duration (30-120 minutes)
  - [ ] 2-4 subtasks each
- [ ] "View Raw JSON Response" expandable works

**Test Case 1.2: Custom Journal Entry**
- [ ] Clear text area
- [ ] Enter: "I need to study for my interview, prepare questions, and review the company website"
- [ ] Click "Parse with AI"
- [ ] Verify 3-5 tasks are generated
- [ ] Check that durations are within 30-120 minutes
- [ ] Verify each task has subtasks

**Expected Results:**
- ✅ No errors in parsing
- ✅ Valid JSON structure
- ✅ Appropriate task breakdown
- ✅ Reasonable time estimates

---

### 🎙️ **Test 2: AI Coach Messages**

**Test Case 2.1: Session Start Message**
- [ ] Task Name field shows "Write Project Report"
- [ ] Duration shows 90 minutes
- [ ] Click "▶️ Session Start" button
- [ ] Spinner shows "🤖 Generating message..."
- [ ] Info box displays encouraging message with 🎙️ emoji
- [ ] Message is approximately 15 words
- [ ] Message mentions the task and/or duration

**Test Case 2.2: Halfway Message**
- [ ] Click "⏱️ Halfway" button
- [ ] Message appears in info box
- [ ] Message is motivational/check-in style

**Test Case 2.3: Break Message**
- [ ] Click "☕ Break" button
- [ ] Message appears in info box
- [ ] Message suggests a healthy break activity

**Test Case 2.4: Completion Message**
- [ ] Click "✅ Completion" button
- [ ] Message appears in info box
- [ ] Message is celebratory/achievement-focused

**Test Case 2.5: Custom Context**
- [ ] Change Task Name to "Build Mobile App"
- [ ] Change Duration to 60
- [ ] Click any coach button
- [ ] Verify message reflects new context

**Expected Results:**
- ✅ All message types generate successfully
- ✅ Messages are contextually appropriate
- ✅ Messages are approximately 15 words
- ✅ No errors or empty responses

---

### 💾 **Test 3: Data Storage**

**Test Case 3.1: Save Default Task**
- [ ] Default values appear:
  - Task Title: "Test Task"
  - Duration: 60 minutes
  - Priority: 75.0
  - Description: "This is a test task to verify data storage"
- [ ] Click "💾 Save Test Task" button
- [ ] Spinner shows "💾 Saving to Snowflake..."
- [ ] Success message appears: "✅ Task 'Test Task' saved successfully"
- [ ] Toast notification appears: "✅ Task saved successfully!"
- [ ] "Saved Task Details" expandable shows complete JSON

**Test Case 3.2: Save Custom Task**
- [ ] Change Task Title to "Integration Testing"
- [ ] Change Duration to 90
- [ ] Change Priority to 85.0
- [ ] Modify description
- [ ] Click "Save Test Task"
- [ ] Verify success messages
- [ ] Check JSON shows correct values

**Test Case 3.3: Edge Cases**
- [ ] Try minimum duration (30 min)
- [ ] Try maximum duration (120 min)
- [ ] Try priority 0.0
- [ ] Try priority 100.0
- [ ] Verify all save successfully

**Expected Results:**
- ✅ Tasks save without errors
- ✅ Success messages display correctly
- ✅ Toast notifications appear
- ✅ Subtasks array is properly saved

---

### 📥 **Test 4: Retrieve Tasks**

**Test Case 4.1: Get All Tasks**
- [ ] Click "🔄 Get All Tasks" button
- [ ] Spinner shows "📥 Retrieving tasks from Snowflake..."
- [ ] Success message shows task count
- [ ] Tasks display in expandable cards
- [ ] Each task shows:
  - [ ] Title
  - [ ] Duration metric
  - [ ] Priority metric
  - [ ] Status with emoji (⏳/▶️/✅)
  - [ ] Description
  - [ ] Task ID
  - [ ] Created timestamp
  - [ ] Subtasks list

**Test Case 4.2: Verify Saved Tasks**
- [ ] Find previously saved "Test Task" in list
- [ ] Expand the card
- [ ] Verify all details match what was saved
- [ ] Check subtasks are preserved

**Test Case 4.3: Get Statistics**
- [ ] Click "📊 Get Statistics" button
- [ ] Spinner shows "📊 Fetching session statistics..."
- [ ] Success message appears
- [ ] Statistics display:
  - [ ] Total Sessions
  - [ ] Total Time (minutes)
  - [ ] Completion Rate (%)
  - [ ] Unique Tasks

**Test Case 4.4: Empty State**
- [ ] If no sessions exist today, verify statistics show 0
- [ ] No errors should occur

**Expected Results:**
- ✅ All saved tasks are retrieved
- ✅ Task data is displayed correctly
- ✅ Subtasks are properly parsed from JSON
- ✅ Statistics calculate correctly
- ✅ No database errors

---

### ⏱️ **Test 5: Work Session Tracking**

**Test Case 5.1: Save Completed Session**
- [ ] Session Duration shows 45 minutes
- [ ] "Completed" checkbox is checked
- [ ] Click "💾 Save Work Session" button
- [ ] Spinner shows "💾 Saving work session..."
- [ ] Success message: "✅ Work session saved successfully"
- [ ] Toast notification appears
- [ ] "Session Details" expandable shows JSON with:
  - [ ] session_id (UUID)
  - [ ] task_id (UUID)
  - [ ] start_time (ISO format)
  - [ ] duration_minutes (45)
  - [ ] completed (true)

**Test Case 5.2: Save Incomplete Session**
- [ ] Change duration to 30
- [ ] Uncheck "Completed" checkbox
- [ ] Click "Save Work Session"
- [ ] Verify saves with completed: false

**Test Case 5.3: Various Durations**
- [ ] Try minimum (5 min)
- [ ] Try maximum (120 min)
- [ ] Try various values in between
- [ ] All should save successfully

**Expected Results:**
- ✅ Sessions save without errors
- ✅ All fields are properly stored
- ✅ UUIDs are generated correctly
- ✅ Timestamps are in correct format

---

### 🔄 **Test 6: Update Task Status**

**Test Case 6.1: Update Existing Task**
- [ ] First, get all tasks to find a task ID
- [ ] Copy a task ID from the expandable card
- [ ] Paste into "Task ID to Update" field
- [ ] Select "in_progress" from dropdown
- [ ] Click "🔄 Update Status" button
- [ ] Spinner shows "🔄 Updating task status..."
- [ ] Success message: "✅ Task status updated to 'in_progress'"
- [ ] Toast notification appears

**Test Case 6.2: Verify Status Update**
- [ ] Click "Get All Tasks" again
- [ ] Find the updated task
- [ ] Expand the card
- [ ] Verify status shows "▶️ In Progress"

**Test Case 6.3: Update to Completed**
- [ ] Use same task ID
- [ ] Select "completed"
- [ ] Update status
- [ ] Verify success
- [ ] Refresh task list
- [ ] Verify shows "✅ Completed"

**Test Case 6.4: Invalid Task ID**
- [ ] Enter invalid UUID (e.g., "invalid-id")
- [ ] Try to update
- [ ] Should show error message gracefully

**Test Case 6.5: Empty Task ID**
- [ ] Clear task ID field
- [ ] Click "Update Status"
- [ ] Should show warning: "⚠️ Please enter a task ID"

**Expected Results:**
- ✅ Status updates successfully
- ✅ Changes persist in database
- ✅ UI reflects updated status
- ✅ Validation messages work
- ✅ Error handling is graceful

---

## 🔍 **Error Testing**

### Test Error Handling
- [ ] Test with empty journal text (should warn)
- [ ] Test with very long journal text (should handle gracefully)
- [ ] Test with special characters in task names
- [ ] Test with emoji in descriptions
- [ ] Verify all errors show in expandable "Error Details"

**Expected Results:**
- ✅ No crashes on invalid input
- ✅ User-friendly error messages
- ✅ Detailed error info in expandables
- ✅ App remains functional after errors

---

## 🎨 **UI/UX Verification**

### Visual Elements
- [ ] Page title displays: "🧪 Snowflake Client Test Suite"
- [ ] Page icon is 🧪
- [ ] Layout is wide format
- [ ] All sections have clear headers with emojis
- [ ] Dividers separate sections cleanly
- [ ] Buttons use appropriate colors (primary for main actions)
- [ ] Spinners show during all operations
- [ ] Toast notifications appear and disappear
- [ ] Expandables work correctly
- [ ] Footer displays: "All tests use real Snowflake Cortex AI ⚡"

### Responsiveness
- [ ] All columns display properly
- [ ] Buttons are properly sized
- [ ] Text doesn't overflow containers
- [ ] Metrics display clearly
- [ ] JSON views are readable

**Expected Results:**
- ✅ Professional, clean interface
- ✅ Consistent styling throughout
- ✅ Good use of whitespace
- ✅ Clear visual hierarchy
- ✅ Responsive layout

---

## 📊 **Performance Check**

### Operation Timing
- [ ] Connection initializes quickly (< 3 seconds)
- [ ] Journal parsing completes in reasonable time (< 10 seconds)
- [ ] Coach messages generate quickly (< 5 seconds)
- [ ] Database operations are fast (< 3 seconds)
- [ ] Task retrieval is performant (< 5 seconds)

### Resource Usage
- [ ] No memory leaks on repeated operations
- [ ] Browser doesn't slow down with multiple tests
- [ ] Streamlit cache works (@st.cache_resource)

**Expected Results:**
- ✅ Responsive user experience
- ✅ No noticeable lag
- ✅ Efficient caching

---

## ✅ **Final Verification**

### Complete Test Sequence
1. [ ] Connect to Snowflake
2. [ ] Parse a journal entry
3. [ ] Generate all 4 coach message types
4. [ ] Save a new task
5. [ ] Retrieve all tasks (should include new task)
6. [ ] Save a work session
7. [ ] Get statistics (should reflect new session)
8. [ ] Update a task status
9. [ ] Verify update by retrieving tasks again

### Known Issues to Check
- [ ] RuntimeWarning about coroutine (harmless, can ignore)
- [ ] Any import errors
- [ ] Missing dependencies
- [ ] Connection timeouts

---

## 🎉 **Success Criteria**

**All tests pass when:**
- ✅ No errors during any operation
- ✅ All AI responses are contextually appropriate
- ✅ Database operations persist correctly
- ✅ UI is responsive and user-friendly
- ✅ Error handling works gracefully
- ✅ All features work as documented

---

## 📝 **Test Results Summary**

**Date:** November 9, 2025
**Tester:** _________________
**Overall Status:** [ ] PASS [ ] FAIL [ ] NEEDS FIXES

**Notes:**
_____________________________________________________________
_____________________________________________________________
_____________________________________________________________

**Issues Found:**
_____________________________________________________________
_____________________________________________________________
_____________________________________________________________

**Recommendations:**
_____________________________________________________________
_____________________________________________________________
_____________________________________________________________

---

## 🚀 **Next Steps After Testing**

If all tests pass:
1. ✅ Mark SnowflakeClient as production-ready
2. ✅ Integrate into main Focus Flow app
3. ✅ Deploy to production
4. ✅ Monitor real-world usage

If issues found:
1. 🔧 Document all errors
2. 🔧 Fix critical issues first
3. 🔧 Re-run test suite
4. 🔧 Iterate until all tests pass

---

**Test App URL:** http://localhost:8502
**Test File:** `tests/test_client_ui.py`
**Client File:** `utils/snowflake_client.py`
