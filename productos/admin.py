from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import Producto



@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'precio', 'stock', 'activo', 'usuario_creador', 'fecha_creacion']
    list_filter = ['activo', 'categoria', 'fecha_creacion']
    search_fields = ['nombre', 'descripcion']
    list_editable = ['precio', 'stock', 'activo']
    readonly_fields = ['fecha_creacion', 'usuario_creador']
    date_hierarchy = 'fecha_creacion'

    fieldsets = (
        ('Información Básica', {
            'fields': ('nombre', 'descripcion')
        }),
        ('Precios e Inventario', {
            'fields': ('precio', 'stock')
        }),
        ('Estado', {
            'fields': ('activo',)
        }),
        ('Imagen', {
            'fields': ('imagen',),
        }),
        ('Metadatos', {
            'fields': ('fecha_creacion', 'usuario_creador'),
            'classes': ('collapse',)
        }),
    )

    def save_model(self, request, obj, form, change):
        if not change:
            obj.usuario_creador = request.user
        super().save_model(request, obj, form, change)

# Personalizar User Admin
class UserAdminCustom(BaseUserAdmin):
    list_display = ['username', 'email', 'first_name', 'last_name', 'is_staff', 'productos_creados']

    def productos_creados(self, obj):
        return Producto.objects.filter(usuario_creador=obj).count()
    productos_creados.short_description = 'Productos'

admin.site.unregister(User)
admin.site.register(User, UserAdminCustom)

# Personalizar títulos
admin.site.site_header = "🛒 Administración de Mi Tienda"
admin.site.site_title = "Admin Productos"
admin.site.index_title = "Panel de Control"
