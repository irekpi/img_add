from django.views.generic.detail import DetailView

from img_upload.models import Image


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
