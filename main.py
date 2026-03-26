from src.tools.db_tools import get_db_schema
from src.agents.librarian import Librarian
from src.agents.architect import Architect

def main():
    # 1. Setup Agents
    full_schema = get_db_schema()
    librarian = Librarian(full_schema)
    architect = Architect()
    
    # Index the database (Only happens once)
    librarian.build_index()
    
    # 2. User Interaction
    user_question = "Which artist has the most tracks in the database?"
    print(f"\nUser: {user_question}")
    
    # 3. Librarian finds relevant tables
    relevant_schema = librarian.get_relevant_schema(user_question)
    print(f"Librarian selected tables: {list(relevant_schema.keys())}")
    
    # 4. Architect writes and executes SQL
    sql, result = architect.run_and_fix(user_question, relevant_schema)
    
    if result["status"] == "success":
        print(f"Final SQL: {sql}")
        print(f"Result: {result['data']}")
    else:
        print(f"System failed to answer: {result['message']}")

if __name__ == "__main__":
    main()