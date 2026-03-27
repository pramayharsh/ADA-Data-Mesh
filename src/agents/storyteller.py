from src.utils.llm_client import query_llm

class Storyteller:
    def __init__(self):
        self.system_prompt = "You are a Business Intelligence Analyst. Summarize the data findings into a single, punchy insight for a CEO."

    def explain(self, question, data):
        prompt = f"Question: {question}\nData: {data}\nProvide a brief, professional insight."
        return query_llm(self.system_prompt, prompt)