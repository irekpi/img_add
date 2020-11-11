from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext as _

from img_upload.models import Plan


class User(AbstractUser):
    plans = models.ManyToManyField(Plan, verbose_name=_('Plany'), blank=True)

    class Meta:
        verbose_name = _('Użytkownik')
        verbose_name_plural = _('Użytkownicy')
