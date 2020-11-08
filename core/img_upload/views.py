from django.shortcuts import render, redirect, HttpResponse
from img_upload.models import Image
from img_upload.serializers import ImageSerializer, UserSerializer
from rest_framework import viewsets
from django.contrib.auth.models import User
from rest_framework import filters, permissions
from django.utils.translation import gettext as _
from rest_framework.response import Response
from django.contrib.auth.models import Group
from django.views.generic.detail import DetailView
from django.urls import reverse_lazy
from django.http import JsonResponse
from rest_framework.reverse import reverse

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
        groups = []
        if self.request.user.groups.exists():
            for group in request.user.groups.all():
                groups.append(group.name)
        # for
        # group = {
        #     itemGroup.objects.all()}
        # for item in group:
        #     print('cos')item.plan.width
        #     cos = Group.objects.get(name=item)
        for item in serializer.data:
            id_numb = '{}'.format(Image.objects.filter(name=item['name']).first().id)

            if 'basic' in groups:
                item.update({'file': reverse('img:img_url', args=id_numb, request=request)})
            if 'premium' in groups:
                item.update({'premium': reverse('img:img_url', args=id_numb, request=request)})
            if 'enterprise' in groups:
                item.update({'enter': reverse('img:img_url', args=id_numb, request=request)})
        return Response(serializer.data)

    def get_serializer_context(self):
        context = super(ImagesViewSet, self).get_serializer_context()

        return context


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.filter()
    serializer_class = UserSerializer
    filter_backends = (filters.OrderingFilter,)
    filter_fields = ('first_name')


class ImgView(DetailView):
    model = Image
    template_name = 'img_upload/photo.html'

    def get_context_data(self, **kwargs):
        context = super(ImgView, self).get_context_data()
        plan = self.request.user.groups.first().plan
        context.update({
            'width': plan.width,
            'height': plan.height
        })
        return context
