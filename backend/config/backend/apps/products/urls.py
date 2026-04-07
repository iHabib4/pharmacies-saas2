from django.urls import path

from .views import symptom_recommendation

urlpatterns = [
    path("ai-recommend/", symptom_recommendation),
]
