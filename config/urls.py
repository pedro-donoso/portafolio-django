from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from productos import views

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),

    # Productos
    path('', views.lista_productos, name='lista_productos'),
    path('productos/<int:pk>/', views.detalle_producto, name='detalle_producto'),
    path('productos/agregar/', views.agregar_producto, name='agregar_producto'),
    path('productos/<int:pk>/editar/', views.editar_producto, name='editar_producto'),
    path('productos/<int:pk>/eliminar/', views.eliminar_producto, name='eliminar_producto'),
    path('dashboard/', views.dashboard, name='dashboard'),

    # Autenticación
    path('accounts/login/', auth_views.LoginView.as_view(), name='login'),
    path('accounts/logout/', views.logout_view, name='logout'),
    path('accounts/registro/', views.registro, name='registro'),
]

# Servir archivos media en desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
