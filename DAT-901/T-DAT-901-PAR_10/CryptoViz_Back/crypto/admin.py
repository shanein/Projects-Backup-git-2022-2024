from django.contrib import admin

from .models import Crypto, CryptoLike

class CryptoLikeAdmin(admin.ModelAdmin):
    model = CryptoLike
    list_display = ['user_id', 'crypto_id', 'created_at']  # Affichez les champs que vous souhaitez voir dans la liste
    list_filter = ['user_id', 'crypto_id']  # Ajoutez des filtres pour faciliter la navigation

admin.site.register(Crypto)
admin.site.register(CryptoLike, CryptoLikeAdmin)

