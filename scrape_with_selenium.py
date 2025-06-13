from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
import json
import os
from datetime import datetime

BASE_URL = "https://discourse.onlinedegree.iitm.ac.in"
CATEGORY_JSON = f"{BASE_URL}/c/courses/tools-in-data-science/75.json"

USERNAME = "24f1000112@ds.study.iitm.ac.in"
PASSWORD = "Cutiepie.18"     # replace with your password

def login_and_fetch_data():
    options = Options()
    options.add_argument("--headless")  # comment out to see browser
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    # 1. Go to login page
    driver.get(f"{BASE_URL}/login")
    time.sleep(3)

    # 2. Enter credentials and login
    driver.find_element(By.ID, "login-account-name").send_keys(USERNAME)
    driver.find_element(By.ID, "login-account-password").send_keys(PASSWORD)
    driver.find_element(By.XPATH, "//button[contains(@class, 'btn-primary')]").click()
    time.sleep(5)  # wait for login to complete

    # 3. Go to category JSON URL
    driver.get(CATEGORY_JSON)
    time.sleep(3)

    # 4. Extract JSON text from <pre> tag
    raw_json = driver.find_element(By.TAG_NAME, "pre").text
    category_data = json.loads(raw_json)
    print(f"Fetched {len(category_data.get('topic_list', {}).get('topics', []))} topics")

    # Save category topics JSON
    with open("category_topics.json", "w", encoding="utf-8") as f:
        json.dump(category_data, f, indent=2, ensure_ascii=False)
    print(f"Saved category_topics.json at: {os.path.abspath('category_topics.json')}")

    # 5. Fetch all posts from topics
    all_posts = []
    for topic in category_data.get("topic_list", {}).get("topics", []):
        topic_id = topic["id"]
        topic_url = f"{BASE_URL}/t/{topic_id}.json"
        print(f"Fetching topic {topic_id}...")

        driver.get(topic_url)
        time.sleep(2)

        topic_raw = driver.find_element(By.TAG_NAME, "pre").text
        topic_data = json.loads(topic_raw)

        posts = topic_data.get("post_stream", {}).get("posts", [])
        for post in posts:
            all_posts.append({
                "topic_id": topic_id,
                "post_number": post["post_number"],
                "content": post["cooked"],
                "created_at": post["created_at"],
                "url": f"{BASE_URL}/t/{topic_id}/{post['post_number']}"
            })

    # Save all posts to JSON
    with open("all_posts.json", "w", encoding="utf-8") as f:
        json.dump(all_posts, f, indent=2, ensure_ascii=False)
    print(f"Saved {len(all_posts)} posts to all_posts.json at: {os.path.abspath('all_posts.json')}")

    driver.quit()

if __name__ == "__main__":
    login_and_fetch_data()
