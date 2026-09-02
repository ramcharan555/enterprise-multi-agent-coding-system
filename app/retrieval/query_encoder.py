import torch
from transformers import AutoTokenizer, AutoModel


MODEL_NAME = "Salesforce/codet5p-110m-embedding"


class QueryEncoder:

    def __init__(self):
        self.device = torch.device("cpu")

        self.tokenizer = AutoTokenizer.from_pretrained(
            MODEL_NAME,
            trust_remote_code=True
        )

        self.model = AutoModel.from_pretrained(
            MODEL_NAME,
            trust_remote_code=True
        ).to(self.device)

        self.model.eval()

    def encode(self, text):
        inputs = self.tokenizer.encode(
            text,
            return_tensors="pt"
        ).to(self.device)

        with torch.no_grad():
            embedding = self.model(inputs)[0]

        return embedding.cpu().numpy()