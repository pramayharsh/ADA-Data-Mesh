import sqlite3
import urllib.request
import os
import ssl  # Add this

def download_db():
    url = "https://raw.githubusercontent.com/lerocha/chinook-database/master/ChinookDatabase/DataSources/Chinook_Sqlite.sqlite"
    os.makedirs("data", exist_ok=True)
    db_path = "data/chinook.db"
    
    if not os.path.exists(db_path):
        print("Downloading Chinook database...")
        # This bypasses the SSL certificate verification
        context = ssl._create_unverified_context()
        
        with urllib.request.urlopen(url, context=context) as response, open(db_path, 'wb') as out_file:
            out_file.write(response.read())
            
        print(f"Database downloaded to {db_path}.")
    else:
        print("Database already exists.")

if __name__ == "__main__":
    download_db()