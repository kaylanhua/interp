import json

def reconstruct_prompts():
    # Read the processed data from the JSON file
    with open('processed_data.json', 'r') as file:
        data = json.load(file)

    reconstructed_prompts = []

    for index, item in enumerate(data, start=1):
        prompt = [f"Consider the following information."]
        
        # Add the context (answered questions) with numbering
        for i, question in enumerate(item['context'], start=1):
            prompt.append(f"   {i}. {question}")
        
        # Add the unanswered question
        prompt.append(f"   {len(item['context']) + 1}. {item['prompt']}")
        
        # Join the prompt lines and add to the list
        reconstructed_prompts.append("\n".join(prompt))

    # Join all reconstructed prompts with double newlines
    return "\n\n".join(reconstructed_prompts)

# Use the function and print the result
if __name__ == "__main__":
    reconstructed_data = reconstruct_prompts()
    print(reconstructed_data)

    # Optionally, save the reconstructed data to a new file
    with open('reconstructed_data.txt', 'w') as file:
        file.write(reconstructed_data)
    print("Reconstructed data has been saved to 'reconstructed_data.txt'")

