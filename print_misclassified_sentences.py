import torch
import pandas as pd
from transformers import AutoTokenizer
from sklearn.model_selection import train_test_split

class MyDataset(torch.utils.data.Dataset):
    def __init__(self, texts, labels):
        self.texts = texts
        self.labels = labels

    def __getitem__(self, index):
        text = self.texts[index]
        label = self.labels[index]
        return text, label
    
    def __len__(self):
        return len(self.texts)

method = 'finetune'
model_path = f'model_{method}.pt'

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
alephbert_tokenizer = AutoTokenizer.from_pretrained('onlplab/alephbert-base')
alephbert = torch.load(model_path)

agg_scores_df = pd.read_csv('agg_score_bin.csv')
agg_scores_df.dropna(inplace=True, ignore_index=True)

agg_test = MyDataset(agg_scores_df['text'], agg_scores_df['score'])

test_dataloader = torch.utils.data.DataLoader(agg_test, batch_size=16, shuffle=False)

# Evaluate model
alephbert.eval()

with torch.no_grad():
    for texts, scores in test_dataloader:
        inputs = alephbert_tokenizer(texts, padding=True, truncation=True, return_tensors='pt').to(device)
        scores = scores.to(device)

        outputs = alephbert(**inputs, return_dict=False)[0]
        _, predicted = torch.max(outputs.data, 1)

        is_correct = (predicted == scores)

        zipped = zip(is_correct, texts, scores, predicted)

        for tup in zipped:
          if not tup[0]:
            print(tup)