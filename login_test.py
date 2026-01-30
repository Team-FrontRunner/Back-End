import requests

def get_token(user_id):
    url = "http://localhost:8000/users/login"
    payload = {"user_id": user_id}
    
    try:
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            token = response.json().get("access_token")
            print(f"--- Login Success ---")
            print(f"User ID: {user_id}")
            print(f"Access Token:\n{token}")
            print(f"----------------------")
            return token
        else:
            print(f"Error: {response.status_code}, {response.text}")
    except Exception as e:
        print(f"Failed to connect to server: {e}")

if __name__ == "__main__":
    # 테스트하고 싶은 유저 ID를 입력하세요.
    test_id = "f57ce428-5e03-4613-9186-cdbce942ba7a"
    get_token(test_id)
