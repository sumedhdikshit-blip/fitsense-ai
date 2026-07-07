import os
import sys
import json
import tempfile
from unittest.mock import patch, MagicMock

# Add fitsense-ai workspace to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database import db
from main import get_insights
from starlette.requests import Request

def test_insights_empty_state():
    """Verify that get_insights returns friendly message when user has no workouts and skips Groq."""
    temp_db_fd, temp_db_path = tempfile.mkstemp()
    os.close(temp_db_fd)
    try:
        original_db_path = db.DB_PATH
        db.DB_PATH = temp_db_path
        db.init_db()
        
        uid = db.create_user("insights_empty_user", "pass", "Insights Empty")
        
        with patch("ai.coach_client.get_groq_client") as mock_client:
            mock_req = Request(scope={"type": "http", "method": "GET", "path": "/ai/insights", "headers": []})
            res = get_insights(request=mock_req, user_id=uid)
            assert "message" in res
            assert res["progress_summary"] == "No workouts logged yet."
            mock_client.assert_not_called()
    finally:
        db.DB_PATH = original_db_path
        try:
            if os.path.exists(temp_db_path):
                os.remove(temp_db_path)
        except:
            pass

def test_insights_success():
    """Verify that get_insights parses a valid JSON response from Groq client correctly."""
    temp_db_fd, temp_db_path = tempfile.mkstemp()
    os.close(temp_db_fd)
    try:
        original_db_path = db.DB_PATH
        db.DB_PATH = temp_db_path
        db.init_db()
        
        uid = db.create_user("insights_success_user", "pass", "Insights Success")
        
        # Log a session to bypass empty check
        sess_id = db.create_in_progress_session(uid)
        ex_id = db.get_or_create_exercise(sess_id, "squat", "Squat")
        db.log_set_to_db(ex_id, 1, 10, 100.0, 8, 95.0, False, "")
        db.finalize_session(sess_id)
        
        mock_client = MagicMock()
        mock_completion = MagicMock()
        mock_choice = MagicMock()
        mock_message = MagicMock()
        
        mock_json_response = {
            "progress_summary": "Your squat session on July 6 showed excellent form at 92.5%. You burned 150.0 kcal across 3 sets of 30 total reps.",
            "tips_to_improve": "Since your form score is high, focus on progressive overload. Try adding small weight increments to your Squats.",
            "what_to_avoid": "Avoid rushing your concentric phase. Control the descent to maintain your 92.5% form rating.",
            "next_steps": "Plan your next leg session for tomorrow. Aim for 3 sets of squats targeting the same form index.",
            "motivation_note": "A 92.5% form rating is a fantastic starting point. Keep lifting with precision!"
        }
        
        mock_message.content = json.dumps(mock_json_response)
        mock_choice.message = mock_message
        mock_completion.choices = [mock_choice]
        mock_client.chat.completions.create.return_value = mock_completion
        
        with patch("ai.coach_client.get_groq_client", return_value=mock_client):
            mock_req = Request(scope={"type": "http", "method": "GET", "path": "/ai/insights", "headers": []})
            res = get_insights(request=mock_req, user_id=uid)
            assert res["progress_summary"] == mock_json_response["progress_summary"]
            assert res["tips_to_improve"] == mock_json_response["tips_to_improve"]
            assert res["what_to_avoid"] == mock_json_response["what_to_avoid"]
            assert res["next_steps"] == mock_json_response["next_steps"]
            assert res["motivation_note"] == mock_json_response["motivation_note"]
    finally:
        db.DB_PATH = original_db_path
        try:
            if os.path.exists(temp_db_path):
                os.remove(temp_db_path)
        except:
            pass

def test_insights_malformed_json_retry():
    """Verify that get_insights retries once with a stricter prompt on malformed JSON, and parses successfully if retry succeeds."""
    temp_db_fd, temp_db_path = tempfile.mkstemp()
    os.close(temp_db_fd)
    try:
        original_db_path = db.DB_PATH
        db.DB_PATH = temp_db_path
        db.init_db()
        
        uid = db.create_user("insights_retry_user", "pass", "Insights Retry")
        
        # Log a session to bypass empty check
        sess_id = db.create_in_progress_session(uid)
        ex_id = db.get_or_create_exercise(sess_id, "squat", "Squat")
        db.log_set_to_db(ex_id, 1, 10, 100.0, 8, 95.0, False, "")
        db.finalize_session(sess_id)
        
        mock_client = MagicMock()
        
        # First call return value is malformed JSON (plain string)
        mock_completion_fail = MagicMock()
        mock_choice_fail = MagicMock()
        mock_message_fail = MagicMock()
        mock_message_fail.content = "This is not a JSON object at all."
        mock_choice_fail.message = mock_message_fail
        mock_completion_fail.choices = [mock_choice_fail]
        
        # Second call (retry) returns valid JSON
        mock_completion_success = MagicMock()
        mock_choice_success = MagicMock()
        mock_message_success = MagicMock()
        mock_json_response = {
            "progress_summary": "Successful progress summary after retry.",
            "tips_to_improve": "Successful tips after retry.",
            "what_to_avoid": "Successful avoid after retry.",
            "next_steps": "Successful next steps after retry.",
            "motivation_note": "Successful motivation after retry."
        }
        mock_message_success.content = json.dumps(mock_json_response)
        mock_choice_success.message = mock_message_success
        mock_completion_success.choices = [mock_choice_success]
        
        # side_effect returns fail first, then success
        mock_client.chat.completions.create.side_effect = [mock_completion_fail, mock_completion_success]
        
        with patch("ai.coach_client.get_groq_client", return_value=mock_client):
            mock_req = Request(scope={"type": "http", "method": "GET", "path": "/ai/insights", "headers": []})
            res = get_insights(request=mock_req, user_id=uid)
            assert res["progress_summary"] == mock_json_response["progress_summary"]
            assert res["tips_to_improve"] == mock_json_response["tips_to_improve"]
            assert mock_client.chat.completions.create.call_count == 2
    finally:
        db.DB_PATH = original_db_path
        try:
            if os.path.exists(temp_db_path):
                os.remove(temp_db_path)
        except:
            pass

def test_insights_api_failure():
    """Verify that get_insights returns a graceful fallback message when both attempts fail or raise exception."""
    temp_db_fd, temp_db_path = tempfile.mkstemp()
    os.close(temp_db_fd)
    try:
        original_db_path = db.DB_PATH
        db.DB_PATH = temp_db_path
        db.init_db()
        
        uid = db.create_user("insights_fail_user", "pass", "Insights Fail")
        
        # Log a session to bypass empty check
        sess_id = db.create_in_progress_session(uid)
        ex_id = db.get_or_create_exercise(sess_id, "squat", "Squat")
        db.log_set_to_db(ex_id, 1, 10, 100.0, 8, 95.0, False, "")
        db.finalize_session(sess_id)
        
        # Mock get_groq_client to raise exception
        with patch("ai.coach_client.get_groq_client", side_effect=ValueError("Missing API key")):
            mock_req = Request(scope={"type": "http", "method": "GET", "path": "/ai/insights", "headers": []})
            res = get_insights(request=mock_req, user_id=uid)
            assert "error" in res
            assert "missing api configuration" in res["error"].lower()
    finally:
        db.DB_PATH = original_db_path
        try:
            if os.path.exists(temp_db_path):
                os.remove(temp_db_path)
        except:
            pass
