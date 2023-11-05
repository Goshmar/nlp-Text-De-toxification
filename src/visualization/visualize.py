# -*- coding: utf-8 -*-
"""visualize.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1gZPBe6QQ6kr0gMzkKG-SOq042BXaHOgn
"""

# Paradetox metric implementation

inputs = ["Great idea, yeah, Cyril. Let's give an M-16 to a bunch of wild Indians!",
         "Looks like she left in a hurry, or she's just a filthy pig.",
         "You're stepping on it! - Shut up."]

preds_t5 = ["great idea, yeah, cyril. we're going to give a bunch of wild Indians a sixteenth.",
          "looks like she left in a hurry, or she's just a a terrible mess.",
          "be out! you're stepping on it!"]

preds_condbert = ["we're going to give a bunch of wild Indians a sixteenth.",
          "she left in a hurry, she just a terrible mess.",
          "watching out! you're stepping!"]

!pip install transformers

from transformers import RobertaTokenizer, RobertaForSequenceClassification
from tqdm.auto import tqdm
import numpy as np

r_tokenizer = RobertaTokenizer.from_pretrained('SkolkovoInstitute/roberta_toxicity_classifier')
r_model = RobertaForSequenceClassification.from_pretrained('SkolkovoInstitute/roberta_toxicity_classifier')

def classify_preds_toxicity(preds, batch_size=16):
    results = []

    for i in tqdm(range(0, len(preds), batch_size)):
        batch = r_tokenizer(preds[i:i + batch_size], return_tensors='pt', padding=True)
        result = (r_model(**batch)['logits'] / 2.5).softmax(dim=1)[:,1].data.tolist()
        results.extend([1 - item for item in result])

    return np.array(results)

non_toxixty_t5 = classify_preds_toxicity(preds_t5)
non_toxixty_condbert = classify_preds_toxicity(preds_condbert)

from nltk.translate.bleu_score import sentence_bleu

def calc_bleu(inputs, preds):
    results = []
    for i in range(len(inputs)):
        results.append(sentence_bleu([inputs[i]], preds[i]))

    return np.array(results)

bleu_t5 = calc_bleu(inputs, preds_t5)
bleu_condbert = calc_bleu(inputs, preds_condbert)

# Load model directly
from transformers import AutoTokenizer, AutoModelForSequenceClassification

cola_tokenizer = AutoTokenizer.from_pretrained("textattack/roberta-base-CoLA")
cola_model = AutoModelForSequenceClassification.from_pretrained("textattack/roberta-base-CoLA")


def classify_cola(preds, batch_size=16):
    results = []

    for i in tqdm(range(0, len(preds), batch_size)):
        batch = cola_tokenizer(preds[i:i + batch_size], return_tensors='pt', padding=True)
        result = (cola_model(**batch)['logits']).softmax(dim=1)[:,1].data.tolist()
        results.extend(result)

    return np.array(results)

cola_t5 = classify_cola(preds_t5)
cola_condbert = classify_cola(preds_condbert)

print("Final score for the T5-small model", (non_toxixty_t5 * bleu_t5 * cola_t5).sum() / len(preds_t5))
print("Final score for the CondBERT model", (non_toxixty_condbert * bleu_condbert * cola_condbert).sum() / len(preds_condbert))

