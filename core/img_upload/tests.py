from django.test import TestCase
from img_upload.models import Image, Plan, Size

from django.utils.translation import gettext as _
from unittest.mock import MagicMock

from django.core.files import File
from datetime import datetime
from users.models import User


class SizeTestCase(TestCase):
    def setUp(self):
        self.size = Size.objects.create(width=100, height=100)

    def test_width_label(self):
        field_label = self.size._meta.get_field('width').verbose_name
        self.assertEqual(field_label, _('Szerokość'))

    def test_width(self):
        self.assertEqual(self.size.width, 100)

    def test_height_label(self):
        field_label = self.size._meta.get_field('height').verbose_name
        self.assertEqual(field_label, _('Wysokość'))

    def test_height(self):
        self.assertEqual(self.size.height, 100)

    def test_string_rep(self):
        self.assertEqual(str(self.size.__str__()), '{}x{}'.format(self.size.width, self.size.height))

    def tearDown(self) -> None:
        self.size.delete()


class PlanTestCase(TestCase):
    def setUp(self):
        self.size = Size.objects.create(width=100, height=100)
        self.plan = Plan.objects.create(name='test1', original_size=False, exp_date=False)
        self.plan.size.add(self.size)

    def test_name_label(self):
        field_label = self.plan._meta.get_field('name').verbose_name
        self.assertEqual(field_label, _('Nazwa planu'))

    def test_name(self):
        self.assertTrue(self.plan.name, 'test1')

    def test_original_size_label(self):
        field_label = self.plan._meta.get_field('original_size').verbose_name
        self.assertEqual(field_label, _('Oryginalne zdjęcie'))

    def test_original_size(self):
        self.assertFalse(self.plan.original_size)

    def test_exp_date_label(self):
        field_label = self.plan._meta.get_field('exp_date').verbose_name
        self.assertEqual(field_label, _('Wygasanie'))

    def test_exp_date(self):
        self.assertFalse(self.plan.exp_date)

    def test_size_label(self):
        field_label = self.plan._meta.get_field('size').verbose_name
        self.assertEqual(field_label, _('Rozmiar'))

    def test_size(self):
        self.assertTrue(self.plan.size.exists())

    def tearDown(self) -> None:
        self.size.delete()
        self.plan.delete()


class ImageTestCase(TestCase):

    def setUp(self):
        file_mock = MagicMock(spec=File)
        file_mock.name = 'test.img'
        self.user = User.objects.create_user(email='user@user.user', username='user', password='user')
        self.image = Image.objects.create(name='IMG', file=file_mock, created_at=datetime.now(), creator=self.user,
                                          exp_date='300')

    def test_name_label(self):
        field_label = self.image._meta.get_field('name').verbose_name
        self.assertEqual(field_label, _('Zdjęcie'))

    def test_file_label(self):
        field_label = self.image._meta.get_field('file').verbose_name
        self.assertEqual(field_label, _('Plik'))

    def test_created_at_label(self):
        field_label = self.image._meta.get_field('created_at').verbose_name
        self.assertEqual(field_label, _('Stworzone'))

    def test_creator_label(self):
        field_label = self.image._meta.get_field('creator').verbose_name
        self.assertEqual(field_label, _('Twórca'))

    def test_exp_date_label(self):
        field_label = self.image._meta.get_field('exp_date').verbose_name
        self.assertEqual(field_label, _('Wygaśnięcie'))

    def test_index_status(self):
        main = self.client.get('/')
        self.assertEqual(main.status_code, 200)

    def test_accesability_img_list(self):
        main = self.client.get('/img_list/', follow=True)
        self.assertEqual(main.status_code, 403)

    def test_view_url_img_list(self):
        self.client.login(username='user', password='user')
        main = self.client.get('/img_list/', follow=True)
        self.assertEqual(main.status_code, 200)

    def test_view_file(self):
        img_pk = self.image.pk
        site = self.client.get('/{}/100/100'.format(img_pk), follow=True)
        self.assertEqual(site.status_code, 200)

    def tearDown(self) -> None:
        self.user.delete()
        self.image.delete()
