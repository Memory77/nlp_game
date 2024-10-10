import fitz  # PyMuPDF pour lire le PDF
import json

# Fonction pour extraire le texte d'un PDF
def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text

# Simuler l'organisation des données en JSON
def convert_text_to_json(text):
    # Ici, tu devrais traiter le texte extrait pour l'organiser
    # Ex. : Séparer les produits, les descriptions, etc.
    catalogue_json = {
        "catalogue": {
            "portes": [
                {"nom": "Porte en bois massif", "prix": "500€", "description": "Porte de haute qualité, en bois massif."},
                {"nom": "Porte en métal", "prix": "700€", "description": "Porte résistante, idéale pour les entrées principales."}
            ],
            "fenetres": [
                {"nom": "Fenêtre à double vitrage", "prix": "300€", "description": "Fenêtre à haute isolation thermique."},
                {"nom": "Fenêtre en PVC", "prix": "200€", "description": "Fenêtre économique, facile d'entretien."}
            ],
            "accessoires": [
                {"nom": "Poignée de porte moderne", "prix": "50€", "description": "Poignée au design élégant."},
                {"nom": "Serrure haute sécurité", "prix": "120€", "description": "Serrure renforcée pour une sécurité maximale."}
            ]
        }
    }
    return catalogue_json

# Chemin vers ton fichier PDF
pdf_path = "2024-04_CATALOGUE-GENERAL_WEB.pdf"

# Extraction du texte et conversion en JSON
pdf_text = extract_text_from_pdf(pdf_path)
catalogue_json = convert_text_to_json(pdf_text)

# Sauvegarde du JSON dans un fichier
with open("catalogue.json", "w", encoding="utf-8") as json_file:
    json.dump(catalogue_json, json_file, ensure_ascii=False, indent=4)

print("Le PDF a été converti en JSON avec succès.")
