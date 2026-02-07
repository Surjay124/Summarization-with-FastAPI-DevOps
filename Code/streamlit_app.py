import streamlit as st
import requests
import json
import pandas as pd
from datetime import datetime

# Configuration
API_URL = "http://127.0.0.1:8000/api/v1"
st.set_page_config(page_title="AI Summarizer", page_icon="📝", layout="wide")

# CSS for Sticky Tabs
st.markdown("""
<style>
    div[data-testid="stTabs"] {
        position: sticky;
        top: 0;
        z-index: 100;
        background-color: #0E1117; /* Default Dark Mode BG. Modify if using Light Mode */
        padding-top: 1rem;
    }
    @media (prefers-color-scheme: light) {
        div[data-testid="stTabs"] {
            background-color: #FFFFFF;
        }
    }
</style>
""", unsafe_allow_html=True)

st.title("📝 AI Summarizer & History")

# Create Tabs
tab1, tab2 = st.tabs(["✨ Generate Summary", "📜 History"])

# --- TAB 1: GENERATE ---
with tab1:
    st.header("Generate New Summary")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        input_text = st.text_area("Enter text to summarize:", height=300, placeholder="Paste your article here...")
        num_sentences = st.slider("Number of sentences:", min_value=1, max_value=10, value=3)
        
        generate_btn = st.button("Summarize", type="primary")

    with col2:
        if generate_btn:
            if not input_text.strip():
                st.error("Please enter some text first.")
            else:
                with st.spinner("Analyzing text..."):
                    try:
                        response = requests.post(
                            f"{API_URL}/summarize",
                            json={"text": input_text, "num_sentences": num_sentences},
                            timeout=30
                        )
                        
                        if response.status_code == 200:
                            data = response.json()
                            st.success("Summary Generated!")
                            st.subheader("Summary")
                            st.write(data["summary"])
                            
                            st.divider()
                            st.caption("MetaData")
                            st.json({
                                "original_length": data["original_length"],
                                "summary_length": data["summary_length"]
                            })
                        else:
                            st.error(f"Error {response.status_code}: {response.text}")
                    except Exception as e:
                        st.error(f"Connection Error: {e}")

# --- TAB 2: HISTORY ---
with tab2:
    st.header("Request History")
    
    if st.button("Refresh History"):
        with st.spinner("Fetching logs..."):
            try:
                response = requests.get(f"{API_URL}/history")
                if response.status_code == 200:
                    history_data = response.json()
                    
                    if not history_data:
                        st.info("No history found yet.")
                    else:
                        # Convert to DataFrame for easier handling
                        df = pd.DataFrame(history_data)
                        
                        # Display Statistics
                        st.metric("Total Requests", len(df))
                        
                        # Display List with Expanders
                        for index, row in df.iterrows():
                            # Create a clean preview string
                            timestamp = row.get('created_at', 'N/A')
                            input_preview = row.get('input_text', '')[:50] + "..."
                            summary_preview = row.get('output_summary', '')[:50] + "..."
                            
                            with st.expander(f"📝 {timestamp} | Input: {input_preview}"):
                                st.markdown("### Input Text")
                                st.text(row.get('input_text', ''))
                                
                                st.divider()
                                
                                st.markdown("### Summary Output")
                                st.info(row.get('output_summary', ''))
                                
                                st.caption(f"Model: {row.get('model_name')} | Time: {row.get('response_time_seconds', 0):.2f}s")
                
                else:
                    st.error(f"Failed to fetch history: {response.status_code}")
            except Exception as e:
                st.error(f"Connection Error: {e}")
