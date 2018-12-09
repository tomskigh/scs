# standard library
from datetime import date

# django library
from django.test import TestCase, Client


# my function
from functions.myfunctions import holidays


# Create your tests here.


class KnownValues(TestCase):

    known_holidays_2017 = {
                'New Year':  date(2017, 1, 1),
                'Epiphany': date(2017, 1, 6),
                'Easter': date(2017,4,16),
                'Easter Monday': date(2017,4,17),
                'Labour Day': date(2017,5,1),
                'Feast of the constitution third of May': date(2017,5,3),
                'Descent of the Holy Spirit': date(2017,6,4),
                "God's Body": date(2017,6,15),
                'Assumption of the Blessed Virgin Mary': date(2017,8,15),
                'All Saints Day': date(2017,11,1),
                'Independence Day': date(2017,11,11),
                'Christmas-first day': date(2017,12,25),
                'Christmas-second day': date(2017,12,26)}

    known_holidays_2018 = {
                'New Year':  date(2018, 1, 1),
                'Epiphany': date(2018, 1, 6),
                'Easter': date(2018,4,1),
                'Easter Monday': date(2018,4,2),
                'Labour Day': date(2018,5,1),
                'Feast of the constitution third of May': date(2018,5,3),
                'Descent of the Holy Spirit': date(2018,5,20),
                "God's Body": date(2018,5,31),
                'Assumption of the Blessed Virgin Mary': date(2018,8,15),
                'All Saints Day': date(2018,11,1),
                'Independence Day': date(2018,11,11),
                'Christmas-first day': date(2018,12,25),
                'Christmas-second day': date(2018,12,26)}

    known_holidays_2019 = {
                'New Year':  date(2019, 1, 1),
                'Epiphany': date(2019, 1, 6),
                'Easter': date(2019,4,21),
                'Easter Monday': date(2019,4,22),
                'Labour Day': date(2019,5,1),
                'Feast of the constitution third of May': date(2019,5,3),
                'Descent of the Holy Spirit': date(2019,6,9),
                "God's Body": date(2019,6,20),
                'Assumption of the Blessed Virgin Mary': date(2019,8,15),
                'All Saints Day': date(2019,11,1),
                'Independence Day': date(2019,11,11),
                'Christmas-first day': date(2019,12,25),
                'Christmas-second day': date(2019,12,26)}


    known_holidays_2065 = {
                'New Year':  date(2065, 1, 1),
                'Epiphany': date(2065, 1, 6),
                'Easter': date(2065,3,29),
                'Easter Monday': date(2065,3,30),
                'Labour Day': date(2065,5,1),
                'Feast of the constitution third of May': date(2065,5,3),
                'Descent of the Holy Spirit': date(2065,5,17),
                "God's Body": date(2065,5,28),
                'Assumption of the Blessed Virgin Mary': date(2065,8,15),
                'All Saints Day': date(2065,11,1),
                'Independence Day': date(2065,11,11),
                'Christmas-first day': date(2065,12,25),
                'Christmas-second day': date(2065,12,26)}

    def test_year_holidays_to_known_holidays_2017(self):
        for d in self.known_holidays_2017.values():
            result = holidays(d)
            self.assertEqual(self.known_holidays_2017, result)

    def test_year_holidays_to_known_holidays_2018(self):
        for d in self.known_holidays_2018.values():
            result = holidays(d)
            self.assertEqual(self.known_holidays_2018, result)

    def test_year_holidays_to_known_holidays_2019(self):
        for d in self.known_holidays_2019.values():
            result = holidays(d)
            self.assertEqual(self.known_holidays_2019, result)

    def test_year_holidays_to_known_holidays_2065(self):
        for d in self.known_holidays_2065.values():
            result = holidays(d)
            self.assertEqual(self.known_holidays_2065, result)


class StatusCodeTest(TestCase):
    def setUp(self):
        # Every test needs a client.
        self.client = Client()

    def test_details(self):
        # Issue a GET request.
        response_1 = self.client.get('http://localhost:8000/index/')

        # Check that the response is 200 OK.
        self.assertEqual(response_1.status_code, 200)

        # Issue a GET request.
        response_2 = self.client.get('http://localhost:8000/registration/register/')
        # Check that the response is 200 OK.
        self.assertEqual(response_2.status_code, 200)

        # Issue a GET request.
        response_3 = self.client.get('http://localhost:8000/admin/')
        # Check that the response is 302 - user is't a superuser.
        self.assertEqual(response_3.status_code, 302)

        # Issue a GET request.
        response_4 = self.client.get('http://localhost:8000/registration/register/')
        # Check that the response is 200 OK.
        self.assertEqual(response_4.status_code, 200)
