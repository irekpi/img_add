
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils.translation import gettext as _
from rest_framework import serializers

from img_upload.models import Image


class ImageSerializer(serializers.ModelSerializer):
    file = serializers.ImageField(max_length=None, use_url=True, allow_empty_file=False, required=True)
    name = serializers.CharField(max_length=250, label=_('Nazwa zdjęcia'), required=True)
    creator = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Image
        fields = ['name', 'file', 'creator']

    def __init__(self, *args, **kwargs):
        super(ImageSerializer, self).__init__(*args, **kwargs)
        if kwargs['context']['request'].user.plans.filter(exp_date=True).exists():
            self.fields['exp_date'] = serializers.IntegerField(
                validators=[MaxValueValidator(30000), MinValueValidator(300)],
                label=_('Wygaśnięcie'),
                required=False,
            )


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'date_joined']