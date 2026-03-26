from src.utils.llm_client import query_llm
from src.tools.db_tools import run_query

class Architect:
    def __init__(self):
        self.system_prompt = """You are a SQL Architect. 
        Given a schema, write a clean SQL query. 
        Return ONLY the raw SQL code. No markdown."""

    def write_sql(self, question, schema):
        prompt = f"Schema: {schema}\nQuestion: {question}"
        sql = query_llm(self.system_prompt, prompt)
        return sql.replace("```sql", "").replace("```", "").strip()

    def run_and_fix(self, question, schema):
        """Tries to run the query. If it fails, asks the LLM to fix it once."""
        sql = self.write_sql(question, schema)
        print(f"Architect attempting SQL: {sql}")
        
        result = run_query(sql)
        
        if result["status"] == "error":
            print(f"Architect noticed an error: {result['message']}. Attempting fix...")
            fix_prompt = f"The following SQL failed: {sql}\nError: {result['message']}\nRewrite the correct SQL."
            sql = query_llm(self.system_prompt, fix_prompt)
            sql = sql.replace("```sql", "").replace("```", "").strip()
            result = run_query(sql)
            
        return sql, result