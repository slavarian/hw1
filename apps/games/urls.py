from django.urls import path

# Local
from .views import index, about, get_game , games


urlpatterns = [
    path('', index),
    path('about/', about),
    path('game/<int:game_id>/', get_game),
    path('game/', games)
]
