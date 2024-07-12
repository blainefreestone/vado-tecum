import json
import random

# Initialize a dictionary to store the counts and lines
counts = {}
lines_by_pos = {}

pos_types = [
    'verb', 'adv', 'adj', 'noun', 'prefix' 'name', 'intj', 'prep', 'conj', 'pron', 
    'phrase', 'num', 'particle', 'proverb', 'suffix', 'prep_phrase', 
    'article', 'postp', 'det', 'contraction', 'interfix', 'infix', 
    'circumfix'
]

# Open the JSONL file and read its contents with UTF-8 encoding
with open('resources/latin-wiktionary.jsonl', 'r', encoding='utf-8') as file:  # Replace with the actual file path
    for line in file:
        # Parse the line as a JSON object
        data = json.loads(line)
        # Extract the value associated with the "pos" key
        pos_string = data.get('pos')
        if pos_string:
            if pos_string in counts:
                counts[pos_string] += 1
            else:
                counts[pos_string] = 1
            
            # Store the line in the corresponding pos list
            if pos_string in pos_types:
                if pos_string not in lines_by_pos:
                    lines_by_pos[pos_string] = []
                lines_by_pos[pos_string].append(data)

# Randomly select 2 lines from each specified pos type and save them to a new file
selected_lines = []
for pos in pos_types:
    if pos in lines_by_pos:
        selected_lines.extend(random.sample(lines_by_pos[pos], min(2, len(lines_by_pos[pos]))))

# Write the selected lines to a new file with proper formatting
with open('resources/selected_lines.json', 'w', encoding='utf-8') as output_file:
    json.dump(selected_lines, output_file, indent=4, ensure_ascii=False)