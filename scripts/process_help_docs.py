import json
import os

def process_help_docs(json_path, output_dir):
    # Load the JSON file
    if not os.path.exists(json_path):
        print(f"Error: {json_path} not found.")
        return

    with open(json_path, "r", encoding="utf-8") as f:
        docs = json.load(f)

    # Create the output folder if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Iterate through the documents and save each as a .txt file
    for doc in docs:
        filename = doc["filename"]
        content = doc["content"]
        
        file_path = os.path.join(output_dir, filename)
        
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(content)
        
        print(f"Created: {file_path}")

    print("\nHelp docs created successfully!")

if __name__ == "__main__":
    # Settings - relative to project root
    INPUT_JSON = "data/help_docs.json"
    OUTPUT_FOLDER = "data/help_docs"
    
    # Get the directory where the script is located to handle paths correctly
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    
    process_help_docs(
        os.path.join(project_root, INPUT_JSON), 
        os.path.join(project_root, OUTPUT_FOLDER)
    )
