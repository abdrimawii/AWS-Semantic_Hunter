import os
import json
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

print("Loading Local AI Model... (all-MiniLM-L6-v2)")
model = SentenceTransformer('all-MiniLM-L6-v2')

LOG_DIR = './raw_logs'
all_events = []

print("Parsing JSON logs from raw_logs...")
if not os.path.exists(LOG_DIR):
    print(f"Error: Folder {LOG_DIR} not found!")
else:
    for root, dirs, files in os.walk(LOG_DIR):
        for file in files:
            if file.endswith('.json'):
                with open(os.path.join(root, file), 'r') as f:
                    try:
                        data = json.load(f)
                        for record in data.get('Records', []):
                            user = record.get('userIdentity', {}).get('arn', 'UnknownUser')
                            event = record.get('eventName', 'UnknownEvent')
                            source = record.get('eventSource', 'UnknownSource')
                            
                            summary = f"User {user} performed {event} on {source}"
                            all_events.append({"summary": summary, "raw": record})
                    except Exception as e:
                        print(f"Skipping broken file {file}: {e}")
                        continue

if not all_events:
    print("Error: No events found in the JSON files. Check your logs!")
else:
    print(f"Vectorizing {len(all_events)} events... processing on your CPU.")
    summaries = [e['summary'] for e in all_events]
    embeddings = model.encode(summaries)

    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(np.array(embeddings).astype('float32'))

    faiss.write_index(index, "threat_hunter.index")
    with open("event_metadata.json", "w") as f:
        json.dump(all_events, f)
    
    print("--- Success! ---")
    print("Files created: 'threat_hunter.index' and 'event_metadata.json'")
    print("Your Semantic Database is now ready for hunting.")