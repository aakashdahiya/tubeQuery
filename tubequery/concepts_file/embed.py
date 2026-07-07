# not in use - just to see how we embed text and compare them

from sentence_transformers import SentenceTransformer
import numpy as np

model=SentenceTransformer("all-MiniLM-L6-V2")

text1 = "the algorithm decides which videos get recommended"
text2 = "how does YouTube pick what to suggest"
text3 = "recipe for chocolate cake"

emb1 = model.encode(text1)
emb2 = model.encode(text2)
emb3 = model.encode(text3)

# Cosine similarity formula
def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

print(f"text1 vs text2 (similar meaning): {cosine_similarity(emb1, emb2):.4f}")
print(f"text1 vs text3 (unrelated):       {cosine_similarity(emb1, emb3):.4f}")
print(f"text2 vs text3 (unrelated):       {cosine_similarity(emb2, emb3):.4f}")