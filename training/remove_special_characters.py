import re
import sys

# Define a dictionary mapping special characters to their normal counterparts
special_chars = {
    'à': 'a', 'á': 'a', 'â': 'a', 'ä': 'a', 'ã': 'a', 'å': 'a', 'ā': 'a',
    'è': 'e', 'é': 'e', 'ê': 'e', 'ë': 'e', 'ē': 'e',
    'ì': 'i', 'í': 'i', 'î': 'i', 'ï': 'i', 'ī': 'i',
    'ò': 'o', 'ó': 'o', 'ô': 'o', 'ö': 'o', 'õ': 'o', 'ø': 'o', 'ō': 'o',
    'ù': 'u', 'ú': 'u', 'û': 'u', 'ü': 'u', 'ū': 'u',
    'ç': 'c', 'ñ': 'n', 'ß': 'ss', 'ÿ': 'y'
}

# Function to replace special characters
def replace_special_chars(text):
    for char, replacement in special_chars.items():
        text = text.replace(char, replacement)
    return text

def main(input_file, output_file):
    # Read the content of the file
    with open(input_file, 'r', encoding='utf-8') as file:
        content = file.read()

    # Replace special characters
    new_content = replace_special_chars(content)

    # Write the modified content back to the file
    with open(output_file, 'w', encoding='utf-8') as file:
        file.write(new_content)

    print("Special characters replaced successfully.")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script.py <input_file> <output_file>")
    else:
        input_file = sys.argv[1]
        output_file = sys.argv[2]
        main(input_file, output_file)