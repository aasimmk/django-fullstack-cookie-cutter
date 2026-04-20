{% if cookiecutter.use_celery == "y" %}
from django.apps import AppConfig


class TasksConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "src.apps.tasks"
    verbose_name = "Background tasks"

{% endif %}
