from django.contrib.auth.models import User

from django.db import models






class Categoria(models.Model):
    nombre = models.CharField(max_length=100, verbose_name='Nombre')
    descripcion = models.TextField(blank=True, verbose_name='Descripción')
   


    class Meta:
        verbose_name = 'Categoría'
        verbose_name_plural = 'Categorías'
        ordering = ['nombre']
        

    def __str__(self):
        
        return self.nombre




class Producto(models.Model):
    
    nombre = models.CharField(max_length=200, verbose_name="Nombre del Producto")
    descripcion = models.TextField(verbose_name='Descripción')
    precio = 
        models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Precio')
    stock = models.IntegerField(default=0, verbose_name='Stock')
    categoria = models.ForeignKey(
    Categoria,
    on_delete=models.CASCADE,
    related_name='productos',
    verbose_name='Categoría'
    )

    fecha_creacion = 
        models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Creación")
    usuario_creador = models.ForeignKey(
    User,
    on_delete=models.SET_NULL,
    null=True,
    verbose_name="Creado por"
    )
    activo = models.BooleanField(default=True, verbose_name='Activo')
    imagen = models.ImageField(
    upload_to='productos/',
    blank=True,
    null=True,
    verbose_name='Imagen'
    )
    


    class Meta:
    verbose_name = 'Producto'
    verbose_name_plural = 'Productos'
    ordering = ['-fecha_creacion']
    permissions = [
    ('puede_ver_estadisticas', "Puede ver estadísticas de productos"),
    ]


    def __str__(self):
        return f"{self.nombre} - ${self.precio}"
