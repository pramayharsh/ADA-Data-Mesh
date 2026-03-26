from src.tools.setup_db import download_db
from src.tools.db_tools import get_db_schema, run_query
from src.utils.llm_client import query_llm

def main():
    # 1. Initialize DB
    download_db()
    
    # 2. Get Data Context
    schema = get_db_schema()
    
    # 3. Ask a question
    user_question = "How many tracks are there in the database?"
    
    system_prompt = """
    You are a SQL expert. 
    Return ONLY the raw SQL query. 
    Do not include markdown code blocks (like ```sql). 
    Do not include any explanations.
    """
    user_prompt = f"Schema: {schema}\nQuestion: {user_question}"
    
    print(f"Asking Groq: {user_question}")
    sql = query_llm(system_prompt, user_prompt).strip()
    
    # Simple cleaning in case the LLM still includes markdown
    sql = sql.replace("```sql", "").replace("```", "").strip()
    
    print(f"Groq generated SQL: {sql}")
    
    # 4. Run it
    result = run_query(sql)
    
    if result["status"] == "success":
        print(f"Result from Database: {result['data']}")
    else:
        print(f"Error: {result['message']}")

if __name__ == "__main__":
    main()