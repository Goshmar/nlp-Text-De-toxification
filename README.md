# Practical Machine Learning and Deep Learning - Text De-toxification

_Georgii Budnik, g.budnik@innopolis.university
BS21-AI-01_

## Task description

Text Detoxification Task is a process of transforming the text with toxic style into the text with the same meaning but with neutral style. My goal is to 
create a solution for detoxing text with high level of toxicity. It can be a model or set of models, or any algorithm that would work. 

## Basic pipline (comands)

1. Prepare the data using make_dataset file (```/src/data/make_dataset.py```)
2. After that, take all the data you need from the "environment" of the models and start training (```/src/models```)
3. So, you can start train-predict models (```/models/train-predict_model.ipynb```)
4. As a result, you will get a function to run the detoxifier, which runs on a cropped dataset (```/data/interim/dataset_cropped.csv```). We can run this version by testing the answers to the metrics (```/src/visualization/visualize.py```), making sure that the reports (```/reports```) are fair

## Repository structure

Repository has the following structure:

```
nlp-Text-De-toxification
├── README.md # Short info about projects
│
├── data 
│   ├── external # Reference's data
│   ├── interim  # Prepared/transformed data
│   └── raw      # The initially data
│
├── models       # Final checkpoints models
│
├── notebooks    # Jupyter models notebooks         
│ 
├── references   # Key explanatory papers
│
├── reports      
│   └── figures  # The result of the work done
│
├── requirements.txt # The requirements file
│                 
└── src                 # Source code for using
    │                 
    ├── data            # Scripts to download/generate data
    │   └── make_dataset.py
    │
    ├── models          # Scripts to train-predict models
    │   └── train-predict_model.py
    │   
    └── visualization   # Scripts to create metrics comparison data
        └── visualize.py
```
