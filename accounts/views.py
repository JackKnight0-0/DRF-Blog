from django.shortcuts import get_object_or_404
from django.contrib.auth import logout
from django.http import JsonResponse

from rest_framework import generics, views
from rest_framework.authtoken.models import Token

from .serializers import RegisterUserSerializer


class RegisterUserView(generics.CreateAPIView):
    serializer_class = RegisterUserSerializer


class LogoutAPIView(views.APIView):
    def post(self, request):
        token = get_object_or_404(Token, user=self.request.user)
        token.delete()

        logout(request=request)

        return JsonResponse({'status': '200'})
