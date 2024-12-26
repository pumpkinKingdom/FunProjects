### api.py (Clothing Detection API Integration)
from inference_sdk import InferenceHTTPClient

CLIENT = InferenceHTTPClient(
    api_url="https://detect.roboflow.com",
    api_key="5VnT4JBda5nPYHYW1biC"
)

def detect_clothes(image_path):
    result = CLIENT.infer(image_path, model_id="clothes-2-xzuaa/10")
    predictions = result.get('predictions', [])

    if not predictions:
        return 'No clothes detected'

    detected_classes = [pred['class'] for pred in predictions]
    return ', '.join(detected_classes)
