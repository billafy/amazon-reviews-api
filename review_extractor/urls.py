from django.urls import path
from .views import extractReview

urlpatterns = [
    path('', extractReview),
]
