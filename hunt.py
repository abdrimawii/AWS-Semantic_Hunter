import faiss
import json
import numpy as np
from sentence_transformers import SentenceTransformer

print("Initializing the Hunter...")
model = SentenceTransformer('all-MiniLM-L6-v2')
index = faiss.read_index("threat_hunter.index")

with open("event_metadata.json", "r") as f:
    all_events = json.load(f)

def search_logs():
    while True:
        query = input("\n[Hunt] Describe the activity you're looking for (or type 'exit'): ")
        if query.lower() == 'exit':
            break
            

        query_vector = model.encode([query])
        
        distances, indices = index.search(np.array(query_vector).astype('float32'), k=5)
        
        print(f"\n--- Potential Matches for '{query}' ---")
        for i in indices[0]:
            if i != -1: 
                event = all_events[i]
                print(f" -> {event['summary']}")

if __name__ == "__main__":
    search_logs()