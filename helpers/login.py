from datetime import datetime
from rest_framework_simplejwt.tokens import RefreshToken
from django.middleware import csrf
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.models import User
from django.conf import settings
from rest_framework import status
from api.models import Farmer


def get_tokens_for_user(user):

    refresh = RefreshToken.for_user(user)

    return {
        "refresh": str(refresh),
        "access": str(refresh.access_token),
    }


class LoginView(APIView):
    def post(self, request, format=None):

        data = request.data
        response = Response()

        username = data.get("username", None)
        password = data.get("password", None)

        user = authenticate(username=username, password=password)

        if user is not None:

            if user.is_active:

                login(request, user)

                data = get_tokens_for_user(user)

                response.set_cookie(
                    key=settings.SIMPLE_JWT["AUTH_COOKIE"],
                    value=data["access"],
                    expires=settings.SIMPLE_JWT["ACCESS_TOKEN_LIFETIME"],
                    secure=settings.SIMPLE_JWT["AUTH_COOKIE_SECURE"],
                    httponly=settings.SIMPLE_JWT["AUTH_COOKIE_HTTP_ONLY"],
                    samesite=settings.SIMPLE_JWT["AUTH_COOKIE_SAMESITE"],
                )
                
                csrf.get_token(request)
                response.data = {"Success": "Login successfully", "data": data}

                return response

            else:
                return Response(
                    {"No active": "This account is not active!!"},
                    status=status.HTTP_404_NOT_FOUND,
                )
        else:
            return Response(
                {"Invalid": "Invalid username or password!!"},
                status=status.HTTP_404_NOT_FOUND,
            )


class RegisterView(APIView):
    def post(self, request, format=None):
        try:
            data = request.data

            # serializer = FarmerSerializer(data=request.data)

            # print(data)
            try:
                # check if user exists
                user_check = User.objects.get(email=data["email"])

                if user_check:
                    return Response(
                        {"message": "User already exists"},
                        status=status.HTTP_208_ALREADY_REPORTED,
                    )

            except ObjectDoesNotExist:
                # create_user
                newUser = User.objects.create_user(
                    data["username"], data["email"], data["password"]
                )
                newUser.first_name = data["first_name"]
                newUser.last_name = data["last_name"]
                newUser.is_active = True

                newUser.save()

                try:
                    # check for farmer-User data
                    newFarmer = User.objects.get(username=data["username"])
                    newFarmerV = User.objects.get(username=data["username"])

                    """ try:
                        crop = Maize.objects.get(maize_type=data["maize"])
                    except Exception as error:
                        return Response({'message':f'{error}'}, status=status.HTTP_400_BAD_REQUEST) """

                    newFarmer_id = newFarmer.id
                    newFarmer_username = newFarmer.username

                    """ newFarmerData = dict(
                        user=newFarmerV,
                        username=newFarmer_username,
                        email=data["email"],
                        first_name=data["first_name"],
                        last_name=data["last_name"],
                        is_active=True,
                        telephone=data["telephone"],
                        region=data["region"],
                    ) """

                    # print(newFarmerData)

                    """ newfarmer_serializer = FarmerSerializer(
                        data=newFarmerData, context={"request": request}
                    ) """

                    # if newfarmer_serializer.is_valid():
                    valid_newFarmer = Farmer()

                    valid_newFarmer.unique_id = "F0" + str(newFarmer_id)
                    valid_newFarmer.user_id = newFarmer_id
                    valid_newFarmer.username = newFarmer_username
                    valid_newFarmer.email = data["email"]
                    valid_newFarmer.first_name = data["first_name"]
                    valid_newFarmer.last_name = data["last_name"]
                    valid_newFarmer.is_active = True
                    valid_newFarmer.telephone = data["telephone"]
                    valid_newFarmer.region = data["region"]

                    valid_newFarmer.save()

                    data = dict(
                        message="Farmer Created Successfully",
                        farmerID=f"ID: {str(valid_newFarmer.unique_id)}",
                    )
                    return Response(data, status=status.HTTP_201_CREATED)
                    # else:
                    #    return Response(
                    #        "Server Error: serializer invalid", status=status.HTTP_500_INTERNAL_SERVER_ERROR
                    #    )

                except Exception as e:
                    return Response(
                        f"Server Error: {e}",
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    )

        except Exception as e:
            return Response(f"Error: {e}")


class LogoutView(APIView):
    def post(self, request, format=None):

        logout(request)

        return Response({"message":"Successfully Logged Out"}, status=status.HTTP_200_OK)