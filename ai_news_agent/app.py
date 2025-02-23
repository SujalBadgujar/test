from fastapi import FastAPI
import requests

app = FastAPI()

# Hugging Face API details
API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct"
HEADERS = {"Authorization": "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"}  # Replace with your real API key

@app.post("/generate/")
def generate_blog(prompt: str):
    """API Endpoint to generate a blog post"""
    response = requests.post(API_URL, headers=HEADERS, json={"inputs": prompt})
    return {"blog_post": response.json()}
