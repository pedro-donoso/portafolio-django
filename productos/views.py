from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.db.models import Q, Count, Sum
from .models import Producto, Categoria
from .forms import ProductoForm, CategoriaForm, RegistroUsuarioForm


def lista_productos(request):
    """Vista pública - Lista todos los productos activos con búsqueda y filtros"""
    query = request.GET.get("q", "")
    categoria_id = request.GET.get("categoria", "")

    productos = Producto.objects.filter(activo=True).select_related(
        "categoria", "usuario_creador"
    )

    if query:
        productos = productos.filter(
            Q(nombre__icontains=query) | Q(descripcion__icontains=query)
        )

    if categoria_id:
        productos = productos.filter(categoria_id=categoria_id)

    categorias = Categoria.objects.all()

    context = {
        "productos": productos,
        "categorias": categorias,
        "query": query,
        "categoria_seleccionada": categoria_id,
    }
    return render(request, "productos/lista_productos.html", context)


@login_required
def detalle_producto(request, pk):
    """Vista protegida - Muestra detalles de un producto"""
    producto = get_object_or_404(Producto, pk=pk)
    return render(request, "productos/detalle_producto.html", {"producto": producto})


@login_required
def agregar_producto(request):
    """Vista protegida - Formulario para agregar producto"""
    if request.method == "POST":
        form = ProductoForm(request.POST, request.FILES)
        if form.is_valid():
            producto = form.save(commit=False)
            producto.usuario_creador = request.user
            producto.save()
            messages.success(
                request, f'Producto "{producto.nombre}" agregado exitosamente.'
            )
            return redirect("lista_productos")
    else:
        form = ProductoForm()

    return render(
        request,
        "productos/form_producto.html",
        {"form": form, "titulo": "Agregar Producto"},
    )


@login_required
def editar_producto(request, pk):
    """Vista protegida - Editar producto (solo creador o admin)"""
    producto = get_object_or_404(Producto, pk=pk)

    if producto.usuario_creador != request.user and not request.user.is_superuser:
        messages.error(request, "No tienes permiso para editar este producto.")
        return redirect("lista_productos")

    if request.method == "POST":
        form = ProductoForm(request.POST, request.FILES, instance=producto)
        if form.is_valid():
            form.save()
            messages.success(
                request, f'Producto "{producto.nombre}" actualizado exitosamente.'
            )
            return redirect("detalle_producto", pk=producto.pk)
    else:
        form = ProductoForm(instance=producto)

    return render(
        request,
        "productos/form_producto.html",
        {"form": form, "titulo": "Editar Producto", "producto": producto},
    )


@login_required
def eliminar_producto(request, pk):
    """Vista protegida - Eliminar producto con confirmación"""
    producto = get_object_or_404(Producto, pk=pk)

    if producto.usuario_creador != request.user and not request.user.is_superuser:
        messages.error(request, "No tienes permiso para eliminar este producto.")
        return redirect("lista_productos")

    if request.method == "POST":
        nombre = producto.nombre
        producto.delete()
        messages.success(request, f'Producto "{nombre}" eliminado exitosamente.')
        return redirect("lista_productos")

    return render(request, "productos/confirmar_eliminar.html", {"producto": producto})


@login_required
@permission_required("productos.puede_ver_estadisticas", raise_exception=True)
def dashboard(request):
    """Vista con permisos especiales - Dashboard con estadísticas"""
    total_productos = Producto.objects.count()
    productos_activos = Producto.objects.filter(activo=True).count()
    valor_inventario = Producto.objects.aggregate(total=Sum("precio"))["total"] or 0

    productos_por_categoria = Categoria.objects.annotate(
        cantidad=Count("productos")
    ).order_by("-cantidad")

    context = {
        "total_productos": total_productos,
        "productos_activos": productos_activos,
        "valor_inventario": valor_inventario,
        "productos_por_categoria": productos_por_categoria,
    }
    return render(request, "productos/dashboard.html", context)


def registro(request):
    """Vista pública - Registro de nuevos usuarios"""
    if request.method == "POST":
        form = RegistroUsuarioForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password1")
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(
                request, f"¡Bienvenido {username}! Tu cuenta ha sido creada."
            )
            return redirect("lista_productos")
    else:
        form = RegistroUsuarioForm()

    return render(request, "registration/registro.html", {"form": form})
