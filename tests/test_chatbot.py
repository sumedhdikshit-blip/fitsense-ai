import os
import sys
from unittest.mock import patch, MagicMock

# Add fitsense-ai workspace to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database import db, models
from main import chat_with_coach
from starlette.requests import Request
from fastapi import HTTPException

# Test 1: Empty message raises HTTP 400
def test_chatbot_empty_message():
    import tempfile
    
    temp_db_fd, temp_db_path = tempfile.mkstemp()
    os.close(temp_db_fd)
    
    try:
        original_db_path = db.DB_PATH
        db.DB_PATH = temp_db_path
        db.init_db()
        
        uid = db.create_user("chat_test_user_empty", "pass", "Chat Empty")
        
        mock_req = Request(scope={"type": "http", "method": "POST", "path": "/chat", "headers": [], "session": {}})
        req_data = models.ChatRequest(message="   ")
        
        try:
            chat_with_coach(request=mock_req, data=req_data, user_id=uid)
            assert False, "Should raise HTTPException 400"
        except HTTPException as exc:
            assert exc.status_code == 400
            assert "empty" in exc.detail
            
    finally:
        db.DB_PATH = original_db_path
        try:
            if os.path.exists(temp_db_path):
                os.remove(temp_db_path)
        except PermissionError:
            pass

# Test 2: Success personal query uses correct prompt/data
def test_chatbot_personal_query():
    import tempfile
    
    temp_db_fd, temp_db_path = tempfile.mkstemp()
    os.close(temp_db_fd)
    
    try:
        original_db_path = db.DB_PATH
        db.DB_PATH = temp_db_path
        db.init_db()
        
        uid = db.create_user("chat_test_user_personal", "pass", "Chat Personal")
        
        # Save a goal and nutrition log
        db.save_weight_goal(uid, "lose", 70.0, 75.0, "2026-08-01", "normal", "preserve", None)
        db.log_nutrition(uid, "2026-07-09", 2000.0, 150.0, 200.0, 60.0)
        
        # Mock client
        mock_client = MagicMock()
        mock_completion = MagicMock()
        mock_choice = MagicMock()
        mock_message = MagicMock()
        mock_message.content = "Based on your progress, you are doing well!"
        mock_choice.message = mock_message
        mock_completion.choices = [mock_choice]
        mock_client.chat.completions.create.return_value = mock_completion
        
        session = {}
        mock_req = Request(scope={"type": "http", "method": "POST", "path": "/chat", "headers": [], "session": session})
        req_data = models.ChatRequest(message="How am I doing on my weight goal?")
        
        with patch("ai.coach_client.get_groq_client", return_value=mock_client) as mock_get_client:
            res = chat_with_coach(request=mock_req, data=req_data, user_id=uid)
            assert res == {"reply": "Based on your progress, you are doing well!"}
            
            # Verify system prompt context contains user profile weight goal and calories
            called_args = mock_client.chat.completions.create.call_args[1]
            messages = called_args["messages"]
            system_msg = messages[0]["content"]
            assert "70.0" in system_msg
            assert "lose" in system_msg
            assert "2000.0" in system_msg
            assert "150.0" in system_msg
            
            # Verify session history updated
            assert len(session.get("chat_history", [])) == 2
            assert session["chat_history"][0]["role"] == "user"
            assert session["chat_history"][0]["content"] == "How am I doing on my weight goal?"
            assert session["chat_history"][1]["role"] == "assistant"
            assert session["chat_history"][1]["content"] == "Based on your progress, you are doing well!"
            
    finally:
        db.DB_PATH = original_db_path
        try:
            if os.path.exists(temp_db_path):
                os.remove(temp_db_path)
        except PermissionError:
            pass

# Test 3: Chatbot handles ValueError/Groq API failures gracefully
def test_chatbot_error_handling():
    import tempfile
    
    temp_db_fd, temp_db_path = tempfile.mkstemp()
    os.close(temp_db_fd)
    
    try:
        original_db_path = db.DB_PATH
        db.DB_PATH = temp_db_path
        db.init_db()
        
        uid = db.create_user("chat_test_user_err", "pass", "Chat Err")
        
        mock_req = Request(scope={"type": "http", "method": "POST", "path": "/chat", "headers": [], "session": {}})
        req_data = models.ChatRequest(message="What is protein?")
        
        with patch("ai.coach_client.get_groq_client", side_effect=Exception("API limit exceeded")):
            try:
                chat_with_coach(request=mock_req, data=req_data, user_id=uid)
                assert False, "Should raise HTTPException 500"
            except HTTPException as exc:
                assert exc.status_code == 500
                assert exc.detail == "Sorry, I couldn't process that — try again."
                
    finally:
        db.DB_PATH = original_db_path
        try:
            if os.path.exists(temp_db_path):
                os.remove(temp_db_path)
        except PermissionError:
            pass
