from transformers import AutoTokenizer
import torch
from typing import List


class AggScoresRater:
    def __init__(self, model_path):
        # Load saved model from file
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.tokenizer = AutoTokenizer.from_pretrained('onlplab/alephbert-base')
        self.model = torch.load(model_path)

    def rate_aggressiveness(self,
                            sentences: List[str],
                            verboose=False) -> float:
        # Evaluate model
        self.model.eval()

        aggressive = 0
        total = 0

        with torch.no_grad():
            inputs = self.tokenizer(sentences, padding=True, truncation=True, return_tensors='pt').to(self.device)
            outputs = self.model(**inputs, return_dict=False)[0].to(self.device)
            del inputs

            _, predicted = torch.max(outputs.data, 1)
            del outputs

            total += predicted.size(0)
            aggressive += predicted.sum().item()
            del predicted

        return aggressive / total
    