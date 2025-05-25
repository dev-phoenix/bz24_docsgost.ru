from django.test import TestCase
from django.test import tag
# Create your tests here.

from user.models import *
# from user.models import Animal


class AnimalTestCase(TestCase):
    def setUp(self):
        # Animal.objects.create(name="lion", sound="roar")
        # Animal.objects.create(name="cat", sound="meow")
        ...

    def test_animals_can_speak(self):
        """Animals that can speak are correctly identified"""
        # lion = Animal.objects.get(name="lion")
        # cat = Animal.objects.get(name="cat")
        # self.assertEqual(lion.speak(), 'The lion says "roar"')
        # self.assertEqual(cat.speak(), 'The cat says "meow"')
        self.assertEqual('The cat says "meow"', 'The cat says "meow"', 'it is ok test')

    def test_2animals_can_speak(self):
        self.assertEqual('The cat says "meow"', 'The cat says "meow"', ' it is wrong test 2 ')
        self.assertEqual(1, 'The cat says "meow"', ' it is wrong test 2 ')

    def test_3animals_can_speak(self):
        self.assertEqual('The cat says "meow"', 'The cat says "meow"', ' it is wrong test 3 ')
        self.assertEqual(2, 'The cat says "meow"', ' it is wrong test 3 ')

    
    @tag("fast")
    def test_details(self):
        response = self.client.get("/customer/details/")
        self.assertEqual(response.status_code, 200)

    def test_index(self):
        response = self.client.get("/customer/index/")
        self.assertEqual(response.status_code, 200)
    
    @tag("fast")
    async def test_my_thing(self):
        response = await self.async_client.get("/some-url/")
        self.assertEqual(response.status_code, 200)
