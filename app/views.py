from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.middleware.csrf import get_token
from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import csrf_protect

from rest_framework import serializers
from rest_framework import status
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.decorators import api_view, parser_classes

from . import serializers_model 
from . import models

@api_view(["GET"])
def get_user(request, *args, **kwargs):
    if request.query_params:
        user_model = models.User.objects.filter(**request.query_params.dict())
        print(request.query_params.dict())
    else:
        print(request.query_params.dict())
        user_model = models.User.objects.all()

    if user_model:
        response_data = serializers_model.UserSerializer(user_model, many=True)
        return Response(response_data.data, status=status.HTTP_200_OK)
    else:
        response_data = serializers_model.UserSerializer(user_model, many=True)
        return Response(response_data.error_messages ,status=status.HTTP_404_NOT_FOUND)
    
@parser_classes([JSONParser])
@api_view(["GET", "POST"])
def get_item(request, *args, **kwargs):
    if request.method == "GET":
        if request.query_params:
            item_model = models.Item.objects.filter(**request.query_params.dict())
            if item_model.count() == 0:
                return Response({"data": "null", "status code": status.HTTP_404_NOT_FOUND})
            
        else:
            item_model = models.Item.objects.all()
        response_data = serializers_model.ItemSerializer(item_model, many=True)
        print(response_data)
        if item_model:
            return Response(response_data.data, status=status.HTTP_200_OK)
        else:
            return Response(response_data.errors, status=status.HTTP_404_NOT_FOUND)
        
    # POST

    if request.method == "POST":
        item_request = request.data
        # item = serlializers_model.ItemSerializer(data = item_request)
        name = item_request.get("name")
        category = item_request.get("category")
        amount = item_request.get("amount")
        subcategory = item_request.get("subcategory")
        user_id = item_request.get("user_id")

        if models.Item.objects.filter(**request.data).exists():
            print("==================TRIGGER EXEPTION")
            raise serializers.ValidationError('This data already exists')

        try:
            print("==================NOT DUPLICATE IN DB")
            item = models.Item.objects.create(name = name, category = category, amount = amount, subcategory = subcategory, user_id = user_id)
            print("==================CREATE SUCCESSFULLY")
            item.save()
            print("==================SAVED SUCCESSFULLY")
            return Response({"status":status.HTTP_201_CREATED,
                             "data":request.data})
        except ValueError:
            print(ValueError)
            return Response({"error":ValueError,"status code":status.HTTP_400_BAD_REQUEST})


@api_view(['POST','DELETE'])
def update_and_delete_items(request,pk):
    if request.method == "POST":
        item_instance = models.Item.objects.filter(uuid = pk).first()
        serializer_data = serializers_model.ItemSerializer(instance=item_instance, data=request.data)

        if serializer_data.is_valid():
            item = serializer_data.save()
            return Response(serializers_model.ItemSerializer(instance=item).data)
        else:
            return Response(serializer_data.errors, status=status.HTTP_400_BAD_REQUEST)
        
    # delete region
    if request.method == "DELETE":
        item_model = get_object_or_404(models.Item, uuid=pk)
        
        result_state = item_model.delete()
        return Response(data = "delete", status= status.HTTP_200_OK)

@api_view(['GET'])
def view_items(request):
     
    # checking for the parameters from the URL
    if request.query_params:
        items = models.Item.objects.filter(**request.query_params.dict())
        print("queryyyyyyyyyyyyyyyyy", request.query_params.dict())
    else:
        items = models.Item.objects.all()
        print("alllllllllllllllllllllllll", items)
    # if there is something in items else raise error
    if items:
        serializer_data = serializers_model.ItemSerializer(items, many=True)
        print(serializer_data)
        return Response(serializer_data.data, status=status.HTTP_200_OK)
    else:
        return Response(serializer_data.errors,status=status.HTTP_404_NOT_FOUND)
    

@api_view(['GET'])
def view_users(request):
     
    # checking for the parameters from the URL
    if request.query_params:
        items = models.User.objects.filter(**request.query_params.dict())
        print("queryyyyyyyyyyyyyyyyy", items)
    else:
        items = models.User.objects.all()
        print("alllllllllllllllllllllllll", items)
    # if there is something in items else raise error
    if items:
        serializer_data = serializers_model.UserSerializer(items, many=True)
        # print(serializer_data)
        return Response(serializer_data.data, status=status.HTTP_200_OK)
    else:
        return Response(serializer_data.errors,status=status.HTTP_404_NOT_FOUND)
    

################################## AUTHEN REGION ##################################

# @csrf_protect
class CheckMyAuth(APIView):
    def get(self, request):
        print(request.user.is_authenticated)
        if request.user.is_authenticated:
            username = request.user.username
            print(username)
            return Response({"status":status.HTTP_200_OK, "username": username})
        else:
            return Response({"status":status.HTTP_403_FORBIDDEN})

class AuthenLogin(APIView):
    @swagger_auto_schema(request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=['username','password'],
        properties={
            'username': openapi.Schema(type=openapi.TYPE_STRING, description='Username of human'),
            'password': openapi.Schema(type=openapi.TYPE_STRING, description='Password!!!'),
        }
    ))
        
    # login
    def post(self, request):
        
        username = request.data["username"]
        password = request.data["password"]
        user = authenticate(username=username, password=password)

        if user is not None:
            csrf_token = get_token(request)
            login(request, user)
            return Response({"status":status.HTTP_200_OK,"csrf_token": csrf_token})
        else:
            return Response({"status":status.HTTP_403_FORBIDDEN, "error message":"username or password are wrong"})

class AuthenSignupClient(APIView):
    @swagger_auto_schema(request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=['username','fullname', 'email','password'],
        properties={
            'username': openapi.Schema(type=openapi.TYPE_STRING, description='Username of human'),
            'fullname': openapi.Schema(type=openapi.TYPE_STRING, description='Fullname please'),
            'email': openapi.Schema(type=openapi.TYPE_STRING, description='Enter email'),
            'password': openapi.Schema(type=openapi.TYPE_STRING, description='Password!!!'),
        }
    ))

    # sign up
    def post(self, request):
        username = request.data["username"]
        fullname = request.data["fullname"]
        email = request.data["email"]
        password = request.data["password"]

        fullname_split = fullname.split()
        print(fullname_split)
        first_name = ' '.join(fullname_split[:-1])
        last_name = fullname_split[-1]

        try:
            new_user = User.objects.create_user(username=username, email=email, password=password, first_name=first_name, last_name= last_name)
            new_user.save()
            return Response({"status":status.HTTP_200_OK,"message":"created successfully","username": username, "email":email})
        except ValueError:
            print(ValueError)
            return Response({"status":status.HTTP_400_BAD_REQUEST, "error message": "created fail"})



# TODO make authenticated before create

class AuthenSignupAdmin(APIView):
    @swagger_auto_schema(request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=['username', 'email','password'],
        properties={
            'username': openapi.Schema(type=openapi.TYPE_STRING, description='Username of human'),
            'email': openapi.Schema(type=openapi.TYPE_STRING, description='Enter email'),
            'password': openapi.Schema(type=openapi.TYPE_STRING, description='Password!!!'),
        }
    ))

    # sign in admin
    def post(self, request):
        username = request.data["username"]
        email = request.data["email"]
        password = request.data["password"]
        try:
            new_user = User.objects.create_user(username=username, email=email, password=password, is_superuser = True)
            new_user.save()
            return Response({"status":status.HTTP_200_OK,"message":"created successfully","username": username, "email":email})
        except ValueError:
            print(ValueError)
            return Response({"status":status.HTTP_400_BAD_REQUEST, "error message": "created fail"})









