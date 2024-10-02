import openai

openai.api_key = "lm-studio"
openai.api_base = "http://localhost:1234/v1"

completion = openai.ChatCompletion.create(
    model="model-identifier",
    messages=[
        {"role": "system", "content": "tu es un chatbot SAV qui parle francais."},
        {"role": "user", "content": "Introduce yourself."}
    ],
    temperature=0.7,
)

print(completion.choices[0].message['content'])
