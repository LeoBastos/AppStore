import uuid
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.utils import timezone
from .models import User
from django.db import models


class UserCreationTest(TestCase):
    def setUp(self):
        self.email = 'test@example.com'
        self.password = '1234password'
        self.name = 'Jose Maria'
        self.user = User.objects.create_user(
            name=self.name,
            email=self.email,
            password=self.password,
        )

    def test_user_creation(self):
        self.assertTrue(isinstance(self.user, User))
        self.assertEqual(self.user.email, self.email)
        self.assertEqual(self.user.name, self.name)
        self.assertTrue(self.user.check_password(self.password))
        self.assertFalse(self.user.is_staff)
        self.assertFalse(self.user.is_superuser)
        self.assertTrue(self.user.is_active)
        self.assertIsNotNone(self.user.date_joined)
        self.assertIsNone(self.user.last_login)

    def test_superuser_creation(self):
        superuser_email = 'admin@example.com'
        superuser_password = '1234password'
        superuser = User.objects.create_superuser(
            name=self.name,
            email=superuser_email,
            password=superuser_password,
        )

        self.assertTrue(isinstance(superuser, User))
        self.assertEqual(superuser.email, superuser_email)
        self.assertEqual(superuser.name, self.name)
        self.assertTrue(superuser.check_password(superuser_password))
        self.assertTrue(superuser.is_staff)
        self.assertTrue(superuser.is_superuser)
        self.assertTrue(superuser.is_active)
        self.assertIsNotNone(superuser.date_joined)
        self.assertIsNone(superuser.last_login)

    def test_create_user_without_name(self):
        user = User.objects.create_user(
            email='test2@example.com',
            password='testpassword2',
            name = '',
        )
        self.assertEqual(user.name, '')

    def test_create_user_without_email(self):
        with self.assertRaises(ValueError):
            User.objects.create_user(
                name=self.name,
                password=self.password,
            )

    def test_create_user_with_existing_email(self):
        with self.assertRaises(Exception):
            User.objects.create_user(
                name=self.name,
                email=self.email,
                password=self.password,
            )   

    def test_user_str_representation(self):
        self.assertEqual(str(self.user), self.email)


class UserModelTest(TestCase):
    def test_fields(self):
        user = User()
        self.assertIsInstance(user.id, uuid.UUID)
        self.assertIsInstance(user.email, str)
        self.assertIsInstance(user.name, str)
        self.assertIsInstance(user.avatar.field, models.ImageField),
        self.assertIsInstance(user.is_active, bool)
        self.assertIsInstance(user.is_superuser, bool)
        self.assertIsInstance(user.is_staff, bool)
        self.assertIsInstance(user.date_joined, timezone.datetime)
        self.assertIsInstance(user.last_login, (type(None), timezone.datetime))
        self.assertEqual(user.USERNAME_FIELD, 'email')
        self.assertEqual(user.EMAIL_FIELD, 'email')
        self.assertEqual(user.REQUIRED_FIELDS, [])