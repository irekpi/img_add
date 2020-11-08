from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext as _
from django.contrib.auth.models import Group
from django.core.validators import MaxValueValidator, MinValueValidator


class Image(models.Model):
    name = models.CharField(max_length=250, verbose_name=_('Zdjęcie'), null=True)
    file = models.ImageField(upload_to='main_imgs/', default='main_imgs/none.jpg', verbose_name=_('Plik'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Stworzone'))
    creator = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_('Twórca'))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Zdjęcie')
        verbose_name_plural = _('Zdjęcia')


class Plan(models.Model):
    group = models.OneToOneField(Group, on_delete=models.CASCADE)
    name = models.CharField(max_length=250, verbose_name=_('Nazwa planu'), null=True)
    width = models.PositiveSmallIntegerField(verbose_name=_('Szerokość'), null=True)
    height = models.PositiveSmallIntegerField(verbose_name=_('Wysokość'), null=True)
    original_size = models.BooleanField(default=False, verbose_name=_('Oryginalne zdjęcie'))
    exp_date = models.PositiveBigIntegerField(
        validators=[MaxValueValidator(30000), MinValueValidator(30)],
        null=True,
        verbose_name=_('Wygaśnięcie'),
        blank=True
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Plan')
        verbose_name_plural = _('Plany')
