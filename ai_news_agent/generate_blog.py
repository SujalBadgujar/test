import requests

# Hugging Face API details
API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct"
HEADERS = {"Authorization": "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"}  # Replace with your real API key

def generate_blog(prompt):
    """Generates a blog post using Hugging Face API."""
    response = requests.post(API_URL, headers=HEADERS, json={"inputs": prompt})
    return response.json()

# Example test
prompt = "Write a blog post about the future of AI in healthcare."
result = generate_blog(prompt)
print(result)
