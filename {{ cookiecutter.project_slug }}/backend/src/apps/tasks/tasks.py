{% if cookiecutter.use_celery == "y" %}
from celery import shared_task


@shared_task
def ping() -> str:
    return "pong"

{% endif %}
