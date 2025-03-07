from django.urls import path
from . import views

app_name = "hangman"

urlpatterns = [
    path("", views.index, name="index"),  # Menu page
    # path("getCharacter/",views.getCharacter, name="getCharacter"),
]
