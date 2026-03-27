import streamlit as st
import pandas as pd
import os
from src.tools.db_tools import get_db_schema
from src.agents.librarian import Librarian
from src.agents.architect import Architect
from src.agents.analyst import Analyst
from src.agents.storyteller import Storyteller

# --- INITIALIZATION ---
st.set_page_config(page_title="ADA: Autonomous Data Analyst", layout="wide")
st.title("🤖 ADA: Autonomous Data Analyst")
st.markdown("---")

# Initialize Agents once (Cached for performance)
@st.cache_resource
def init_agents():
    schema = get_db_schema()
    lib = Librarian(schema)
    lib.build_index()
    return lib, Architect(), Analyst(), Storyteller()

librarian, architect, analyst, storyteller = init_agents()

# --- SIDEBAR: Agent Chatter ---
st.sidebar.title("🧠 Agent Thought Process")
chatter_placeholder = st.sidebar.empty()

def log_chatter(message):
    if "chatter_log" not in st.session_state:
        st.session_state.chatter_log = ""
    st.session_state.chatter_log += f"{message}\n\n"
    chatter_placeholder.markdown(st.session_state.chatter_log)

# --- MAIN UI: Chat ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if "chart" in message:
            st.image(message["chart"])
        if "data" in message:
            st.dataframe(message["data"])

# User input
if prompt := st.chat_input("Ask me about your data..."):
    # Add user message to history
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # --- AGENTIC FLOW ---
    with st.chat_message("assistant"):
        with st.spinner("Analyzing..."):
            # 1. Librarian
            relevant_schema = librarian.get_relevant_schema(prompt)
            log_chatter(f"**Librarian:** Found relevant tables: `{list(relevant_schema.keys())}`")
            
            # 2. Architect
            sql, result = architect.run_and_fix(prompt, relevant_schema)
            
            if result["status"] == "success":
                log_chatter(f"**Architect:** Generated SQL:\n```sql\n{sql}\n```")
                
                # 3. Analyst (Viz)
                viz_code = analyst.generate_viz_code(prompt, result["data"], result["columns"])
                try:
                    # Clean the data/ folder for fresh charts
                    if os.path.exists("data/output_chart.png"):
                        os.remove("data/output_chart.png")
                        
                    exec(viz_code, {"pd": pd, "plt": __import__('matplotlib.pyplot')})
                    chart_path = "data/output_chart.png"
                except Exception as e:
                    log_chatter(f"**Analyst Error:** {e}")
                    chart_path = None

                # 4. Storyteller
                insight = storyteller.explain(prompt, result["data"])
                
                # FINAL DISPLAY
                st.markdown(insight)
                if chart_path and os.path.exists(chart_path):
                    st.image(chart_path)
                
                df_result = pd.DataFrame(result["data"], columns=result["columns"])
                st.dataframe(df_result)

                # Store history
                history_entry = {
                    "role": "assistant", 
                    "content": insight, 
                    "data": df_result
                }
                if chart_path: history_entry["chart"] = chart_path
                st.session_state.messages.append(history_entry)

            else:
                st.error(f"Architect Error: {result['message']}")
                log_chatter(f"**Architect Failed:** {result['message']}")