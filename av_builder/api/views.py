from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_protect
from rest_framework.authentication import BasicAuthentication, SessionAuthentication
from rest_framework.exceptions import ValidationError
from rest_framework.generics import DestroyAPIView, ListCreateAPIView, RetrieveAPIView

from aircrafts.models import Aircraft, AircraftPart
from api.serializers import AircraftPartSerializer, AircraftSerializer, UserSerializer


@login_required
def index(request, *args, **kwargs):
    return render(request, 'api/index.html')

@csrf_protect
def custom_login(request, *args, **kwargs):
    messages.success(request, "You are successfully logged in")
    return render(request, 'api/login.html')


def custom_logout(request):
    logout(request)
    messages.success(
        request, "You have logged out successfully.")
    return HttpResponseRedirect(reverse("base"))


def auth_view(request):
    username = request.POST.get('username' , '')
    password = request.POST.get('password' , '')
    user = authenticate(username=username, password=password)

    if user is not None:
       login(request, user)
       return HttpResponseRedirect(reverse("base"))
    else:
       return HttpResponseRedirect(reverse("login"))


class UserRetrieveAPI(RetrieveAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    authentication_classes = [BasicAuthentication, SessionAuthentication]


class AircraftPartListCreateAPI(ListCreateAPIView):
    authentication_classes = [BasicAuthentication, SessionAuthentication]
    serializer_class = AircraftPartSerializer
    
    def get_queryset(self):
        part_name_value = self.request.user.groups.first().name
        return AircraftPart.objects.filter(name=part_name_value)


class AircraftPartDestroyAPI(DestroyAPIView):
    authentication_classes = [BasicAuthentication, SessionAuthentication]
    queryset = AircraftPart.objects.all()
    serializer_class = AircraftPartSerializer
    
    def perform_destroy(self, instance):
        if instance.aircraft:
            raise ValidationError(f"Can not delete {instance.name}. It is used.")
        return super().perform_destroy(instance)


class AircraftListCreateAPI(ListCreateAPIView):
    authentication_classes = [BasicAuthentication, SessionAuthentication]
    serializer_class = AircraftSerializer
    queryset = Aircraft.objects.all()


class AircraftDestroyAPI(DestroyAPIView):
    authentication_classes = [BasicAuthentication, SessionAuthentication]
    queryset = Aircraft.objects.all()
    serializer_class = AircraftSerializer
