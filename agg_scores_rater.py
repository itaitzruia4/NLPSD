from transformers import AutoTokenizer
import torch
from typing import List


class AggScoresRater:
    '''
    Rate the aggressiveness of a protocol using a pre-trained model.
    
    Params
    ------
    model_path: str
        path to the saved model
    
    Attributes
    ----------
    device: torch.device
        device to run the model on.
    tokenizer: transformers.AutoTokenizer
        tokenizer for the model.
    model: transformers.AutoModelForSequenceClassification
        model to use for rating the aggressiveness of a protocol.
    '''
    def __init__(self, model_path: str) -> None:
        # Load saved model from file
        self.device = torch.device('cpu')
        self.tokenizer = AutoTokenizer.from_pretrained('onlplab/alephbert-base')
        self.model = torch.load(model_path)

    def rate_aggressiveness(self,
                            sentences: List[str]) -> float:
        '''
        Rate the aggressiveness of a protocol.

        Params
        ------
        sentences: str
            list of sentences in the protocol.
        
        Returns
        -------
        float
            aggressiveness score - ratio of aggressive sentences in protocol.
        '''
        torch.cuda.empty_cache()
        # Evaluate model
        self.model.to(self.device)
        self.model.eval()

        aggressive = 0
        total = 0

        # Iterate over sentences in the protocol
        with torch.no_grad():
            # Tokenize sentences
            inputs = self.tokenizer(sentences, padding=True, truncation=True, return_tensors='pt').to(self.device)
            # Obtain predictions from model
            outputs = self.model(**inputs, return_dict=False)[0].to(self.device)
            del inputs

            _, predicted = torch.max(outputs.data, 1)
            del _
            del outputs

            # Update sentences count and aggression count
            total += predicted.size(0)
            aggressive += predicted.sum().item()
            del predicted

        return aggressive / total
    