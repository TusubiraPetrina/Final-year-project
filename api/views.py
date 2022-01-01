from enum import unique
from django.core import paginator
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Farmer, Maize, Precipitation,Dataset
from .serializers import FarmerSerializer, MaizeSerializer, PrecipitationSerializer,DatasetSerializer

# Create your views here.


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

@api_view(['GET'])
def PageNotFound(request, exception):

    return Response(
            {
                "message": "Page Not Found",
                "meta": f"{request.headers}"
            },
            status=status.HTTP_404_NOT_FOUND
        )

@api_view(['GET'])
def dataset(request):
    queryset = Dataset.objects.all()
    serializer_class = DatasetSerializer