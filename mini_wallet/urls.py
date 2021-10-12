from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('token/', include('account.urls', namespace='account')),
    path('api/v1/wallet/', include('wallet.urls', namespace='wallet'))
]
