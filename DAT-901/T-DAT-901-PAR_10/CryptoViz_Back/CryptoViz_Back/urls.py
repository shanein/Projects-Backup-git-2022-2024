"""
URL configuration for CryptoViz_Back project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from accounts import views as accountsviews
from crypto import views as cryptoViews

urlpatterns = [
    path('admin/', admin.site.urls),

    path('register/', accountsviews.register),
    path('login/', accountsviews.login),
    path('edit/', accountsviews.update),
    path('password/', accountsviews.update_password),
    path('delete/', accountsviews.delete_user),

    path('crypto/', cryptoViews.get_crypto),
    path('cryptos/', cryptoViews.get_cryptos),
    path('detail/', cryptoViews.get_crypto_info),
    path('variation/', cryptoViews.get_crypto_info),


    path('create-crypto/', cryptoViews.create_crypto),
    path('delete-crypto/', cryptoViews.delete_crypto),

    path('subscribe-crypto/', cryptoViews.crypto_like),
    path('unsubscribe-crypto/', cryptoViews.crypto_like_delete),
    path('subscriptions-crypto/', cryptoViews.crypto_like_list),

]
