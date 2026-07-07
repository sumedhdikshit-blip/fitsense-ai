import os
import sys
from unittest.mock import patch, MagicMock

# Add fitsense-ai workspace to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database import db
from main import get_coach_tip

def test_coach_tip_empty_state():
    """Verify that get_coach_tip returns friendly message when user has no workouts."""
    import tempfile
    
    temp_db_fd, temp_db_path = tempfile.mkstemp()
    os.close(temp_db_fd)
    
    try:
        original_db_path = db.DB_PATH
        db.DB_PATH = temp_db_path
        db.init_db()
        
        uid = db.create_user("coach_test_user_empty", "pass", "Coach Empty")
        
        # Act
        result = get_coach_tip(user_id=uid)
        
        # Assert
        assert result == {"tip": "Log a workout first to get personalized coaching tips"}
        
    finally:
        db.DB_PATH = original_db_path
        try:
            if os.path.exists(temp_db_path):
                os.remove(temp_db_path)
        except PermissionError:
            pass

def test_coach_tip_groq_error_graceful():
    """Verify that get_coach_tip handles Groq client initialization or call errors gracefully."""
    import tempfile
    
    temp_db_fd, temp_db_path = tempfile.mkstemp()
    os.close(temp_db_fd)
    
    try:
        original_db_path = db.DB_PATH
        db.DB_PATH = temp_db_path
        db.init_db()
        
        uid = db.create_user("coach_test_user_err", "pass", "Coach Err")
        
        # Log a session to bypass empty check
        sess_id = db.create_in_progress_session(uid)
        db.finalize_session(sess_id, notes="Great push workout")
        
        # Mock get_groq_client to raise exception
        with patch("ai.coach_client.get_groq_client", side_effect=ValueError("Missing API key")):
            result = get_coach_tip(user_id=uid)
            assert result == {"tip": "Coach tip unavailable right now"}
            
    finally:
        db.DB_PATH = original_db_path
        try:
            if os.path.exists(temp_db_path):
                os.remove(temp_db_path)
        except PermissionError:
            pass

def test_coach_tip_success():
    """Verify that get_coach_tip succeeds and calls Groq client with formatted prompt."""
    import tempfile
    
    temp_db_fd, temp_db_path = tempfile.mkstemp()
    os.close(temp_db_fd)
    
    try:
        original_db_path = db.DB_PATH
        db.DB_PATH = temp_db_path
        db.init_db()
        
        uid = db.create_user("coach_test_user_ok", "pass", "Coach OK")
        
        # Log a session and weight
        sess_id = db.create_in_progress_session(uid)
        ex_id = db.get_or_create_exercise(sess_id, "squat", "Squat")
        db.log_set_to_db(ex_id, 1, 10, 100.0, 8, 95.0, False, "")
        db.finalize_session(sess_id)
        
        db.log_weight(uid, "2026-07-06", 80.0)
        db.log_weight(uid, "2026-07-07", 79.5)
        
        # Mock groq client response
        mock_client = MagicMock()
        mock_completion = MagicMock()
        mock_choice = MagicMock()
        mock_message = MagicMock()
        mock_message.content = "Great job on your squats! You lifted 100.0 kg for 10 reps. Keep up the good work and watch your form."
        mock_choice.message = mock_message
        mock_completion.choices = [mock_choice]
        mock_client.chat.completions.create.return_value = mock_completion
        
        with patch("ai.coach_client.get_groq_client", return_value=mock_client):
            result = get_coach_tip(user_id=uid)
            
            # Verify result matches LLM reply
            assert "Great job on your squats!" in result["tip"]
            
            # Verify groq was called
            mock_client.chat.completions.create.assert_called_once()
            
            # Verify prompt content includes weight trend and exercise details
            call_kwargs = mock_client.chat.completions.create.call_args[1]
            prompt = call_kwargs["messages"][0]["content"]
            assert "Squat" in prompt
            assert "100.0" in prompt or "100" in prompt
            assert "79.5" in prompt
            
    finally:
        db.DB_PATH = original_db_path
        try:
            if os.path.exists(temp_db_path):
                os.remove(temp_db_path)
        except PermissionError:
            pass
