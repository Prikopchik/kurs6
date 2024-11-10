from django import template

register = template.Library()

@register.filter
def media_url(path):
    """Превращаем путь в полный URL для доступа к медиафайлу."""
    if path:
        return f'/media/{path}'
    return '#'
