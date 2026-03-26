# from rest_framework import response
from rest_framework.views import APIView
from django.contrib.auth import authenticate 
from rest_framework.response import Response 
from rest_framework import status 
from rest_framework.authtoken.models import Token


from rest_framework import generics
from users.serializer import SignUpSerializer, LogInSerializer
from django.contrib.auth import get_user_model

User = get_user_model()


class SignUpView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = SignUpSerializer


class LogInView(generics.GenericAPIView):
    serializer_class = LogInSerializer
    
    def post(self, request):
        serializer = LogInSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)


        email = serializer.validated_data["email"]
        password = serializer.validated_data["password"]

        user = authenticate(request, username=email, password=password)

        if user is not None:
            token, _ = Token.objects.get_or_create(user=user)
            return Response({
                "message": "Login successful.",
                "token": token.key
                }, status = status.HTTP_200_OK)
        else:
            return Response({"message": "Invalid email or password."}, status=status.HTTP_401_UNAUTHORIZED)