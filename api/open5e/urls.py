from django.urls import path
from .views import SearchView

urlpatterns = [ 
    path("search/<str:type>", SearchView.as_view(), name = "database-search")
]