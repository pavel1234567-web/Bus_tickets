"""
Django app configuration for tickets application.
"""

from django.apps import AppConfig


class TicketsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'tickets'
    verbose_name = 'Bilety autobusowe'

    def ready(self):
        # Import signals when app is ready
        try:
            from . import signals
        except ImportError:
            pass
