from rest_framework.response import Response
from rest_framework import status
from users.models import User
from users.serializers import RegistrationSerializer,LoginUserSerializer
from rest_framework.authtoken.models import Token
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import  IsAuthenticated, AllowAny

class SignInUserView(APIView):
    def post(self, request):
        self.serializer_class = RegistrationSerializer
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            first_name = serializer.validated_data['first_name']
            last_name = serializer.validated_data['last_name']
            email = serializer.validated_data['email']
            phone_number = serializer.validated_data['phone_number']
            password = serializer.validated_data['password']

            password = request.data.get('password')

            user = User.objects.create(
                first_name=first_name,
                last_name=last_name,
                email=email,
                phone_number=phone_number,
            )

            user.set_password(password)
            user.save()

            token, created = Token.objects.get_or_create(user=user)

            response_content = {
                'status': True,
                'message': 'User registered successfully.',
                'token': token.key,
            }

            return Response(response_content, status=status.HTTP_201_CREATED)

        else:
            response_content = {
                'status': False,
                'message': serializer.errors,
            }

            print(response_content)
            return Response(response_content, status=status.HTTP_400_BAD_REQUEST)


class LoginUserView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = LoginUserSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        try:
            if serializer.is_valid():
                email = serializer.validated_data['email']

                user = User.objects.get(email=email)

                token, created = Token.objects.get_or_create(user=user)


                response_content = {
                    'status': True,
                    'message': 'User logged in successfully.',
                    'token': token.key,
                }

                return Response(response_content, status=status.HTTP_200_OK)

            else:
                response_content = {
                    'status': False,
                    'message': serializer.errors,
                }

                return Response(response_content, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(e)


class LogoutUserView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        user = request.user

        token = Token.objects.get(user=user)

        token.delete()

        response_content = {
            'status': True,
            'message': 'User logged out successfully.'
        }

        return Response(response_content, status=status.HTTP_202_ACCEPTED)