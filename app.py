import streamlit as st
import faiss
import json
import numpy as np
import pandas as pd
from sentence_transformers import SentenceTransformer


st.set_page_config(page_title="AWS Semantic Hunter", page_icon="🛡️", layout="wide")


@st.cache_resource
def load_resources():
    model = SentenceTransformer('all-MiniLM-L6-v2')
    index = faiss.read_index("threat_hunter.index")
    with open("event_metadata.json", "r") as f:
        all_events = json.load(f)
    return model, index, all_events

model, index, all_events = load_resources()

st.title("🛡️ AWS Semantic Threat Hunter")
st.markdown("### Search your CloudTrail logs using natural language intent.")

query = st.text_input("Describe a threat or activity (e.g., 'Unauthorized login attempts' or 'S3 bucket changes')", "")

if query:
    
    query_vector = model.encode([query])
    
    
    k = 25  
    distances, indices = index.search(np.array(query_vector).astype('float32'), k)
    
    
    results = []
    for i in indices[0]:
        if i != -1:
            evt = all_events[i]
            results.append({
                "Match Confidence": round(1 / (1 + distances[0][results.__len__()]), 2),
                "Summary": evt['summary'],
                "Event Name": evt['raw'].get('eventName'),
                "User": evt['raw'].get('userIdentity', {}).get('arn', 'N/A'),
                "Source IP": evt['raw'].get('sourceIPAddress', 'N/A')
            })
     
    df = pd.DataFrame(results)
    st.dataframe(df, use_container_width=True)

st.sidebar.header("Log Statistics")
st.sidebar.info(f"Total Logs Indexed: {len(all_events)}")
if st.sidebar.button("Re-run Log Fetcher"):
    st.sidebar.warning("This would trigger fetch_logs.py (Logic for button can be added later)")