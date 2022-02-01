import os
import csv
import json
from datetime import datetime
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.sites.shortcuts import get_current_site
from django.middleware import csrf
from django.core.mail import send_mail
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.conf import settings
from rest_framework import status
from django.template.loader import render_to_string
from api.models import Farmer
from .email import ResetEmail


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

        try:
            user = User.objects.get(username=username)

            user = authenticate(username=username, password=password)

            if user is not None:

                if user.is_active:

                    login(request, user)

                    access_data = get_tokens_for_user(user)

                    response.set_cookie(
                        key=settings.SIMPLE_JWT["AUTH_COOKIE"],
                        value=access_data["access"] + "::" + "F0" + str(user.id),
                        expires=settings.SIMPLE_JWT["ACCESS_TOKEN_LIFETIME"],
                        secure=settings.SIMPLE_JWT["AUTH_COOKIE_SECURE"],
                        httponly=settings.SIMPLE_JWT["AUTH_COOKIE_HTTP_ONLY"],
                        samesite=settings.SIMPLE_JWT["AUTH_COOKIE_SAMESITE"],
                    )

                    csrf.get_token(request)

                    response.data = {
                        "message": "Login Successful",
                        # "data": data
                        }
                        
                    response['status'] = status.HTTP_200_OK

                    return response

                else:
                    return Response(
                        {"No active": "This account is not active!!"},
                        status=status.HTTP_403_FORBIDDEN,
                    )
            else:
                return Response(
                    {"Invalid": "Invalid username or password!!"},
                    status=status.HTTP_403_FORBIDDEN,
                )

        except ObjectDoesNotExist:
            return Response(
                {"message": "User doesnot exist"}, status=status.HTTP_404_NOT_FOUND
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
                # newUser.is_active = True

                newUser.save()

                try:
                    # check for farmer-User data
                    newFarmer = User.objects.get(username=data["username"])

                    newFarmer_id = newFarmer.id
                    newFarmer_username = newFarmer.username

                    valid_newFarmer = Farmer()

                    valid_newFarmer.unique_id = "F0" + str(newFarmer_id)
                    valid_newFarmer.user_id = newFarmer_id
                    valid_newFarmer.username = newFarmer_username
                    valid_newFarmer.email = data["email"]
                    valid_newFarmer.first_name = data["first_name"]
                    valid_newFarmer.last_name = data["last_name"]
                    # valid_newFarmer.is_active = True
                    valid_newFarmer.telephone = data["telephone"]
                    valid_newFarmer.region = data["region"]

                    valid_newFarmer.save()

                    mail_subject = "Activate AgriPredict Account"

                    current_site = get_current_site(request)

                    token = ResetEmail.generate_token()

                    eToken = urlsafe_base64_encode(force_bytes(token))

                    refreshID = urlsafe_base64_encode(force_bytes(newUser.email))
                    # message = f"Please confirm your account by clicking here: http://{current_site.domain}"

                    message = render_to_string(
                        "activateEmail.html",
                        {
                            "user": newUser,
                            "domain": current_site.domain,
                            "token": eToken,
                            "refreshID": refreshID,
                        },
                    )

                    from_email = settings.EMAIL_HOST_USER

                    recipient_list = [
                        f"{data['email']}",
                    ]

                    try:

                        send_mail(mail_subject, message, from_email, recipient_list)

                        activation_data = [newUser.email, token]

                        try:
                            with open("activate.csv", "a") as outfile:
                                writer = csv.writer(outfile)
                                writer.writerow(activation_data)

                        except Exception as write_exception:
                            return Response(
                                {"message": f"{write_exception}"},
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            )

                    except Exception as exception:

                        return Response(
                            {"message": f"{exception}"},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        )

                    data = dict(
                        message=f"Please check {data['email']} to confirm your account",
                    )
                    return Response(data, status=status.HTTP_200_OK)
                    # else:
                    #    return Response(
                    #        "Server Error: serializer invalid", status=status.HTTP_500_INTERNAL_SERVER_ERROR
                    #    )

                except Exception as e:
                    return Response(
                        {"message": f"{e}"},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    )

        except Exception as e:
            return Response(
                {"message": f"{e}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class LogoutView(APIView):
    def post(self, request, format=None):

        try:
            logout(request)

            return Response(
                {"message": "Successfully Logged Out"}, 
                status=status.HTTP_200_OK
            )
        except Exception as exception:
            return Response(
                {"Error":f"{exception}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
