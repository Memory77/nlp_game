import json
from sentence_transformers import SentenceTransformer
import fitz  # PyMuPDF pour extraire le texte des PDF

# Fonction pour extraire le texte du PDF
def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)  # Ouvrir le PDF
    text = ""
    for page in doc:
        text += page.get_text()  # Extraire le texte de chaque page
    return text

# Générer l'embedding à partir du texte extrait
def generate_embedding_from_pdf(pdf_path, model):
    text = extract_text_from_pdf(pdf_path)  # Extraire le texte du PDF
    embedding = model.encode(text).tolist()  # Générer l'embedding et convertir en liste
    return embedding

# Charger le modèle SentenceTransformer
model = SentenceTransformer('all-MiniLM-L6-v2')

# Chemin vers ton fichier PDF
pdf_path = "2024-04_CATALOGUE-GENERAL_WEB.pdf"

# Générer l'embedding
embedding = generate_embedding_from_pdf(pdf_path, model)

# Sauvegarder l'embedding dans un fichier JSON
with open("embedding_catalogue.json", "w") as f:
    json.dump({"embedding": embedding}, f)

print("Embedding généré et sauvegardé dans 'embedding_catalogue.json'")
