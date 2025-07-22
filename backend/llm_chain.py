import os
from openai import AzureOpenAI
from dotenv import load_dotenv

load_dotenv()

openai_client = AzureOpenAI(
    api_key=os.getenv("openai_key"),
    api_version=os.getenv("openai_version"),
    azure_endpoint=os.getenv("openai_endpoint")
)

deployment_name = os.getenv("deployment_name")

def ask_llm(text_input):
    prompt = f"""
    Du bist ein KI-System für betriebswirtschaftliche Analysen.
    Analysiere das folgende Dokument (z. B. ein Rechnungs- oder Produktionsbericht) und gib die wichtigsten geschäftsrelevanten Informationen strukturiert zurück.

    TEXT:
    \"\"\"
    {text_input}
    \"\"\"

    Ausgabeformat:
    - Zusammenfassung:
    - Wichtige Kennzahlen (z. B. Stromkosten, Zölle, CO₂-Werte):
    - Empfehlungen für das Management:
    """

    response = openai_client.chat.completions.create(
        model=deployment_name,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
    )

    return response.choices[0].message.content

