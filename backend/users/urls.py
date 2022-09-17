from django.urls import path
from .views import Register, Login, Logout, GetAppointments, GetAppointmentsNumber, MatchUser

urlpatterns = [
    path('register/', Register.as_view(), name="register"),
    path('login/', Login.as_view(), name="login"),
    path('logout/', Logout.as_view(), name="logout"),
    path('get_appointments/', GetAppointments.as_view(), name="get_appointments"),
    path('get_appointments_number/',
         GetAppointmentsNumber.as_view(), name="get_appointments_number"),
    path('match_user/', MatchUser.as_view(), name="match_user"),
]
