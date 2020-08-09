from django.urls import path
from .views import Register, UserDeatils
urlpatterns = [
    path('register/', Register.as_view()),
    path('<user_id>/get/', UserDeatils.as_view())
]
