import os
import json
import re
import matplotlib.pyplot as plt


# Define the directory containing your JSON files
directory = "/Users/theodatta/Downloads/interp/ig_results"

# Function to extract individual example prompts from input text
def extract_prompts(text):
    # Use regex to split the text into examples starting with "number + period" and ending at the next newline
    # Example: r'\d\.\s+.*?(?=\n)'
    pattern = r'\d\.\s+.*?(?=\n|$)'
    return re.findall(pattern, text, re.DOTALL)

# Initialize a list to hold the average attribution scores for each prompt
prompt_avg_attributions = []

# Function to check if a token represents a number followed by a period (e.g., "1.")
def is_number_period_token(token):
    return re.match(r'^\d+\.$', token)

# Helper function to calculate the average attributions between two indexes
# Helper function to calculate the average attributions between two indexes
def calculate_average_attribution(start_idx, end_idx, attributions):
    # Ensure start_idx and end_idx are integers
    if not isinstance(start_idx, int) or not isinstance(end_idx, int):
        raise ValueError(f"Indices must be integers. Got start_idx={start_idx}, end_idx={end_idx}")

    # Extract the attributions for the tokens between the number and the newline
    attribution_slice = attributions[start_idx:end_idx]
    
    # Calculate the average attribution for this range
    if len(attribution_slice) > 0:
        return sum(attribution_slice) / len(attribution_slice)
    else:
        return 0

averages_first = []
averages_second = []
averages_third = []

# Loop through all JSON files in the directory
for filename in os.listdir(directory):
    if filename.endswith(".json"):  # Check for JSON files
        file_path = os.path.join(directory, filename)

        # Open and load the JSON file
        with open(file_path, 'r') as json_file:
            data = json.load(json_file)
            
            # Iterate through each entry in the JSON file
            for entry in data:
                input_text = entry["input"]
                tokens = entry["tokens"]
                attributions = entry["attributions"]
                
                # Lists to store number-period tokens and newline tokens
                number_period_tokens = []
                newline_tokens = []

                # Loop through the tokens array to find number followed by period tokens and \n
                i = 0
                while i < len(tokens):
                    token = tokens[i]
                    print(token)
                    # Check if the current token is a number and the next token is a period
                    if ((token == '\u01201') or (token == '\u01202') or (token == '\u01203') ) and tokens[i + 1] == ".":
                        # Store the index and the combined token (number and period)
                        number_period_tokens.append(i + 2) # the +2 is what changes this
                        i += 2  # Skip the next token (the period)
                    elif token == "\u010a":
                        # Store the index and the token if it's a newline
                        newline_tokens.append(i - 1) # the -1 is what changes this
                        i += 1
                    else:
                        i += 1
                
                averages_first.append(calculate_average_attribution(number_period_tokens[0], newline_tokens[0], attributions))
                averages_second.append(calculate_average_attribution(number_period_tokens[1], newline_tokens[1], attributions))
                averages_third.append(calculate_average_attribution(number_period_tokens[2], newline_tokens[2], attributions))


                
                

# Calculate the means for each prompt
mean_first = sum(averages_first) / len(averages_first)
mean_second = sum(averages_second) / len(averages_second)
mean_third = sum(averages_third) / len(averages_third)

# Data for the bar chart
prompts = ['First Prompt', 'Second Prompt', 'Third Prompt']
means = [mean_first, mean_second, mean_third]

# Plot the bar chart
plt.figure(figsize=(8, 5))
plt.bar(prompts, means, color='mediumseagreen')

# Add a horizontal line at y=0 to emphasize it
plt.axhline(0, color='black', linewidth=1.5, linestyle='--')

# Add labels and title
plt.ylabel('Average Attribution')
plt.title('Average Attribution for First, Second, and Third Prompts (No Numbering)')

# Show the plot
plt.show()