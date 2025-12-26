import sys
import os
import pytest
from fastapi.testclient import TestClient

# FastAPIアプリのパスを追加
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from app import app

client = TestClient(app)


def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert "Chess Club" in data
    assert isinstance(data, dict)

def test_signup_for_activity():
    activity = "Chess Club"
    email = "newstudent@mergington.edu"
    # 正常な登録
    response = client.post(f"/activities/{activity}/signup", params={"email": email})
    assert response.status_code == 200
    assert response.json()["message"] == f"Signed up {email} for {activity}"
    # 既に登録済みの場合
    response = client.post(f"/activities/{activity}/signup", params={"email": email})
    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up for this activity"

def test_signup_activity_not_found():
    response = client.post("/activities/UnknownActivity/signup", params={"email": "test@mergington.edu"})
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"

def test_remove_participant():
    activity = "Chess Club"
    email = "newstudent@mergington.edu"
    # 参加者削除（正常）
    response = client.post(f"/activities/{activity}/remove", json=email)
    assert response.status_code == 200
    assert response.json()["message"] == f"Removed {email} from {activity}"
    # 参加者がいない場合
    response = client.post(f"/activities/{activity}/remove", json=email)
    assert response.status_code == 404
    assert response.json()["detail"] == "Participant not found in this activity"

def test_remove_activity_not_found():
    response = client.post("/activities/UnknownActivity/remove", json="test@mergington.edu")
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"
