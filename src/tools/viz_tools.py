import pandas as pd
import matplotlib.pyplot as plt
import os

def save_chart(df, chart_type, title, filename="output_chart.png"):
    """
    A simple sandbox tool that the Analyst Agent can 'call' 
    by writing code that uses this function.
    """
    plt.figure(figsize=(10, 6))
    
    if chart_type == "bar":
        df.plot(kind='bar', x=df.columns[0], y=df.columns[1], legend=False)
    elif chart_type == "line":
        df.plot(kind='line', x=df.columns[0], y=df.columns[1])
    
    plt.title(title)
    plt.xticks(rotation=45)
    plt.tight_layout()
    
    output_path = f"data/{filename}"
    plt.savefig(output_path)
    plt.close()
    return output_path