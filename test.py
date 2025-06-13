import json

# Example: Load JSON data from a file
with open("all_posts.json", "r", encoding="utf-8") as f:
    data = json.load(f)

documents = []

for doc in data:
    text = doc.get("content", "").strip()
    url = doc.get("url", "").strip()
    
    # Generate a title since none is provided
    topic_id = doc.get("topic_id", "unknown")
    post_number = doc.get("post_number", "unknown")
    title = f"Topic {topic_id}, Post {post_number}"
    
    # Only add if text and url exist
    if text and url:
        documents.append({
            "text": text,
            "url": url,
            "title": title
        })

if not documents:
    raise ValueError("No valid documents found with non-empty 'content' and 'url'.")

# Example: print the first document to verify
print(documents[0])
