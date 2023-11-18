from django.contrib import admin
from .models import ConfDiaSemana
# Register your models here.

@admin.register(ConfDiaSemana)
class ConfDiaSemanaAdmin(admin.ModelAdmin):
    list_display = ['dia_da_semana', 'valor_minimo', 'valor_maximo']