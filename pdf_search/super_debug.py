import requests
import msgpack
import numpy as np
from config import Config
from embedder import Embedder

def super_debug_search():
    embedder = Embedder()
    query_vec = embedder.embed_text("vector database performance")
    
    url = f"{Config.ENDEE_URL}/api/v1/index/{Config.COLLECTION_NAME}/search"
    data = {"vector": query_vec.tolist(), "k": 5}
    
    print(f"SEARCH URL: {url}")
    print(f"SEARCH DATA: k={data['k']}, vector_len={len(data['vector'])}")
    
    response = requests.post(url, json=data)
    
    print(f"STATUS CODE: {response.status_code}")
    if response.status_code != 200:
        print(f"ERROR: {response.text}")
        return

    raw_content = response.content
    print(f"RAW CONTENT SIZE: {len(raw_content)} bytes")
    
    unpacked = msgpack.unpackb(raw_content, raw=False)
    print(f"UNPACKED DATA TYPE: {type(unpacked)}")
    print(f"UNPACKED DATA: {unpacked}")
    
    # Simulating EndeeClient logic
    response_data = unpacked
    if len(response_data) > 0 and isinstance(response_data[0], list):
        if len(response_data[0]) > 0 and isinstance(response_data[0][0], (list, tuple)):
            print("Detected WRAPPED ResultSet")
            hits = response_data[0]
        else:
            print("Detected UNWRAPPED list of results")
            hits = response_data
    else:
        print("Detected non-standard format or empty results")
        hits = response_data
        
    print(f"EXTRACTED HITS (count={len(hits)}): {hits}")
    
    for i, item in enumerate(hits):
        print(f"Hit {i} type: {type(item)}")
        print(f"Hit {i} content: {item}")

if __name__ == "__main__":
    super_debug_search()
