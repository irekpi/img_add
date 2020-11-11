from datetime import datetime

from django.views.generic.detail import DetailView
from rest_framework import permissions
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.reverse import reverse

from img_upload.models import Image
from img_upload.serializers import ImageSerializer


class ImagesViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = Image.objects.filter()
    serializer_class = ImageSerializer

    def get_queryset(self):
        return self.queryset.filter(creator=self.request.user)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)

        for item in serializer.data:
            image = Image.objects.filter(name=item['name']).first()
            for plan in self.request.user.plans.all():
                if not plan.original_size:
                    item.pop('file')
                for img in plan.size.all():
                    height = img.height
                    width = img.width
                    item.update({'Height {} - Width {}'.format(height, width): reverse(
                        'img:img_url',
                        kwargs={
                            'pk': str(image.id),
                            'height': height,
                            'width': width
                        }, request=request)})
                if image.exp_date is not None and int(
                        (datetime.utcnow() - image.created_at.replace(tzinfo=None)).total_seconds()) < image.exp_date:
                    item.update({
                        'File with Exp date': item['file']
                    })
                elif image.exp_date is not None:
                    item.update({
                        'exp_date': 'Expired'
                    })
        return Response(serializer.data)

    def get_serializer_context(self):
        context = super(ImagesViewSet, self).get_serializer_context()

        return context


class ImgView(DetailView):
    model = Image
    template_name = 'img_upload/photo.html'

    def get_context_data(self, **kwargs):
        context = super(ImgView, self).get_context_data()
        context.update({
            'width': self.kwargs['width'],
            'height': self.kwargs['height']
        })
        return context

#
# from django.db.models.signals import post_migrate
# from django.utils.translation import gettext as _
#
# # TODO
# # noqa This part of code should be in separate User App (because in normal situation we would like to have ability to make changes in USER groups)
# BASIC = 'basic'
# PREMIUM = 'premium'
# ENTERPRISE = 'enterprise'
#
# GROUPS_NAME = {
#     BASIC: _('basic'),
#     PREMIUM: _('premium'),
#     ENTERPRISE: _('enterprise')
# }
#
#
# def create_groups():
#     from django.contrib.auth.models import Group
#     try:
#         Group.objects.create(name=GROUPS_NAME.get(BASIC))
#         Group.objects.create(name=PREMIUM)
#         Group.objects.create(name=ENTERPRISE)
#     except:
#         pass
#     #to do app congi kasly
#     def ready(self):
#         post_migrate.connect(create_groups)
