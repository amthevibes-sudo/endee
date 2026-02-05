import requests
import msgpack
from config import Config
from embedder import Embedder

def debug_search():
    embedder = Embedder()
    query_vec = embedder.embed_text("vector database")
    
    url = f"{Config.ENDEE_URL}/api/v1/index/{Config.COLLECTION_NAME}/search"
    data = {"vector": query_vec.tolist(), "k": 5}
    
    print(f"Searching at {url}...")
    response = requests.post(url, json=data)
    
    if response.status_code == 200:
        print("✅ Search successful!")
        raw_data = response.content
        print(f"Raw binary size: {len(raw_data)} bytes")
        
        try:
            # Try unpacking
            unpacked = msgpack.unpackb(raw_data, raw=False)
            print("Unpacked data type:", type(unpacked))
            print("Number of results:", len(unpacked))
            if len(unpacked) > 0:
                print("First result type:", type(unpacked[0]))
                print("First result content:", unpacked[0])
        except Exception as e:
            print(f"❌ Failed to unpack: {e}")
    else:
        print(f"❌ Search failed: {response.status_code}")
        print(response.text)

if __name__ == "__main__":
    debug_search()
