"""
Test the new priority and label features
"""
import requests

BASE_URL = "http://127.0.0.1:8000/api"

# Use existing token (replace with a valid token from your test)
TOKEN = "YOUR_TOKEN_HERE"
headers = {"Authorization": f"Bearer {TOKEN}"}

# Test creating task with priority and label
def test_create_task():
    task_data = {
        "title": "Test Priority Task",
        "description": "Testing high priority urgent task",
        "priority": "high",
        "label": "urgent"
    }
    
    response = requests.post(f"{BASE_URL}/tasks", json=task_data, headers=headers)
    print(f"Create task: {response.status_code}")
    if response.status_code == 200:
        task = response.json()
        print(f"  ✅ Created task with priority={task['priority']}, label={task['label']}")
        return task['id']
    else:
        print(f"  ❌ Error: {response.text}")
        return None

# Test filtering by priority
def test_filter_by_priority():
    response = requests.get(f"{BASE_URL}/tasks?priority=high", headers=headers)
    print(f"\nFilter by priority=high: {response.status_code}")
    if response.status_code == 200:
        tasks = response.json()
        print(f"  ✅ Found {len(tasks)} high priority tasks")
        for task in tasks[:3]:  # Show first 3
            print(f"    - {task['title']} (priority={task['priority']}, label={task['label']})")

# Test filtering by label
def test_filter_by_label():
    response = requests.get(f"{BASE_URL}/tasks?label=urgent", headers=headers)
    print(f"\nFilter by label=urgent: {response.status_code}")
    if response.status_code == 200:
        tasks = response.json()
        print(f"  ✅ Found {len(tasks)} urgent tasks")

# Test filtering by both
def test_filter_by_both():
    response = requests.get(f"{BASE_URL}/tasks?priority=high&label=urgent", headers=headers)
    print(f"\nFilter by priority=high AND label=urgent: {response.status_code}")
    if response.status_code == 200:
        tasks = response.json()
        print(f"  ✅ Found {len(tasks)} high priority urgent tasks")

if __name__ == "__main__":
    print("🧪 Testing Priority & Label Features\n")
    print("=" * 50)
    
    # First, you need to get a token by logging in
    print("\n⚠️  To run this test, first get a valid token:")
    print("1. Login via POST /api/auth/login")
    print("2. Copy the access_token")
    print("3. Replace TOKEN in this script")
    print("\nOr test manually using the frontend! 🎨\n")
