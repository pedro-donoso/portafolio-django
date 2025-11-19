from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import Producto

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'precio', 'stock', 'activo', 'tiene_imagen', 'usuario_creador', 'fecha_creacion']
    list_filter = ['activo', 'fecha_creacion']
    search_fields = ['nombre', 'descripcion']
    list_editable = ['precio', 'stock', 'activo']
    readonly_fields = ['fecha_creacion', 'usuario_creador', 'vista_previa_imagen']
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
            'fields': ('imagen_url', 'vista_previa_imagen'),
            'description': 'Proporciona la URL de una imagen externa.'
        }),
        ('Metadatos', {
            'fields': ('fecha_creacion', 'usuario_creador'),
            'classes': ('collapse',)
        }),
    )

    def tiene_imagen(self, obj):
        return '✓' if obj.get_imagen() else '✗'
    tiene_imagen.short_description = 'Imagen'

    def vista_previa_imagen(self, obj):
        if obj.get_imagen():
            from django.utils.html import format_html
            return format_html(
                '<img src="{}" style="max-height: 200px; max-width: 300px; object-fit: contain;" />',
                obj.get_imagen()
            )
        return "Sin imagen"
    vista_previa_imagen.short_description = 'Vista Previa'

    def save_model(self, request, obj, form, change):
        if not change:
            obj.usuario_creador = request.user
        super().save_model(request, obj, form, change)

class UserAdminCustom(BaseUserAdmin):
    list_display = ['username', 'email', 'first_name', 'last_name', 'is_staff', 'productos_creados']

    def productos_creados(self, obj):
        return Producto.objects.filter(usuario_creador=obj).count()
    productos_creados.short_description = 'Productos'

admin.site.unregister(User)
admin.site.register(User, UserAdminCustom)

admin.site.site_header = "🛒 Administración de Mi Tienda"
admin.site.site_title = "Admin Productos"
admin.site.index_title = "Panel de Control"
