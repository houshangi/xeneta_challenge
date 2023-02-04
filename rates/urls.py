from django.urls import path
from .views import AveragePriceList

urlpatterns = [path("rates", AveragePriceList.as_view(), name="hours-convert")]
