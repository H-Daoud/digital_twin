import os
import aiohttp
from dotenv import load_dotenv

load_dotenv()

FORM_ENDPOINT = os.getenv("form_endpoint")
FORM_KEY = os.getenv("form_key")

async def extract_text_from_file(file):
    url = f"{FORM_ENDPOINT}/formrecognizer/documentModels/prebuilt-read:analyze?api-version=2023-07-31"

    headers = {
        "Content-Type": "application/octet-stream",
        "Ocp-Apim-Subscription-Key": FORM_KEY
    }

    content = await file.read()

    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, data=content) as response:
            if response.status != 202:
                raise Exception(f"OCR-Fehler: {response.status} – {await response.text()}")

            operation_location = response.headers.get("Operation-Location")

        # Ergebnis-URL abfragen
        for _ in range(10):
            async with session.get(operation_location, headers={"Ocp-Apim-Subscription-Key": FORM_KEY}) as result_response:
                result = await result_response.json()
                if result.get("status") == "succeeded":
                    lines = result["analyzeResult"]["content"]
                    return lines
                elif result.get("status") == "failed":
                    raise Exception("OCR-Analyse fehlgeschlagen.")

    raise Exception("OCR-Zeitüberschreitung – keine Antwort nach mehreren Versuchen.")

