#from ai import get_ai_response
import ai
def predict_disease(symptoms):
    prompt = f"A patient has the following symptoms: {symptoms}. What is the most likely diagnosis?"
    return get_ai_response(prompt)

def generate_treatment_plan(disease):
    prompt = f"Suggest a treatment plan for the disease: {disease}."
    return get_ai_response(prompt)
