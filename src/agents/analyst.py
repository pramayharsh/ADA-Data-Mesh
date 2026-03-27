from src.utils.llm_client import query_llm

class Analyst:
    def __init__(self):
        self.system_prompt = """
        You are a Data Scientist. You receive JSON data and a user question.
        Your job is to write a Python script that:
        1. Imports pandas and matplotlib.pyplot.
        2. Loads the data into a Pandas DataFrame.
        3. Creates a professional chart.
        4. Uses plt.savefig('data/output_chart.png').
        
        Return ONLY the Python code. No explanations.
        """

    def generate_viz_code(self, question, data, columns):
        # Format data for the prompt
        data_str = str(data)
        cols_str = str(columns)
        
        user_prompt = f"""
        User Question: {question}
        Data: {data_str}
        Columns: {cols_str}
        
        Write Python code to visualize this. Use plt.savefig('data/output_chart.png').
        """
        
        code = query_llm(self.system_prompt, user_prompt)
        return code.replace("```python", "").replace("```", "").strip()