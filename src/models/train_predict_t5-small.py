# -*- coding: utf-8 -*-
"""train-predict_t5-small.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/18shvaqlHkTW1OIFxZu2pbhjf0CggcsYz
"""

import os

repo_dir = "nlp-Text-De-toxification"

if os.path.exists(repo_dir):
    print(f"{repo_dir} already exists. Removing it...\n")
    !rm -r {repo_dir}

# Clone the repository from GitHub
!git clone https://github.com/Goshmar/nlp-Text-De-toxification

! pip install -r nlp-Text-De-toxification/requirements.txt -q

import pandas as pd
import requests
import zipfile

# Define the paths
dataset_url = "https://github.com/skoltech-nlp/detox/releases/download/emnlp2021/filtered_paranmt.zip"
zip_file_path = "dataset.zip"
csv_file_path, tsv_file_path = "dataset.csv", "filtered.tsv"

# Download the ZIP file
response = requests.get(dataset_url)
if response.status_code == 200:
    with open(zip_file_path, 'wb') as file:
        file.write(response.content)
else:
    print("Attempt failed")
    exit()

with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
    zip_ref.extractall(".")

dataset = pd.read_csv("filtered.tsv", delimiter='\t')
dataset.to_csv(csv_file_path, index=False)

# ZIP cleaning up
os.remove(zip_file_path)
os.remove(tsv_file_path)

from transformers import T5ForConditionalGeneration, T5Tokenizer
from sklearn.model_selection import train_test_split


# Split the dataset into training and validation sets
train_data, val_data = train_test_split(dataset, test_size=0.1, random_state=42)

# Define the T5 model and tokenizer
model_name = "t5-small"
tokenizer = T5Tokenizer.from_pretrained(model_name)
model = T5ForConditionalGeneration.from_pretrained(model_name)

# Tokenize and preprocess the data
def preprocess_data(data):
    input_text = data['reference'].apply(lambda x: "detoxify: " + x + " </s>")
    target_text = data['translation'].apply(lambda x: x + " </s>")

    input_text = list(input_text)
    target_text = list(target_text)

    inputs = tokenizer(input_text, return_tensors="pt", padding=True, truncation=True, max_length=128)
    targets = tokenizer(target_text, return_tensors="pt", padding=True, truncation=True, max_length=128)

    return inputs, targets

train_inputs, train_targets = preprocess_data(train_data)
val_inputs, val_targets = preprocess_data(val_data)

# Define a function for training the model
def train(model, train_inputs, train_targets, val_inputs, val_targets, num_epochs=5, batch_size=32, learning_rate=1e-4):
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model.to(device)

    optimizer = torch.optim.AdamW(model.parameters(), lr=learning_rate)

    for epoch in range(num_epochs):
        print(f"Epoch {epoch+1}/{num_epochs}")

        model.train()
        for i in range(0, len(train_inputs['input_ids']), batch_size):
            input_batch = {key: value[i:i+batch_size].to(device) for key, value in train_inputs.items()}
            target_batch = {key: value[i:i+batch_size].to(device) for key, value in train_targets.items()}

            optimizer.zero_grad()
            loss = model(**input_batch, labels=target_batch['input_ids']).loss
            loss.backward()
            optimizer.step()

        model.eval()
        with torch.no_grad():
            val_loss = 0.0
            for i in range(0, len(val_inputs['input_ids']), batch_size):
                input_batch = {key: value[i:i+batch_size].to(device) for key, value in val_inputs.items()}
                target_batch = {key: value[i:i+batch_size].to(device) for key, value in val_targets.items()}

                loss = model(**input_batch, labels=target_batch['input_ids']).loss
                val_loss += loss.item()

        val_loss /= (len(val_inputs['input_ids']) / batch_size)
        print(f"Validation Loss: {val_loss:.4f}")

# Train the model
train(model, train_inputs, train_targets, val_inputs, val_targets, num_epochs=20)

import warnings
warnings.filterwarnings('ignore')

# Detoxify a sample sentence
def detoxify_sentence(sentence):
    input_text = "detoxify: " + sentence + " </s>"
    input_ids = tokenizer(input_text, return_tensors="pt", max_length=128).input_ids.to(model.device)

    with torch.no_grad():
        output_ids = model.generate(input_ids, max_length=128, num_return_sequences=1, no_repeat_ngram_size=2)

    detoxified_text = tokenizer.decode(output_ids[0], skip_special_tokens=True)
    return detoxified_text

dataset = pd.read_csv("/content/nlp-Text-De-toxification/data/interim/dataset_cropped.csv")
for example in dataset['reference'].sample(3):
    print("------")
    print(example)
    print("-->", detoxify_sentence(example))
    print("------\n\n")

