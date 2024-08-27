from django.http import JsonResponse
from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
import requests
from .models import Crypto, CryptoLike
from rest_framework import status
from django.db import IntegrityError
from rest_framework.authtoken.models import Token
import json
import os



# Any #


# Get one cryptocurrency
@api_view(['GET'])
@permission_classes([AllowAny])
def get_crypto(request):
    try:
        crypto_name = request.data["name"]
        crypto_name = crypto_name.lower()
        crypto = Crypto.objects.get(name=crypto_name)
        return JsonResponse({
            "crypto" : crypto.name
         })
    except Crypto.DoesNotExist:
        # Gérez le cas où la crypto-monnaie demandée n'existe pas dans la base de données
        return JsonResponse({"error": "Cryptocurrency not found"}, status=404)
    except Exception as e:
        # Gérez les autres exceptions possibles
        return JsonResponse({"error": str(e)}, status=500)


# Get all cryptocurrencies in database
@api_view(['GET'])
@permission_classes([AllowAny])
def get_cryptos(request):
    backup_dir = 'backups'  # Nom du dossier pour les sauvegardes
    backup_file = os.path.join(backup_dir, 'crypto_data_backup.json')  # Chemin complet vers le fichier de sauvegarde

    try:
        # Récupérer les noms des cryptomonnaies depuis la base de données
        cryptos = Crypto.objects.values_list('name', flat=True)
        if not cryptos:
            return JsonResponse({"error": "No cryptocurrencies found in the database"}, status=404)

        # Construction de l'URL avec les noms des cryptos
        url = "https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&ids=" + ','.join(cryptos) + "&order=market_cap_desc&page=1&sparkline=false&x_cg_demo_api_key=CG-2r8ib2dqpFsVk5UG5Hn38hZy"

        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            # Enregistrer les données dans un fichier JSON
            os.makedirs(backup_dir, exist_ok=True)  # Crée le dossier s'il n'existe pas
            with open(backup_file, 'w') as file:
                json.dump(data, file)
            return JsonResponse(data, safe=False)
        else:
            # Tente de récupérer les données du fichier de secours
            if os.path.exists(backup_file):
                with open(backup_file, 'r') as file:
                    backup_data = json.load(file)
                    return JsonResponse(backup_data, safe=False)
            else:
                return JsonResponse({"error": "Cryptocurrency information not found and no backup available"},
                                    status=404)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


# Get information of a specific cryptocurrency.

@api_view(['GET'])
@permission_classes([AllowAny])
def get_crypto_info(request):
    backup_dir = 'backups'
    os.makedirs(backup_dir, exist_ok=True)

    try:
        crypto_name = request.GET.get('name')

        if not crypto_name:
            return JsonResponse({"error": "Name of the cryptocurrency is required"}, status=status.HTTP_400_BAD_REQUEST)

        crypto_name = crypto_name.lower()
        crypto = Crypto.objects.get(name=crypto_name)


        if request.path == '/detail/':
            backup_file_name = f'{crypto_name}_detail_backup.json'
            url = f"https://api.coingecko.com/api/v3/coins/{crypto.name}?tickers=false&market_data=true&community_data=false&developer_data=false&sparkline=false&x_cg_demo_api_key=CG-2r8ib2dqpFsVk5UG5Hn38hZy"
        elif request.path == '/variation/':
            length = request.GET.get('length')
            backup_file_name = f'{crypto_name}_variation_{length}_backup.json'
            url = f"https://api.coingecko.com/api/v3/coins/{crypto.name}/ohlc?vs_currency=usd&days={length}&x_cg_demo_api_key=CG-2r8ib2dqpFsVk5UG5Hn38hZy"
        else:
            return JsonResponse({'error': 'Invalid URL'}, status=400)

        backup_file_path = os.path.join(backup_dir, backup_file_name)

        response = requests.get(url)
        print(response.status_code)
        if response.status_code == 1200:
            data = response.json()
            # Enregistrer les données dans un fichier JSON
            with open(backup_file_path, 'w') as file:
                json.dump(data, file)
            return JsonResponse(data, safe=False)
        else:
            # Tente de récupérer les données du fichier de secours
            if os.path.exists(backup_file_path):
                with open(backup_file_path, 'r') as file:
                    backup_data = json.load(file)
                    return JsonResponse(backup_data, safe=False)
            else:
                return JsonResponse({"error": f"Error retrieving cryptocurrency {crypto_name} and no backup available"}, status=404)

    except Crypto.DoesNotExist:
        return JsonResponse({"error": "Cryptocurrency not found"}, status=404)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

# User #

# Subscribe to a cryptocurrency
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def crypto_like(request):
    try:
        token = request.headers.get('Authorization').split()[1]
        crypto_name = request.data["name"]

        # Find the user associated with the token
        token_user = Token.objects.get(key=token).user
        crypto = Crypto.objects.get(name=crypto_name)

        if not crypto_name:
            return JsonResponse({"error": "Name of the cryptocurrency is required"}, status=400)

        if CryptoLike.objects.filter(user_id=token_user, crypto_id=crypto).exists():
            return JsonResponse({"error": "User already liked this cryptocurrency"}, status=400)

        CryptoLike.objects.create(user_id=token_user, crypto_id=crypto)

        return JsonResponse({"message": "Cryptocurrency liked successfully"}, status=201)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def crypto_like_delete(request):
    try:
        token = request.headers.get('Authorization').split()[1]
        crypto_name = request.data.get('name')

        # Find the user associated with the token
        token_user = Token.objects.get(key=token).user
        crypto = Crypto.objects.get(name=crypto_name)

        if not crypto_name:
            return JsonResponse({"error": "Name of the cryptocurrency is required"}, status=400)

        crypto_like = CryptoLike.objects.filter(user_id=token_user, crypto_id=crypto)
        if not crypto_like.exists():
            return JsonResponse({"error": "User has not liked this cryptocurrency"}, status=400)

        crypto_like.delete()

        return JsonResponse({"message": "Cryptocurrency unliked successfully"}, status=200)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def crypto_like_list(request):
    try:
        token = request.headers.get('Authorization').split()[1]
        token_user = Token.objects.get(key=token).user

        user_likes = CryptoLike.objects.filter(user_id=token_user.id)

        if user_likes.exists():
            liked_crypto_names = [crypto_like.crypto_id.name for crypto_like in user_likes]
            formatted_data = [{"crypto": {"id": name}} for name in liked_crypto_names]
            return JsonResponse(formatted_data, safe=False)
        else:
            return JsonResponse([], safe=False)


    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

# Admin #

# Create a cryptocurrency
@api_view(['POST'])
@permission_classes([IsAdminUser])
def create_crypto(request):
    crypto_params = request.data['name']

    if not crypto_params:
        return JsonResponse({"error": "Name of the cryptocurrency is required"}, status=status.HTTP_400_BAD_REQUEST)

    name = crypto_params.lower()
    url = f"https://api.coingecko.com/api/v3/coins/{name}?x_cg_demo_api_key=CG-2r8ib2dqpFsVk5UG5Hn38hZy"
    print(url)

    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise HTTPError for non-2xx responses

        if response.status_code == 429:
            return JsonResponse({"error": "You've exceeded the Rate Limit. Please try again later."},
                                status=status.HTTP_429_TOO_MANY_REQUESTS)

        if response.status_code == 200:
            # Process successful response here
            # Assuming Crypto model is imported and has create method
            crypto = Crypto.objects.create(name=name)
            return JsonResponse({"name": crypto.name}, status=status.HTTP_201_CREATED)
        else:
            return JsonResponse({"error": "Cryptocurrency not found"}, status=status.HTTP_404_NOT_FOUND)
    except requests.exceptions.RequestException:
        return JsonResponse({"error": "Error retrieving cryptocurrency information"},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    except IntegrityError:
        return JsonResponse({"error": "Cryptocurrency with this name already exists"}, status=status.HTTP_409_CONFLICT)


# Delete a cryptocurrency
@api_view(['DELETE'])
@permission_classes([IsAdminUser])
def delete_crypto(request):
    try:
        crypto_name = request.data.get('name')

        if not crypto_name:
            return JsonResponse({"error": "Name of the cryptocurrency is required"}, status=status.HTTP_400_BAD_REQUEST)

        crypto_name = crypto_name.lower()
        crypto = Crypto.objects.get(name=crypto_name)

        # Delete the user
        crypto.delete()

        return JsonResponse({"message": "Cryptocurrency deleted successfully"})
    except KeyError:
        return JsonResponse({"error": "Missing fields"}, status=400)
    except Crypto.DoesNotExist:
        # Gérez le cas où la crypto-monnaie demandée n'existe pas dans la base de données
        return JsonResponse({"error": "Cryptocurrency not found"}, status=404)
    except Exception as e:
        # Gérez les autres exceptions possibles
        return JsonResponse({"error": str(e)}, status=500)


