from django.shortcuts import render
from rest_framework.authtoken.models import Token
# from django.contrib.auth.models import User
from rest_framework.decorators import api_view, permission_classes
from django.http import JsonResponse
from rest_framework.permissions import AllowAny, IsAuthenticated
import base64

from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken

from accounts.models import CustomUser
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.core.exceptions import ObjectDoesNotExist
from django.core.files.uploadedfile import InMemoryUploadedFile
from io import BytesIO
from django.db import IntegrityError
from django.contrib.auth.hashers import make_password

# accounts/views.py
@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    try:
        email = request.data["email"]
        password = request.data["password"]
        firstname = request.data["firstname"]
        lastname = request.data["lastname"]

        # Validate password
        try:
            validate_password(password)
        except ValidationError as e:
            # Return an error response if the password is invalid
            return JsonResponse({"error": e.messages}, status=400)

        user = CustomUser.objects.create_user(email=email, password=password, username=email, firstname=firstname,
                                              lastname=lastname)
        user.save()
        # token = Token.objects.create(user=user)
        token = RefreshToken.for_user(user)
        return JsonResponse({
            # "token": token.key,
            # "user": user.__str__(),
            "access": str(token.access_token),
            "refresh": str(token),
            "email": user.email,
            "firstname": user.firstname,
            "lastname": user.lastname,
            "is_admin": user.is_superuser
        })
    except IntegrityError:
        return JsonResponse({"error": "A user with this email already exists"}, status=400)


@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    email = request.data["email"]
    password = request.data["password"]

    user = CustomUser.objects.get(email=email)
    if user.check_password(password):
        # token = Token.objects.get(user=user)
        token = RefreshToken.for_user(user)
        if user.profile_picture:
            with open(user.profile_picture.path, "rb") as image_file:
                profile_picture = base64.b64encode(image_file.read()).decode("utf-8")
        return JsonResponse({
            # "token": token.key,
            # "user": user.__str__(),
            "access": str(token.access_token),
            "refresh": str(token),
            "email": user.email,
            "firstname": user.firstname,
            "lastname": user.lastname,
            "profile_picture": profile_picture if user.profile_picture else None,
            "is_admin": user.is_superuser
        })

    # Remaining code for login


# def get_user_from_token(request):
#     auth_header = request.headers.get('Authorization')
#     if auth_header is None or not auth_header.startswith('Bearer '):
#         return JsonResponse({"error": "Invalid token header"}, status=400)
#
#     token_str = auth_header.split(' ')[1]
#
#     # Authenticate the token
#     jwt_authenticator = JWTAuthentication()
#     try:
#         validated_token = jwt_authenticator.get_validated_token(token_str)
#         user = jwt_authenticator.get_user(validated_token)
#         return user
#     except AuthenticationFailed:
#         return JsonResponse({"error": "Invalid token"}, status=401)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def update(request):
    try:
        # user = get_user_from_token(request)
        # if isinstance(user, JsonResponse):
        #     return user

        user = request.user

        email = request.data["email"]
        firstname = request.data["firstname"]
        lastname = request.data["lastname"]
        profile_picture = request.data["profile_picture"]

        # # Find the user associated with the token
        # token_user = Token.objects.get(key=token).user

        # Update user fields with new values

        if email and email != user.email:
            # Check if the new email already exists
            if CustomUser.objects.filter(email=email).exists():
                return JsonResponse({"error": "A user with this email already exists"}, status=400)
            user.email = email

        user.firstname = firstname
        user.lastname = lastname

        if profile_picture:
            # Decode image data
            image_data = base64.b64decode(profile_picture)
            # Check image size
            max_image_size = 5000000  # Maximum image size in bytes
            if len(image_data) > max_image_size:
                return JsonResponse({"error": f"Image size exceeds {max_image_size} bytes"}, status=400)
            # Save image if it conforms to maximum size
            image_file = BytesIO(image_data)
            user.profile_picture.save("profile_picture.png",
                                            InMemoryUploadedFile(image_file, None, "profile_picture.png", "image/png",
                                                                 len(image_data), None))
        user.save()

        if user.profile_picture:
            with open(user.profile_picture.path, "rb") as image_file:
                profile_picture = base64.b64encode(image_file.read()).decode("utf-8")

        return JsonResponse({
            "email": user.email,
            "firstname": user.firstname,
            "lastname": user.lastname,
            "profile_picture": profile_picture if user.profile_picture else None,
            "is_admin": user.is_superuser
        })
    except KeyError:
        return JsonResponse({"error": "Missing fields"}, status=400)
    except Token.DoesNotExist:
        return JsonResponse({"error": "Invalid token"}, status=401)
    except ObjectDoesNotExist:
        return JsonResponse({"error": "Account not found"}, status=404)
    except IntegrityError:
        return JsonResponse({"error": "A user with this email already exists"}, status=400)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def update_password(request):
    try:
        user = request.user

        # email = request.data["email"]
        old_password = request.data["old_password"]
        new_password = request.data["new_password"]

        # Check if the old password is correct
        if not user.check_password(old_password):
            return JsonResponse({"error": "Incorrect old password"}, status=400)

        if old_password == new_password:
            return JsonResponse({"error": "New password can't be the same as the old password"}, status=400)


        # Validate the new password
        try:
            validate_password(new_password)
        except ValidationError as e:
            return JsonResponse({"error": e.messages}, status=400)

        # Update the password
        user.password = make_password(new_password)
        user.save()

        return JsonResponse({"message": "Password updated successfully"})
    except KeyError:
        return JsonResponse({"error": "Missing fields"}, status=400)
    except Token.DoesNotExist:
        return JsonResponse({"error": "Invalid token"}, status=401)
    except ObjectDoesNotExist:
        return JsonResponse({"error": "Account not found"}, status=404)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_user(request):
    try:
        user = request.user


        # email = request.data["email"]
        # password = request.data["password"]
        #
        # # Find the user associated with the token
        # token_user = Token.objects.get(key=token).user
        #
        # if token_user.email != email:
        #     return JsonResponse({"error": "Account not found"}, status=400)
        #
        # # Check if the password is correct
        # if not token_user.check_password(password):
        #     return JsonResponse({"error": "Incorrect password"}, status=400)

        # Delete the user
        user.delete()

        ### TO-DO : Ajouter pour supprimer le token de l'user

        return JsonResponse({"message": "User deleted successfully"})
    except KeyError:
        return JsonResponse({"error": "Missing fields"}, status=400)
    except Token.DoesNotExist:
        return JsonResponse({"error": "Invalid token"}, status=401)
    except ObjectDoesNotExist:
        return JsonResponse({"error": "Account not found"}, status=404)