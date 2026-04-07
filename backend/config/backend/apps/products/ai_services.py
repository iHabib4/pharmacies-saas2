from .models import Symptom


def detect_symptoms(user_text):

    detected = []

    symptoms = Symptom.objects.all()

    text = user_text.lower()

    for symptom in symptoms:

        if symptom.name.lower() in text:

            detected.append(symptom)

    return detected


def recommend_medicines(symptoms):
    medicines = Product.objects.filter(symptoms__in=symptoms, is_otc=True).distinct()
    return medicines
