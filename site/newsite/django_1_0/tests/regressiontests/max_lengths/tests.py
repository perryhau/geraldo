from unittest import TestCase
from django.db import DatabaseError
from regressiontests.max_lengths.models import PersonWithDefaultMaxLengths, PersonWithCustomMaxLengths

class MaxLengthArgumentsTests(TestCase):
        
    def verify_max_length(self, model,field,length):
        self.assertEquals(model._meta.get_field(field).max_length,length)
        
    def test_default_max_lengths(self):
        self.verify_max_length(PersonWithDefaultMaxLengths, 'email', 75)
        self.verify_max_length(PersonWithDefaultMaxLengths, 'vcard', 100)
        self.verify_max_length(PersonWithDefaultMaxLengths, 'homepage', 200)
        self.verify_max_length(PersonWithDefaultMaxLengths, 'avatar', 100)

    def test_custom_maxlengths(self):
        self.verify_max_length(PersonWithCustomMaxLengths, 'email', 384)
        self.verify_max_length(PersonWithCustomMaxLengths, 'vcard', 1024)
        self.verify_max_length(PersonWithCustomMaxLengths, 'homepage', 256)
        self.verify_max_length(PersonWithCustomMaxLengths, 'avatar', 512)

class MaxLengthORMTests(TestCase):

    def test_custom_max_lengths(self):
        args = {
            "email": "someone@example.com",
            "vcard": "vcard",
            "homepage": "http://example.com/",
            "avatar": "me.jpg"
        }

        for field in ("email", "vcard", "homepage", "avatar"):
            new_args = args.copy()
            new_args[field] = "X" * 250 # a value longer than any of the default fields could hold.
            p = PersonWithCustomMaxLengths.objects.create(**new_args)
            self.assertEqual(getattr(p, field), ("X" * 250))