import os
import pandas as pd
import matplotlib.pyplot as plt
from src.tools.db_tools import get_db_schema
from src.agents.librarian import Librarian
from src.agents.architect import Architect
from src.agents.analyst import Analyst
from src.agents.storyteller import Storyteller

def main():
    # 1. Initialize the Mesh
    print("--- ADA: Autonomous Data Analyst Initializing ---")
    full_schema = get_db_schema()
    librarian = Librarian(full_schema)
    architect = Architect()
    analyst = Analyst()
    storyteller = Storyteller()
    
    librarian.build_index()
    print("--- System Ready. Type 'exit' to quit. ---")

    while True:
        # 2. Interactive Input
        user_question = input("\n[User]: ")
        
        if user_question.lower() in ["exit", "quit", "q"]:
            print("Goodbye!")
            break
            
        if not user_question.strip():
            continue

        # 3. Librarian (RAG)
        relevant_schema = librarian.get_relevant_schema(user_question)
        print(f"[Librarian]: Identified relevant tables: {list(relevant_schema.keys())}")
        
        # 4. Architect (SQL)
        sql, result = architect.run_and_fix(user_question, relevant_schema)
        
        if result["status"] == "success":
            print(f"[Architect]: Query Successful.")
            
            # 5. Analyst (Python Viz)
            print("[Analyst]: Generating visualization...")
            viz_code = analyst.generate_viz_code(user_question, result["data"], result["columns"])
            
            # EXECUTE the generated code
            try:
                # We provide a clean dictionary for the exec environment
                exec(viz_code, {"pd": pd, "plt": plt})
                print("[System]: Chart updated at data/output_chart.png")
            except Exception as e:
                print(f"[Analyst Error]: Could not generate chart: {e}")
                
            # 6. Storyteller (Narrative)
            insight = storyteller.explain(user_question, result["data"])
            print(f"\n[Storyteller Insight]: {insight}")
            
        else:
            print(f"[Architect Error]: {result['message']}")

if __name__ == "__main__":
    main()