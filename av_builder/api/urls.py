from django.urls import path

from api.views import (
    AircraftDestroyAPI,
    AircraftListCreateAPI,
    AircraftPartDestroyAPI,
    AircraftPartListCreateAPI,
    UserRetrieveAPI,
    auth_view,
    custom_login,
    custom_logout,
    index,
)

urlpatterns = [
    path("", index, name="base"),
    path("login", custom_login, {"next_page": "base"}, name="login"),
    path("logout", custom_logout, name="realout"),
    path("auth", auth_view, name="auth"),
    path("api/user/<int:pk>", UserRetrieveAPI.as_view(), name="retrieve-user"),
    path("api/aircraft-parts", AircraftPartListCreateAPI.as_view(), name="list-create-aircraft-parts"),
    path("api/aircraft-parts/<int:pk>", AircraftPartDestroyAPI.as_view(), name="destroy-aircraft-parts"),
    path("api/aircrafts", AircraftListCreateAPI.as_view(), name="list-create-aircrafts"),
    path("api/aircrafts/<int:pk>", AircraftDestroyAPI.as_view(), name="destroy-aircrafts")

]