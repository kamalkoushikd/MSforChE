from django.contrib import admin
from .models import Element

@admin.register(Element)
class ElementAdmin(admin.ModelAdmin):
    list_display = ('atomic_number', 'symbol', 'name', 'atomic_mass', 'group_block', 'period_number', 'group_number',)
    list_filter = ('group_block', 'standard_state', 'period_number', 'group_number')
    search_fields = ('name', 'symbol')
    ordering = ('atomic_number',)

