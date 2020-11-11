from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import gettext as _


class Size(models.Model):
    width = models.PositiveSmallIntegerField(verbose_name=_('Szerokość'), null=True)
    height = models.PositiveSmallIntegerField(verbose_name=_('Wysokość'), null=True)

    def __str__(self):
        return '{}x{}'.format(self.width, self.height)

    class Meta:
        verbose_name = _('Rozmiar')
        verbose_name_plural = _('Rozmiar')


class Image(models.Model):
    name = models.CharField(max_length=250, verbose_name=_('Zdjęcie'), null=True)
    file = models.ImageField(upload_to='main_imgs/', default='main_imgs/none.jpg', verbose_name=_('Plik'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Stworzone'))
    creator = models.ForeignKey('users.User', on_delete=models.CASCADE, verbose_name=_('Twórca'))
    exp_date = models.PositiveBigIntegerField(
        validators=[MaxValueValidator(30000), MinValueValidator(30)],
        null=True,
        verbose_name=_('Wygaśnięcie'),
        blank=True
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Zdjęcie')
        verbose_name_plural = _('Zdjęcia')


class Plan(models.Model):
    name = models.CharField(max_length=250, verbose_name=_('Nazwa planu'), null=True)
    original_size = models.BooleanField(default=False, verbose_name=_('Oryginalne zdjęcie'))
    exp_date = models.BooleanField(default=False, verbose_name=_('Wygasanie'))
    size = models.ManyToManyField(Size, verbose_name=_('Rozmiar'), blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Plan')
        verbose_name_plural = _('Plany')


def create_plans(apps, schema_editor):
    from users.models import User
    BASIC = 'basic'
    PREMIUM = 'premium'
    ENTERPRISE = 'enterprise'
    PLAN_NAME = {
        BASIC: _('basic'),
        PREMIUM: _('premium'),
        ENTERPRISE: _('enterprise')
    }
    try:
        User.objects.create_superuser(username='admin', password='admin')
        first_size = Size.objects.create(width=200, height=200)
        second_size = Size.objects.create(width=400, height=400)

        bas = Plan.objects.create(name=BASIC, original_size=False, exp_date=False)
        bas.size.add(first_size)

        prem = Plan.objects.create(name=PREMIUM, original_size=True, exp_date=False)
        prem.size.add(first_size, second_size)

        ent = Plan.objects.create(name=ENTERPRISE, original_size=True, exp_date=True)
        ent.size.add(first_size, second_size)
    except:
        pass
