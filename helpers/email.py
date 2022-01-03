import os
import csv
import uuid
import json
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from datetime import datetime
from rest_framework_simplejwt.tokens import RefreshToken
from django.middleware import csrf
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import send_mail
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.conf import settings
from rest_framework import status
from api.models import Farmer


class ResetEmail(APIView):

    randomNumber = uuid.uuid4()
    # def __init__(self):
    #    self.randomNumber = "randonNumber"

    def generate_token():
        return str(ResetEmail.randomNumber)

    def post(request):

        data = request.data

        email = data["email"]

        resetInfo = [email, ResetEmail.randomNumber]

        try:
            subject = "AgriPredict Password Reset"

            message = f"Use this code to reset your password: {ResetEmail.randomNumber}"

            email_from = settings.EMAIL_HOST_USER

            recipient_list = [f"{email}"]

            # resetData = json.dumps(resetInfo, indent=4)

            with open("reset.csv", "a") as outfile:
                writer = csv.writer(outfile)
                writer.writerow(resetInfo)

            try:
                send_mail(subject, message, email_from, recipient_list)
            except Exception as exception:
                return Response(
                    {"message": f"{exception}"},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )

            return Response(
                {"message": f"Password Reset Email Sent to {email}"},
                status=status.HTTP_200_OK,
            )

        except Exception as exception:

            return Response(
                {"message": f"{exception}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class PasswordReset(APIView):
    # request to reset password before sending email
    def post(self, request, format=None):

        try:
            data = request.data

            email = data["email"]

            try:
                user = User.objects.get(email=email)

                reset_email = ResetEmail()

                reset_email.post(request)

            except ObjectDoesNotExist:

                return Response(
                    {"message": "User Does Not Exist!"},
                    status=status.HTTP_404_NOT_FOUND,
                )

        except Exception as exception:

            return Response(
                {"message": f"{exception}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class PasswordConfirm(APIView):
    # inputing the new password
    def post(request):

        data = request.data

        resetValue = data["resetValue"]

        password = data["newPassword"]

        email = data["email"]

        try:
            rows = []
            with open("reset.csv", "r") as openfile:
                csvreader = csv.reader(openfile)
                for row in csvreader:
                    rows.append(row)

            current_user = rows[-1]

            if current_user[0] == email:

                if current_user[1] == resetValue:

                    try:

                        user = User.objects.get(email=email)

                        user.set_password(password)

                        user.save()

                        """ if os.path.exists("reset.json"):

                            os.remove("reset.json")

                        else:

                            return Response(
                                {"message": f"Reset File Error"},
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            ) """

                        return Response(
                            {"message": "Password reset sucessfully"},
                            status=status.HTTP_200_OK,
                        )

                    except ObjectDoesNotExist:

                        return Response(
                            {"message": f"User with email address: {email} Not Found"},
                            status=status.HTTP_404_NOT_FOUND,
                        )

                else:

                    return Response(
                        {"message": "Invalid Token"},
                        status=status.HTTP_401_UNAUTHORIZED,
                    )
            else:

                return Response(
                    {"message": "Invalid Email"}, status=status.HTTP_401_UNAUTHORIZED
                )

        except Exception as exception:

            return Response(
                {"message": f"{exception}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


@api_view(["GET"])
def ConfirmAccount(request, eToken, refreshID):
    try:
        data = request.data

        token = force_text(urlsafe_base64_decode(eToken))

        user_email = force_text(urlsafe_base64_decode(refreshID))

        try:
            rows = []
            with open("activate.csv", "r") as infile:
                csvreader = csv.reader(infile)
                for row in csvreader:
                    rows.append(row)

            current_user = rows[-1]

            if user_email == current_user[0]:
                if token == current_user[1]:
                    try:
                        inactive_user = User.objects.get(email=user_email)

                        inactive_farmer = Farmer.objects.get(email=user_email)

                        inactive_user.is_active = True

                        inactive_farmer.is_active = True

                        inactive_user.save()

                        inactive_farmer.save()

                        login(request, inactive_user)

                        """ if os.path.exists("activate.json"):

                            os.remove("activate.json")

                        else:

                            return Response(
                                {"message": f"Reset File Error"},
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            ) """

                        return Response(
                            {
                                "message": "Thank you for confirming your account. You can now login."
                            },
                            status=status.HTTP_200_OK,
                        )

                    except ObjectDoesNotExist:
                        return Response(
                            {"message": f"User with email {user_email} does not exist"},
                            status=status.HTTP_404_NOT_FOUND,
                        )
                else:
                    return Response(
                        {"message": "Invalid token for email"},
                        status=status.HTTP_400_BAD_REQUEST,
                    )
            else:
                return Response(
                    {"message": "Invalid Email for token"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        except Exception as file_exception:
            return Response(
                {"message": f"{file_exception}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
    except Exception as func_exception:
        return Response(
            {"message": f"{func_exception}"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
