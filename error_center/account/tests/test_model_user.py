from django.core.exceptions import ValidationError
from django.test import TestCase
from django.core import mail

from error_center.account.models import User


class UserModelTest(TestCase):
    def setUp(self) -> None:
        self.user_common = User.objects.create_user(
            first_name="Fulano",
            last_name="de Tal",
            email="fulano@xpto.com",
            password="xpto123"
        )
        self.user_admin = User.objects.create_superuser(
            first_name="Beltrano",
            last_name="de Tal",
            email="beltrano@xpto.com",
            password="xpto123"
        )

    def test_create_user(self):
        """"Must return True if exist users"""
        self.assertTrue(User.objects.exists())

    def test_email_error(self):
        """Must validate if email is valid"""
        user = User(
            first_name="Ciclano",
            last_name="de Tal",
            email="ciclano",
            password="xpto123"
        )
        self.assertRaises(ValidationError, user.full_clean)

    def test_user_is_staff(self):
        """Must return True if user is staff"""
        self.assertTrue(self.user_admin.is_staff)

    def test_user_is_not_staff(self):
        """Must return False if user not is staff"""
        self.assertFalse(self.user_common.is_staff)

    def test_full_name(self):
        """Must return full name of user"""
        self.assertEqual(self.user_common.get_full_name(), "Fulano de Tal")
        self.assertEqual(self.user_admin.get_full_name(), "Beltrano de Tal")

    def test_short_name(self):
        """Must return short name of user"""
        self.assertEqual(self.user_common.get_short_name(), "Fulano Tal")
        self.assertEqual(self.user_admin.get_short_name(), "Beltrano Tal")

    def test_str(self):
        """Checks if the __str__ method is the same as the user's full name"""
        self.assertEqual(str(self.user_common), "Fulano de Tal")
        self.assertEqual(str(self.user_admin), "Beltrano de Tal")

    def test_get_user_by_email(self):
        """Must return user by email"""
        u = User.objects.get(email="fulano@xpto.com")
        self.assertTrue(self.user_common, u)

    def test_send_email(self):
        self.user_common.email_user('Cadastro realizado com sucesso',
                                    'O seu cadastro foi realizado com sucesso no sistema.',
                                    'suporte@xpto.com',
                                    fail_silently=False)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, 'Cadastro realizado com sucesso')