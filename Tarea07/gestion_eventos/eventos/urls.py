from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.listar_eventos, name='listar_eventos'),
    path('evento/<int:evento_id>/', views.detalle_evento, name='detalle_evento'),
    path('crear/', views.crear_evento, name='crear_evento'),
    path('registrar/<int:evento_id>/', views.registrar_usuario_evento, name='registrar_usuario_evento'),
    path('eliminar/<int:evento_id>/', views.eliminar_evento, name='eliminar_evento'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('perfil/', views.perfil_usuario, name='perfil_usuario'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/eventos/'), name='logout'),
    path('evento/actualizar/<int:evento_id>/', views.actualizar_evento, name='actualizar_evento'),

    # Rutas para consultas avanzadas
    path('evento/cantidad_usuarios/<int:evento_id>/', views.cantidad_usuarios_registrados, name='cantidad_usuarios_registrados'),
    path('usuarios/mas_activos/', views.usuarios_mas_activos, name='usuarios_mas_activos'),
    path('usuario/eventos_organizados/<int:usuario_id>/', views.eventos_organizados_por_usuario, name='eventos_organizados_por_usuario'),
    path('eventos/mes/<int:year>/<int:month>/', views.eventos_mes, name='eventos_mes'),  # Corrige la ruta
]
