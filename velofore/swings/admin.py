from django.contrib import admin
from .models import Swing


class SwingAdmin(admin.ModelAdmin):
    model = Swing
    list_display = ('user', 'speed', 'date_created')
    list_filter = ('user', 'speed', 'date_created')

    fieldsets = (
        (None, {'fields': ('date_created', 'user', 'speed', 'is_active', 'note',  'recording')}),
    )
    
    readonly_fields = ('date_created',)
admin.site.register(Swing, SwingAdmin)