from datetime import datetime

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
                    item.update({'height_{} width_{}'.format(height, width): reverse(
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
