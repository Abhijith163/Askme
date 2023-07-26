from django import template
from ..models import Like

register = template.Library()

@register.filter
def user_likes_answer(user, answer):
    return Like.objects.filter(user=user, answer=answer).exists()