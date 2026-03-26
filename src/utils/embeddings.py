import os
import requests
import numpy as np
import time
from dotenv import load_dotenv

load_dotenv()

# Using a more reliable embedding model for Feature Extraction
HF_API_URL = "https://router.huggingface.co/hf-inference/models/BAAI/bge-small-en-v1.5"
headers = {"Authorization": f"Bearer {os.getenv('HF_API_KEY')}"}

def get_embedding(text):
    """Fetches a vector (embedding) for a given text from HuggingFace."""
    # Ensure text is not empty
    if not text.strip():
        return None
        
    payload = {"inputs": text}
    
    for attempt in range(3):
        try:
            response = requests.post(HF_API_URL, headers=headers, json=payload, timeout=10)
            
            if response.status_code == 200:
                result = response.json()
                # BGE model returns a list of floats or a list of lists. 
                # We need a flat list of floats.
                if isinstance(result, list) and isinstance(result[0], list):
                    return result[0]
                return result
            elif response.status_code == 503:
                print(f"HuggingFace is loading the model... waiting 10s (Attempt {attempt+1})")
                time.sleep(10)
                continue
            else:
                raise Exception(f"HF API Error: {response.status_code} - {response.text}")
        except Exception as e:
            if attempt == 2: raise e
            time.sleep(2)
            
    return None

def cosine_similarity(v1, v2):
    """Calculates how similar two vectors are."""
    v1, v2 = np.array(v1), np.array(v2)
    return np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))