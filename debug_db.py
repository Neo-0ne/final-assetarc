import os
import sys

# Change the working directory and add the app folder to the path.
os.chdir('Services/eng-lifecycle/app')
sys.path.insert(0, '.')

try:
    from app import init_db, engine
    print(f"Database engine is configured for: {engine.url}")
    print("Import successful.")

    print("Attempting to initialize database...")
    init_db()
    print("Database initialization function called successfully.")

    # Check if the file was created in the app directory
    if os.path.exists('eng_lifecycle.db'):
        print("Database file was created successfully in Services/eng-lifecycle/app/")
    else:
        # Since the path in app.py is now absolute, check there too
        if os.path.exists('/app/eng_lifecycle.db'):
             print("Database file was created successfully at /app/eng_lifecycle.db")
        else:
             print("Database file was NOT created in either location.")

except Exception as e:
    print(f"An error occurred: {e}")
