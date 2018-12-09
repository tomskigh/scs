# standard library
from datetime import date

# my models
from .models import Patient

# django library
from django.core import mail
from django.test import TestCase

# Create your tests here.


class EmailTest(TestCase):
    def test_send_email(self):
        # Send message.
        mail.send_mail('Test e-mail', 'To jest e-mail testowy wysłany z aplikacji <<Small Clinic>>',
                       'unikogen@gmail.com', ['tomski@unikolor.com'], fail_silently=False,)

        # Test that one message has been sent.
        self.assertEqual(len(mail.outbox), 1)

        # Verify that the subject of the first message is correct.
        self.assertEqual(mail.outbox[0].subject, 'Test e-mail')


class PatientMethodTests(TestCase):
    def setUp(self):
        dataTW = {'first_name': 'Tomasz', 'last_name': 'Wygonowski', 'postal':'85-027', 'city': 'Bydgoszcz',
                'street': 'Jagiellońska 66/3', 'phone': '+48 728 443 153', 'birthday': date(1995,4,14),
                'email': 'tomski@unikolor.com', 'ensured': True}
        dataJW = {'first_name': 'Jan', 'last_name': 'Wygonowski', 'postal':'85-027', 'city': 'Bydgoszcz',
                'street': 'Jagiellońska 66/3', 'phone': '+48 604 557 822', 'birthday': date(1999,11,29),
                'email': 'janek_w@unikolor.com', 'ensured': False}
        dataset = [dataTW, dataJW]
        for data in dataset:
            Patient.objects.create(**data)


    def test_who_is_who(self):
        """Porównuje dane"""
        tomek = Patient.objects.get(first_name='Tomasz',)
        janek = Patient.objects.get(first_name='Jan',)
        self.assertEqual(tomek.birthday > janek.birthday, False)
        self.assertEqual(tomek.birthday < janek.birthday, True)
        self.assertEqual(tomek.birthday == janek.birthday, False)
        self.assertEqual(tomek.pk > janek.pk, False, 'Janek został wcześniej zarejestrowany niż Tomek')
        self.assertEqual(tomek.pk < janek.pk, True, ' Tomek został wcześniej zarejestrowany niż Janek')
