from django.shortcuts import render, get_object_or_404, redirect
from .models import Evento, RegistroEvento
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models import Count
from datetime import timedelta
from .forms import EventoForm
from django.contrib.auth.decorators import login_required
from datetime import datetime

# Vista para mostrar el perfil del usuario
@login_required
def perfil_usuario(request):
    return render(request, 'registration/perfil_usuario.html', {'user': request.user})

# Vista para crear un nuevo evento
@login_required
def crear_evento(request):
    if request.method == 'POST':
        form = EventoForm(request.POST)
        if form.is_valid():
            evento = form.save(commit=False)
            evento.organizador = request.user  # Asignar el usuario autenticado como organizador
            evento.save()
            return redirect('listar_eventos')
    else:
        form = EventoForm()
    return render(request, 'crear_evento.html', {'form': form})

# Vista para registrar un usuario en un evento
@login_required
def registrar_usuario_evento(request, evento_id):
    evento = get_object_or_404(Evento, pk=evento_id)
    if not RegistroEvento.objects.filter(usuario=request.user, evento=evento).exists():
        RegistroEvento.objects.create(usuario=request.user, evento=evento)
    return redirect('detalle_evento', evento_id=evento_id)

# Listar todos los eventos
@login_required
def listar_eventos(request):
    eventos = Evento.objects.all()
    
    # Si hay una solicitud GET con parámetros de año y mes
    year = request.GET.get('year')
    month = request.GET.get('month')
    
    if year and month:
        return redirect('eventos_mes', year=int(year), month=int(month))

    return render(request, 'listar_eventos.html', {'eventos': eventos})

# Vista para eliminar un evento
@login_required
def eliminar_evento(request, evento_id):
    evento = get_object_or_404(Evento, pk=evento_id)
    evento.delete()
    return redirect('listar_eventos')

# Consultar la cantidad de usuarios registrados en un evento específico
@login_required
def cantidad_usuarios_registrados(request, evento_id):
    evento = get_object_or_404(Evento, pk=evento_id)
    registros = RegistroEvento.objects.filter(evento=evento).count()
    return render(request, 'cantidad_usuarios_registrados.html', {'evento': evento, 'registros': registros})

# Consultar eventos del mes actual
@login_required
def eventos_mes(request, year, month):
    # Procesamiento para eventos del mes especificado
    year = int(year)
    month = int(month)

    # Obtener el primer y último día del mes solicitado
    primer_dia_mes = datetime(year, month, 1)
    if month == 12:
        ultimo_dia_mes = datetime(year + 1, 1, 1) - timedelta(days=1)
    else:
        ultimo_dia_mes = datetime(year, month + 1, 1) - timedelta(days=1)
    
    # Filtrar eventos dentro del mes especificado
    eventos = Evento.objects.filter(fecha_inicio__gte=primer_dia_mes, fecha_inicio__lte=ultimo_dia_mes)
    return render(request, 'eventos_mes.html', {'eventos': eventos, 'year': year, 'month': month})

# Consultar los usuarios más activos
@login_required
def usuarios_mas_activos(request):
    usuarios_activos = User.objects.annotate(eventos_count=Count('registroevento')).order_by('-eventos_count')[:10]
    return render(request, 'usuarios_mas_activos.html', {'usuarios_activos': usuarios_activos})

# Consultar eventos organizados por un usuario específico
@login_required
def eventos_organizados_por_usuario(request, usuario_id):
    usuario = get_object_or_404(User, pk=usuario_id)
    eventos = Evento.objects.filter(organizador=usuario)  # Filtrar eventos por el organizador
    return render(request, 'eventos_organizados_por_usuario.html', {'usuario': usuario, 'eventos': eventos})

# Detalle de un evento específico
def detalle_evento(request, evento_id):
    evento = get_object_or_404(Evento, pk=evento_id)
    usuario_registrado = RegistroEvento.objects.filter(evento=evento, usuario=request.user).exists()  # Verifica si el usuario ya está registrado
    registros = RegistroEvento.objects.filter(evento=evento).count()  # Cuenta los registros

    return render(request, 'detalle_evento.html', {
        'evento': evento, 
        'registros': registros,
        'usuario_registrado': usuario_registrado  # Pasa esta variable al template
    })
# Vista para actualizar un evento
@login_required
def actualizar_evento(request, evento_id):
    evento = get_object_or_404(Evento, id=evento_id)
    if request.method == 'POST':
        form = EventoForm(request.POST, instance=evento)
        if form.is_valid():
            form.save()
            return redirect('listar_eventos')  # O redirige a la vista deseada
    else:
        form = EventoForm(instance=evento)
    return render(request, 'actualizar_evento.html', {'form': form, 'evento': evento})
