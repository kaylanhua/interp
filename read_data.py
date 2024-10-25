import re
import json

def parse_data(file_path):
    with open(file_path, 'r') as file:
        content = file.read()
    
    # Split the content into separate question sets
    question_sets = re.split(r'\n\s*\n', content.strip())

    result = []
    for question_set in question_sets:
        lines = question_set.strip().split('\n')
        
        # Extract the context (last unanswered question)
        context = re.sub(r'^\d+\.\s*', '', lines[-1].strip())
        
        # Extract the prompt (answered questions) and remove numeric prefixes
        prompt = [re.sub(r'^\d+\.\s*', '', line.strip()) for line in lines[1:-1]]
        
        result.append({
            "prompt": context,
            "context": prompt
        })

    return result

# Parse the data
data = parse_data('data.txt')

# Save the result to a JSON file
output_file = 'processed_data.json'
with open(output_file, 'w') as json_file:
    json.dump(data, json_file, indent=2)

print(f"Data has been processed and saved to {output_file}")
