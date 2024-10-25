import json
from itertools import permutations
import os

def load_data(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

def generate_permutations(data):
    permuted_data = []
    for item in data:
        context = item['context']
        prompt = item['prompt']

        # Generate permutations of 3 questions
        perms_3 = list(permutations(context, 3))
        
        # Generate permutations of 2 questions
        perms_2 = list(permutations(context, 2))

        # Combine all permutations
        all_perms = perms_3 + perms_2

        for perm in all_perms:
            permuted_item = {
                'context': list(perm),
                'prompt': prompt
            }
            permuted_data.append(permuted_item)

    return permuted_data

def format_output(permuted_data):
    output = []
    for item in permuted_data:
        prompt = ["Consider the following information."]
        for i, question in enumerate(item['context'], start=1):
            prompt.append(f"   {i}. {question}")
        prompt.append(f"   {len(item['context']) + 1}. {item['prompt']}")
        output.append("\n".join(prompt))
    return "\n\n".join(output)

def save_output(output, file_path):
    with open(file_path, 'w') as file:
        file.write(output)

def main():
    input_file = 'processed_data.json'
    output_file = 'permuted_data.txt'

    data = load_data(input_file)
    permuted_data = generate_permutations(data)
    formatted_output = format_output(permuted_data)
    save_output(formatted_output, output_file)

    print(f"Permuted data has been saved to '{output_file}'")

if __name__ == "__main__":
    main()

