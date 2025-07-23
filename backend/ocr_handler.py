import os
from azure.ai.formrecognizer import DocumentAnalysisClient
from azure.core.credentials import AzureKeyCredential

AZURE_FORM_ENDPOINT = os.getenv("FORM_ENDPOINT")
AZURE_FORM_KEY = os.getenv("FORM_KEY")

def extract_text_from_file(file):
    client = DocumentAnalysisClient(
        endpoint=AZURE_FORM_ENDPOINT,
        credential=AzureKeyCredential(AZURE_FORM_KEY)
    )
    content = await file.read()
    poller = client.begin_analyze_document("prebuilt-document", content)
    result = poller.result()
    text = "\n".join([line.content for page in result.pages for line in page.lines])
    return text
