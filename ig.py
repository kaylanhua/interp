import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from captum.attr import IntegratedGradients
import json
import os

model_name = "gpt2"
model = AutoModelForCausalLM.from_pretrained(model_name)
tokenizer = AutoTokenizer.from_pretrained(model_name)
model.eval()

def model_wrapper(inputs_embeds):
    outputs = model(inputs_embeds=inputs_embeds)
    return outputs.logits[:, -1, :]

def load_augmented_data(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

def perform_ig(input_text, target_token):
    input_ids = tokenizer.encode(input_text, return_tensors='pt')
    inputs_embeds = model.get_input_embeddings()(input_ids)

    target_token_id = tokenizer.encode(target_token)[-1]

    # Create a baseline of the same length as the input
    baseline_input_ids = torch.zeros_like(input_ids)
    baseline_embeds = model.get_input_embeddings()(baseline_input_ids)

    ig = IntegratedGradients(model_wrapper)

    attributions, delta = ig.attribute(
        inputs_embeds,
        baselines=baseline_embeds,
        target=target_token_id,
        n_steps=50,
        return_convergence_delta=True
    )

    tokens = tokenizer.convert_ids_to_tokens(input_ids[0])
    attributions_sum = attributions.sum(dim=-1).squeeze().tolist()

    return tokens, attributions_sum, delta.item()  # Convert delta to a Python scalar

def process_file(file_path, augmented_data):
    with open(file_path, 'r') as file:
        content = file.read()

    examples = content.split('\n\n')
    results = []

    for example in examples:
        lines = example.split('\n')
        context = '\n'.join(lines[1:-1])  # Skip the first line and the last line
        question = lines[-1].split('. ')[-1]  # Get the question part
        
        print(f"Processing question: {question}")
        # Find the corresponding augmented data item
        augmented_item = next((item for item in augmented_data if item['prompt'] == question), None)
        
        if augmented_item:
            target_token = augmented_item['target']
            print(f"Found target token: {target_token}")
        else:
            print(f"Warning: No matching augmented data found for question: {question}")
            continue

        input_text = context + '\n' + question
        tokens, attributions, delta = perform_ig(input_text, target_token)

        results.append({
            'input': input_text,
            'target_token': target_token,
            'tokens': tokens,
            'attributions': attributions,
            'delta': delta
        })
        break

    return results

def main():
    permuted_folder = 'permuted'
    output_folder = 'ig_results'
    augmented_data_file = 'augmented_data.json'

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    augmented_data = load_augmented_data(augmented_data_file)

    for filename in os.listdir(permuted_folder):
        if filename.endswith('.txt'):
            file_path = os.path.join(permuted_folder, filename)
            results = process_file(file_path, augmented_data)

            output_file = os.path.join(output_folder, f'ig_{filename[:-4]}.json')
            with open(output_file, 'w') as f:
                json.dump(results, f, indent=2)

            print(f"Processed {filename} and saved results to {output_file}")

if __name__ == "__main__":
    main()
