from django.urls import path
from .views import Create, Join, GetFiltered

urlpatterns = [
    path('create/', Create.as_view(), name="create"),
    path('join/', Join.as_view(), name='join'),
    path('', GetFiltered.as_view(), name='get_filtered'),
]
