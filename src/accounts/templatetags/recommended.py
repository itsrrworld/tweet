from django import template
from django.contrib.auth import get_user_model

from accounts.models import userProfile

register = template.Library()


User = get_user_model()

@register.inclusion_tag("accounts/snippets/recommend.html")
def recommended(user):
    if isinstance(user, User):
        qs = userProfile.objects.recommended(user)
        return {"recommended": qs}
