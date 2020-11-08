from django.apps import AppConfig
from django.db.models.signals import post_migrate
from django.utils.translation import gettext as _

# TODO
# noqa This part of code should be in separate User App (because in normal situation we would like to have ability to make changes in USER groups)
BASIC = 'basic'
PREMIUM = 'premium'
ENTERPRISE = 'enterprise'

GROUPS_NAME = {
    BASIC: _('basic'),
    PREMIUM: _('premium'),
    ENTERPRISE: _('enterprise')
}


def create_groups():
    from django.contrib.auth.models import Group
    try:
        Group.objects.create(name=GROUPS_NAME.get(BASIC))
        Group.objects.create(name=PREMIUM)
        Group.objects.create(name=ENTERPRISE)
    except:
        pass


class ImgUploadConfig(AppConfig):
    name = 'img_upload'

    def ready(self):
        post_migrate.connect(create_groups)
