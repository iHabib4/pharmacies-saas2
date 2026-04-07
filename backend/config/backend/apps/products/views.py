from rest_framework.decorators import api_view
from rest_framework.response import Response

from .ai_services import detect_symptoms
from .models import Product
from .services import search_medicines


@api_view(["POST"])
def symptom_recommendation(request):

    text = request.data.get("symptom")
    lat = float(request.data.get("lat"))
    lon = float(request.data.get("lon"))

    symptoms = detect_symptoms(text)

    medicines = Product.objects.filter(symptoms__in=symptoms, is_otc=True).distinct()

    data = []

    for m in medicines:
        pharmacy = m.pharmacy
        data.append(
            {
                "medicine": m.name,
                "pharmacy": pharmacy.name,
                "price": getattr(m, "price", None),
            }
        )

    return Response(data)
