import os
from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential
from azure.core.exceptions import HttpResponseError
from azure.ai.contentsafety.models import AnalyzeTextOptions, TextCategory
from flask import flash


def analyze_text(text, threshold=4):
    try:
        key = os.environ["CONTENT_SAFETY_KEY"]
        endpoint = os.environ["CONTENT_SAFETY_ENDPOINT"]
    except KeyError:
        flash("Content safety service is not configured.", "error")
        return False

    client = ContentSafetyClient(endpoint, AzureKeyCredential(key))
    request = AnalyzeTextOptions(text=text)

    try:
        response = client.analyze_text(request)
    except HttpResponseError as e:
        print("Analyze text failed.")
        return False

    for item in response.categories_analysis:
        if item.severity is not None and item.severity >= threshold:
            return False
    return True
