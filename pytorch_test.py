from transformers import AutoTokenizer, AutoModelForCausalLM, AutoConfig

# Charger le tokenizer
tokenizer = AutoTokenizer.from_pretrained("neuralmagic/Mistral-7B-Instruct-v0.3-GPTQ-4bit")

# Charger la configuration du modèle
config = AutoConfig.from_pretrained("neuralmagic/Mistral-7B-Instruct-v0.3-GPTQ-4bit")

# Ajouter une configuration de quantification pour désactiver Exllama
quantization_config = {
    "quant_method": "gptq",  # méthode de quantification utilisée
    "use_exllama": False,
    "bits": 4  # spécifiez le nombre de bits utilisés pour la quantification
}

# Mettre à jour la configuration avec la configuration de quantification
config.quantization_config = quantization_config

# Charger le modèle avec la configuration mise à jour
model = AutoModelForCausalLM.from_pretrained("neuralmagic/Mistral-7B-Instruct-v0.3-GPTQ-4bit", config=config)

# Définir le pad_token_id si nécessaire
if model.config.pad_token_id is None:
    model.config.pad_token_id = model.config.eos_token_id

# Fonction pour générer du texte
def generate_text(prompt, max_length=50):
    inputs = tokenizer(prompt, return_tensors="pt")  # Utilise PyTorch
    attention_mask = inputs.attention_mask
    outputs = model.generate(inputs.input_ids, attention_mask=attention_mask, max_length=max_length, num_return_sequences=1)
    generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return generated_text

# Exemple d'utilisation
prompt = "Dans un futur lointain, l'humanité a"
generated_text = generate_text(prompt)
print(generated_text)
