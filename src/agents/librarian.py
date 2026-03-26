import json
import os
from src.utils.embeddings import get_embedding, cosine_similarity
from src.utils.llm_client import query_llm

class Librarian:
    def __init__(self, schema):
        self.schema = schema # Dict of {table: [cols]}
        self.index_path = "data/schema_index.json"
        self.metadata = {}

    def build_index(self):
        """Generates descriptions and embeddings for every table in the DB."""
        if os.path.exists(self.index_path):
            with open(self.index_path, 'r') as f:
                self.metadata = json.load(f)
            return

        print("Librarian is cataloging the library (indexing database)...")
        for table_name, columns in self.schema.items():
            # 1. Ask LLM to describe the table
            prompt = f"Table: {table_name}\nColumns: {columns}\nBriefly describe what this table stores."
            description = query_llm("You are a database librarian.", prompt)
            
            # 2. Get vector for that description
            vector = get_embedding(description)
            
            self.metadata[table_name] = {
                "description": description,
                "columns": columns,
                "vector": vector
            }
        
        with open(self.index_path, 'w') as f:
            json.dump(self.metadata, f)

    def get_relevant_schema(self, user_query):
        """Finds the top 3 tables most relevant to the user's question."""
        query_vector = get_embedding(user_query)
        scores = []
        
        for table_name, info in self.metadata.items():
            score = cosine_similarity(query_vector, info['vector'])
            scores.append((table_name, score))
        
        # Sort by similarity score
        sorted_tables = sorted(scores, key=lambda x: x[1], reverse=True)[:3]
        
        relevant_schema = {}
        for table_name, _ in sorted_tables:
            relevant_schema[table_name] = self.metadata[table_name]['columns']
            
        return relevant_schema