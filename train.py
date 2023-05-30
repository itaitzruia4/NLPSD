from transformers import AutoModelForSequenceClassification, AutoTokenizer
import torch
import torch.nn as nn
from sklearn.model_selection import train_test_split
import pandas as pd

transfer_learning = False

class Dataset(torch.utils.data.Dataset):
    def __init__(self, texts, labels):
        self.texts = texts
        self.labels = labels

    def __getitem__(self, index):
        text = self.texts[index]
        label = self.labels[index]
        return text, label
    
    def __len__(self):
        return len(self.texts)
    
alephbert_tokenizer = AutoTokenizer.from_pretrained('onlplab/alephbert-base')
alephbert = AutoModelForSequenceClassification.from_pretrained('onlplab/alephbert-base', num_labels=2)

# Freeze the weights of the model
if transfer_learning:
    for param in list(alephbert.parameters())[:-1]:
        param.requires_grad = False

agg_scores_df = pd.read_csv('agg_score_bin.csv')
agg_scores_df.dropna(inplace=True, ignore_index=True)

train_set, test_set = train_test_split(agg_scores_df, test_size=0.2)

# Reset the index of each DataFrame
train_set.reset_index(drop=True, inplace=True)
test_set.reset_index(drop=True, inplace=True)

agg_train = Dataset(train_set['text'], train_set['score'])
agg_test = Dataset(test_set['text'], test_set['score'])

train_dataloader = torch.utils.data.DataLoader(agg_train, batch_size=16, shuffle=True)
test_dataloader = torch.utils.data.DataLoader(agg_test, batch_size=16, shuffle=False)

# Set device
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
alephbert.to(device)

# Set optimizer and loss function
optimizer = torch.optim.Adam(alephbert.parameters(), lr=5e-5)
criterion = nn.CrossEntropyLoss()

# Train model
alephbert.train()
for epoch in range(5):
    for texts, scores in train_dataloader:
        optimizer.zero_grad()
        scores = scores.long().to(device)
        inputs = alephbert_tokenizer(texts, padding=True, truncation=True, return_tensors='pt').to(device)
        outputs = alephbert(**inputs, return_dict=False)[0]

        loss = criterion(outputs, scores)
        loss.backward()
        optimizer.step()

# Evaluate model
alephbert.eval()

total = 0
correct = 0

with torch.no_grad():
    for texts, scores in test_dataloader:
        inputs = alephbert_tokenizer(texts, padding=True, truncation=True, return_tensors='pt').to(device)
        scores = scores.to(device)

        outputs = alephbert(**inputs, return_dict=False)[0]
        _, predicted = torch.max(outputs.data, 1)
        total += scores.size(0)
        correct += (predicted == scores).sum().item()

print('total accuracy on test set:', correct/total)

torch.save(alephbert, 'model.pt')