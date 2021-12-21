
import os
import uuid
import json
from datetime import datetime
from rest_framework_simplejwt.tokens import RefreshToken
from django.middleware import csrf
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import send_mail
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.models import User
from django.conf import settings
from rest_framework import status
from api.models import Farmer

class PasswordReset(APIView):
    #request to reset password before sending email
    def post(self, request, format=None):

        try:
            data = request.data

            email = data["email"]

            try:
                user = User.objects.get(email=email)

                reset_email = ResetEmail()
                
                reset_email.post(request)

            except ObjectDoesNotExist:
                return Response({"message":"User Does Not Exist!"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as exception:

            return Response({"message":f"{exception}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class PasswordConfirm(APIView):
    #request to reset password after getting token
    def post(request):
        try:
            data = request.data

            resetValue = data['resetValue']

            with open("reset.json", "r") as openfile:
                resetInfo = json.load(openfile)
                
            if resetInfo['randomNumber'] == resetValue:
                #
                return Response({"message":"Success", "link":"/api/"}, status=status.HTTP_200_OK)
            else:
                return Response({"message":"Invalid Token"}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as exception:

            return Response({"message":f"{exception}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class NewPassword(APIView):
    #inputing the new password
    def post(request):

        data = request.data 

        resetValue = data['resetValue']

        password = data['newPassword']

        email = data['email']

        try:

            with open("reset.json", "r") as openfile:
                resetInfo = json.load(openfile)
                
            if resetInfo['email'] == email:

                if resetInfo['randomNumber'] == resetValue:
                    
                    try:

                        user = User.objects.get(email=email)

                        user.set_password(password)

                        user.save()

                        if os.path.exists("reset.json"):

                            os.remove("reset.json")

                        else:

                            return Response({"message":f"Reset File Error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

                        return Response({"message":"Password reset sucessfully","link":"/login/"}, status=status.HTTP_200_OK)

                    except ObjectDoesNotExist:

                        return Response({"message":f"User with email address: {email} Not Found"}, status=status.HTTP_404_NOT_FOUND)
                    
                else:

                    return Response({"message":"Invalid Token"}, status=status.HTTP_401_UNAUTHORIZED)
            else:

                return Response({"message":"Invalid Email"}, status=status.HTTP_401_UNAUTHORIZED)
        
        except Exception as exception:

            return Response({"message":f"{exception}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            

            

        


class ConfirmEmail(APIView):
    def post(request):
        return Response({"message":f"Confirmation Email Sent to {email}"}, status=status.HTTP_200_OK)



class ResetEmail(APIView):

    randomNumber = uuid.uuid4()
    #def __init__(self):
    #    self.randomNumber = "randonNumber"

    def post(request):

        data = request.data

        email = data['email']

        resetInfo = {
            "email": f"{email}",
            "randomNumber": f"{ResetEmail.randomNumber}"
        }

        try:
            subject = "AgriPredict Password Reset"

            message = f"Use this code to reset your password: {ResetEmail.randomNumber}"

            email_from = settings.EMAIL_HOST_USER

            recipient_list = [f'{email}']

            resetData = json.dumps(resetInfo, indent=4)

            with open("reset.json", "w") as outfile:
                outfile.write(resetData)

            send_mail(subject, message, email_from, recipient_list)

            return Response({"message":f"Password Reset Email Sent to {email}"}, status=status.HTTP_200_OK)

        except Exception as exception:

            return Response({"message":f"{exception}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)