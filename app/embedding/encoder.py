import torch
from transformers import AutoModel, AutoTokenizer


MODEL_NAME = "Salesforce/codet5p-110m-embedding"


class CodeEmbedder:

    def __init__(self):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"

        self.tokenizer = AutoTokenizer.from_pretrained(
            MODEL_NAME,
            trust_remote_code=True,
        )

        self.model = AutoModel.from_pretrained(
            MODEL_NAME,
            trust_remote_code=True,
        ).to(self.device)

        self.model.eval()

    def encode(self, texts):
        vectors = []

        with torch.no_grad():
            for text in texts:
                inputs = self.tokenizer(
                    text,
                    return_tensors="pt",
                    truncation=True,
                    max_length=512,
                ).to(self.device)

                embedding = self.model(**inputs)[0]

                embedding = embedding / embedding.norm()

                vectors.append(
                    embedding.cpu().tolist()
                )

        return vectors

    def dimension(self):
        return 256