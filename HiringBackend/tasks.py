# tasks.py
from celery import shared_task
from datetime import datetime
import requests

@shared_task
def call_api_task():
    api_url = 'http://127.0.0.1:8000/email/readResume'  # Replace with your API endpoint
    response = requests.get(api_url)
    
    if response.status_code == 200:
        print(f"API called successfully at {datetime.now()}")
        # Process the API response as needed
    else:
        print(f"Failed to call API at {datetime.now()}. Status code: {response.status_code}")
