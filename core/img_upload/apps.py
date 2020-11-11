from django.apps import AppConfig
from django.db.models.signals import post_migrate
from django.utils.translation import gettext as _


def create_groups(sender, **kwargs):
    from img_upload.models import Size, Plan
    BASIC = 'basic'
    PREMIUM = 'premium'
    ENTERPRISE = 'enterprise'
    PLAN_NAME = {
        BASIC: _('basic'),
        PREMIUM: _('premium'),
        ENTERPRISE: _('enterprise')
    }
    try:
        print('cos')
        first_size = Size.objects.create(width=200, height=200)
        second_size = Size.objects.create(width=400, height=400)

        bas = Plan.objects.create(name=BASIC, original_size=True, exp_date=False)
        bas.add(first_size)

        prem = Plan.objects.create(name=PREMIUM, original_size=True, exp_date=False)
        prem.size.add(first_size, second_size)

        ent = Plan.objects.create(name=ENTERPRISE, original_size=True, exp_date=False)
        ent.size.add(first_size, second_size)
        print('dziala :)')
    except:
        pass


class ImgUploadConfig(AppConfig):
    name = 'img_upload'

    def ready(self):
        post_migrate.connect(create_groups, sender=self)
