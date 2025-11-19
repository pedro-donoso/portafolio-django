from django.db import models
from django.contrib.auth.models import User

class Producto(models.Model):
    nombre = models.CharField(max_length=200, verbose_name="Nombre del Producto")
    descripcion = models.TextField(verbose_name="Descripción")
    precio = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Precio")
    stock = models.IntegerField(default=0, verbose_name="Stock")
    fecha_creacion = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Creación")
    usuario_creador = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="Creado por"
    )
    activo = models.BooleanField(default=True, verbose_name="Activo")
    imagen_url = models.URLField(
        max_length=500,
        blank=True,
        null=True,
        verbose_name="URL de Imagen",
        help_text="Ingresa la URL de una imagen (ej: https://ejemplo.com/imagen.jpg)"
    )

    class Meta:
        verbose_name = "Producto"
        verbose_name_plural = "Productos"
        ordering = ['-fecha_creacion']
        permissions = [
            ("puede_ver_estadisticas", "Puede ver estadísticas de productos"),
        ]

    def __str__(self):
        return f"{self.nombre} - ${self.precio}"

    def get_imagen(self):
        """Retorna la URL de la imagen, priorizando imagen_url sobre imagen local"""
        if self.imagen_url:
            return self.imagen_url
        elif self.imagen:
            return self.imagen.url
        return None
