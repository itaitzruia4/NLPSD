from transformers import AutoTokenizer
import torch
import re

class AggScoresRater:
    def __init__(self, model_path):
        # Load saved model from file
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.tokenizer = AutoTokenizer.from_pretrained('onlplab/alephbert-base')
        self.model = torch.load(model_path)

    def filter_protocol_sentences(self, text: str) -> str:
        ind = re.search("<< יור >>", text)

        if ind is None:
            ind = re.search("יו\"ר.*:", text)

        txt2 = text[ind.span()[0]:]
        txt2 = re.sub("<<.*","", txt2)
        txt2 = re.sub(">>.*","", txt2)
        txt2 = re.sub(".*:","", txt2)
        txt2 = re.sub("-", " ", txt2)
        txt2 = re.sub("\n\s+","\n", txt2)
        txt2 = re.sub(" +"," ", txt2)
        txt2 = re.sub("\t","", txt2)
        return txt2

    def rate_aggressiveness(self, protocol: str) -> float:
        # Evaluate model
        self.model.eval()

        sentences = self.filter_protocol_sentences(protocol).split('\n')

        aggressive = 0
        total = 0

        with torch.no_grad():
            inputs = self.tokenizer(sentences, padding=True, truncation=True, return_tensors='pt').to(self.device)
            outputs = self.model(**inputs, return_dict=False)[0].to(self.device)

            _, predicted = torch.max(outputs.data, 1)
            print
            total += predicted.size(0)
            aggressive += predicted.sum().item()

        return aggressive / total