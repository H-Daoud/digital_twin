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

import os
from openai import AzureOpenAI
from dotenv import load_dotenv

load_dotenv()

openai_client = AzureOpenAI(
    api_key=os.getenv("OPENAI_KEY"),
    api_version=os.getenv("OPENAI_VERSION"),
    azure_endpoint=os.getenv("OPENAI_ENDPOINT")
)
deployment_name = os.getenv("DEPLOYMENT_NAME")

def ask_llm(text_input):
    """
    Summarizes business documents and extracts KPIs using LLM.
    """
    prompt = f"""
    You are an AI assistant for business analysis.
    Analyze the following document (e.g. invoice or production report) and extract:
    - A summary
    - Key metrics (energy cost, tariffs, CO₂, etc.)
    - Management recommendations
    TEXT:
    \"\"\"{text_input}\"\"\"
    Format:
    - Summary:
    - Key Metrics:
    - Recommendations:
    """
    response = openai_client.chat.completions.create(
        model=deployment_name,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
    )
    return response.choices[0].message.content

def extract_structured_logic(text_input):
    """
    Extracts simulation-ready business logic from natural language rules.
    Example: "If energy price rises above 200€/MWh, delay production by one week."
    """
    prompt = f'''
    You are an AI assistant for process simulation.
    Analyze the following business rule and extract it as structured JSON:
    Example input: "Wenn die Energiekosten über 200 €/MWh steigen, schieben wir die Produktion um eine Woche nach hinten."
    Output format:
    {{
      "block": "ProductionSchedule",
      "trigger_attribute": "Energy.price",
      "condition": "Energy.price > 200",
      "effect": "ProductionSchedule.delay += 7"
    }}
    Text: \"\"\"{text_input}\"\"\"
    '''
    response = openai_client.chat.completions.create(
        model=deployment_name,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
    )
    return response.choices[0].message.content
