import json
import openai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set up OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

def load_data(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

def get_gpt_answer(prompt):
    try:
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that provides one or two word answers to questions."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=50,
            n=1,
            stop=None,
            temperature=0.7,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Error getting GPT answer: {e}")
        return None

def augment_data(data):
    augmented_data = []
    for item in data:
        context = item['context']
        prompt = item['prompt']
        
        # Construct the full prompt for GPT
        full_prompt = "Given the following context:\n"
        for ctx in context:
            full_prompt += f"- {ctx}\n"
        full_prompt += f"\nAnswer the following question in ONE or TWO words: {prompt}"
        
        # Get the answer from GPT
        answer = get_gpt_answer(full_prompt)
        
        # Create the augmented item
        augmented_item = {
            "context": context,
            "prompt": prompt,
            "target": answer
        }
        augmented_data.append(augmented_item)
    
    return augmented_data

def save_augmented_data(data, file_path):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=2)

def main():
    input_file = 'processed_data.json'
    output_file = 'augmented_data.json'
    
    # Load the processed data
    data = load_data(input_file)
    
    # Augment the data with GPT-generated answers
    augmented_data = augment_data(data)
    
    # Save the augmented data
    save_augmented_data(augmented_data, output_file)
    
    print(f"Augmented data has been saved to '{output_file}'")

if __name__ == "__main__":
    main()

