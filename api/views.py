import json
from enum import unique
from django.core import paginator
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.parsers import JSONParser
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
from .models import Farmer, Maize, Precipitation, Dataset, Repo
from .serializers import (
    FarmerSerializer,
    MaizeSerializer,
    PrecipitationSerializer,
    DatasetSerializer,
    RepositorySerializer,
)

# Create your views here.

@csrf_exempt
@api_view(["GET"])
def IndexView(request):

    data = {"message": "Welcome to the PrediFarm API"}

    if request.method == "GET":
        return Response(data, status=status.HTTP_200_OK)


@api_view(["GET", "POST"])
def FarmerBasicView(request):
    # Lists All Farmers
    if request.method == "GET":
        data = []

        nextPage = 1

        previousPage = 1

        farmers = Farmer.objects.all()

        page = request.GET.get("page", 1)

        paginator = Paginator(farmers, 10)

        try:

            data = paginator.page(page)

        except PageNotAnInteger:

            data = paginator.page(1)

        except EmptyPage:

            data = paginator.page(paginator.num_pages)

        serializer = FarmerSerializer(data, context={"request": request}, many=True)

        if data.has_next():

            nextPage = data.next_page_number()

        if data.has_previous():

            previousPage = data.previous_page_number()

        return Response(
            {
                "data": serializer.data,
                "count": paginator.count,
                "numpages": paginator.num_pages,
                "nextlink": "/api/farmers/?page=" + str(nextPage),
                "prevlink": "/api/farmers/?page=" + str(previousPage),
            }
        )

    # Creates New Farmer
    elif request.method == "POST":

        serializer = FarmerSerializer(data=request.data)

        if serializer.is_valid():

            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "PUT", "DELETE"])
def FarmerDetailView(request, id):
    # Retrieve Individual Farmer Details
    try:

        farmer = Farmer.objects.get(unique_id=id)

    except Farmer.DoesNotExist:

        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":

        serializer = FarmerSerializer(farmer, context={"request": request})

        return Response(serializer.data)

    elif request.method == "PUT":

        serializer = FarmerSerializer(
            farmer, data=request.data, context={"request": request}
        )

        if serializer.is_valid():

            serializer.save()

            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == "DELETE":

        farmer.delete()

        return Response(message="Farmer Deleted", status=status.HTTP_204_NO_CONTENT)


@api_view(["GET", "POST"])
def PreciBasicView(request):
    # Lists All Precipitation Records
    if request.method == "GET":
        data = []

        nextPage = 1

        previousPage = 1

        preci_values = Precipitation.objects.all()

        page = request.GET.get("page", 1)

        paginator = Paginator(preci_values, 10)

        try:

            data = paginator.page(page)

        except PageNotAnInteger:

            data = paginator.page(1)

        except EmptyPage:

            data = paginator.page(paginator.num_pages)

        serializer = PrecipitationSerializer(
            data, context={"request": request}, many=True
        )

        if data.has_next():

            nextPage = data.next_page_number()

        if data.has_previous():

            previousPage = data.previous_page_number()

        return Response(
            {
                "data": serializer.data,
                "count": paginator.count,
                "numpages": paginator.num_pages,
                "nextlink": "/api/precipitation/?page=" + str(nextPage),
                "prevlink": "/api/precipitation/?page=" + str(previousPage),
            }
        )

    # Adds New Precipitation Record
    elif request.method == "POST":

        serializer = PrecipitationSerializer(data=request.data)

        if serializer.is_valid():

            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "POST", "DELETE"])
def PreciDetailView(request, id):
    # Retrieve Single Precipitation Record
    try:

        preci_record = Precipitation.objects.get(id=id)

    except Precipitation.DoesNotExist:

        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":

        serializer = PrecipitationSerializer(preci_record, context={"request": request})

        return Response(serializer.data)

    elif request.method == "PUT":

        serializer = PrecipitationSerializer(
            preci_record, data=request.data, context={"request": request}
        )

        if serializer.is_valid():

            serializer.save()

            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == "DELETE":

        preci_record.delete()

        return Response(message="Record Deleted", status=status.HTTP_204_NO_CONTENT)


@api_view(["GET", "POST"])
def MaizeBasicView(request):
    # Lists All Maize Records
    if request.method == "GET":
        data = []

        nextPage = 1

        previousPage = 1

        crop_values = Maize.objects.all()

        page = request.GET.get("page", 1)

        paginator = Paginator(crop_values, 10)

        try:

            data = paginator.page(page)

        except PageNotAnInteger:

            data = paginator.page(1)

        except EmptyPage:

            data = paginator.page(paginator.num_pages)

        serializer = MaizeSerializer(data, context={"request": request}, many=True)

        if data.has_next():

            nextPage = data.next_page_number()

        if data.has_previous():

            previousPage = data.previous_page_number()

        return Response(
            {
                "data": serializer.data,
                "count": paginator.count,
                "numpages": paginator.num_pages,
                "nextlink": "/api/crop/?page=" + str(nextPage),
                "prevlink": "/api/crop/?page=" + str(previousPage),
            }
        )

    # Adds New Crop Record
    elif request.method == "POST":

        serializer = MaizeSerializer(data=request.data)

        if serializer.is_valid():

            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "POST", "DELETE"])
def MaizeDetailView(request, type):
    # Retrieve Single Crop Record
    try:

        crop_record = Maize.objects.get(maize_type=type)

    except Maize.DoesNotExist:

        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":

        serializer = MaizeSerializer(crop_record, context={"request": request})

        return Response(serializer.data)

    elif request.method == "PUT":

        serializer = PrecipitationSerializer(
            crop_record, data=request.data, context={"request": request}
        )

        if serializer.is_valid():

            serializer.save()

            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == "DELETE":

        crop_record.delete()

        return Response(message="Record Deleted", status=status.HTTP_204_NO_CONTENT)

@csrf_exempt
@api_view(["GET"])
def PageNotFound(request, exception):

    return Response(
        {"message": "Page Not Found", "meta": f"{request.headers}"},
        status=status.HTTP_404_NOT_FOUND,
    )


@csrf_exempt
@api_view(["GET"])
def dataset(request):
    snippets = Dataset.objects.all()
    serializer = DatasetSerializer(snippets, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def dataByYear(request, year):
    try:
        snippet = Dataset.objects.get(year=year)
        serializer = DatasetSerializer(snippet)
        return Response(serializer.data)
    except Dataset.DoesNotExist:
        return Response(status=404)

        serializer = SnippetSerializer(snippet)
        return JsonResponse(serializer.data)


@csrf_exempt
@api_view(["GET", "POST"])
def RepositoryView(request):
    try:
        if request.method == "POST":

            months = [
                "January",
                "February",
                "March",
                "April",
                "May",
                "June",
                "July",
                "August",
                "September",
                "November",
                "December",
            ]

            regions = ["North", "South", "East", "West"]

            data = request.data
            # print(data)
            try:

                user = User.objects.get(username=data["username"])

                if data["month"] not in months:

                    return Response(
                        {
                            "message": "Invalid Month Format! Use (January, February,...)"
                        },
                        status=status.HTTP_400_BAD_REQUEST,
                    )

                else:
                    if data["region"] not in regions:

                        return Response(
                            {"message": "Invalid Region! Use (North, South,...)"},
                            status=status.HTTP_400_BAD_REQUEST,
                        )

                    else:
                        record = Repo()

                        record.user_name = data["username"]

                        record.month = data["month"]

                        record.region = data["region"]

                        record.production = data["production"]

                        record.price = data["price"]

                        try:
                            record.save()

                            return Response(
                                {"message": "successfully added"},
                                status=status.HTTP_201_CREATED,
                            )

                        except Exception as exception:
                            return Response(
                                {"message": f"{exception}"},
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            )
            except ObjectDoesNotExist:

                return Response(
                    {"message": "User does not exist"}, status=status.HTTP_404_NOT_FOUND
                )

        elif request.method == "GET":

            try:
                repository = Repo.objects.all()

                serialized_data = RepositorySerializer(repository, many=True)

                all_data = json.dumps(serialized_data.data)

                clean_data = json.loads(all_data)

                return Response({"data": clean_data}, status=status.HTTP_200_OK)

            except ObjectDoesNotExist:

                return Response(
                    {"message": "No data available"}, status=status.HTTP_404_NOT_FOUND
                )

        else:
            return Response(
                {"message": "Method NOT Allowed"},
                status=status.HTTP_405_METHOD_NOT_ALLOWED,
            )
    except Exception as exception:
        return Response(
            {"message": f"{exception}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
