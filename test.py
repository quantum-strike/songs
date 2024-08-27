import re
import json
# File path
js_file_path = 'main.js'

# Function to read the existing track list from the JS file
def read_existing_entries():
    with open(js_file_path, 'r') as file:
        content = file.read()
        
        # Use regex to find the track_list definition
        match = re.search(r'let\s+track_list\s*=\s*(\[\s*.*?\s*\])', content, re.DOTALL)
        if match:
            json_text = match.group(1)
            
            # Replace single quotes with double quotes and handle other non-JSON-compliant aspects
            json_text = json_text.replace("'", '"')
            json_text = re.sub(r'(\w+):', r'"\1":', json_text)  # Convert property names to double-quoted strings
            
            try:
                return eval(json_text)
            except Exception as e:
                print(f"Error parsing JSON: {e}")
                return []
        else:
            print("Error: track_list not found.")
            return []

# Function to write the updated track list back to the JS file
def write_entries(entries):
    with open(js_file_path, 'r') as file:
        content = file.read()

    # Replace the old track_list with the new one
    updated_content = re.sub(
        r'let\s+track_list\s*=\s*\[[^\]]*\]',
        f'let track_list = {json.dumps(entries, indent=2)}',
        content,
        flags=re.DOTALL
    )

    with open(js_file_path, 'w') as file:
        file.write(updated_content)

# Function to add a new track entry
def add_entry():
    name = input("Enter the track name: ")
    artist = input("Enter the artist(s): ")
    image = input("Enter the image URL: ")
    path = input("Enter the track URL: ")

    new_entry = {
        "name": name,
        "artist": artist,
        "image": image,
        "path": path
    }

    entries = read_existing_entries()
    entries.append(new_entry)
    write_entries(entries)
    print("New entry added successfully!")

if __name__ == '__main__':
    add_entry()
