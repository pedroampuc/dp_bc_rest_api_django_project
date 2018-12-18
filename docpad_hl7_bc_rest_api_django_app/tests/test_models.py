from django.test import TestCase
from model_mommy import mommy
from docpad_hl7_bc_rest_api_django_app.models import Transaction


class TestTransactionModel(TestCase):

    def setUp(self):
        self.transaction = mommy.make(Transaction, address= "test address", transaction="{1230h9r23n29r3293h23}",
                                      public_key="dasj0239jd02j3d023jd0293dj2930dj2093dj2093dj2093")

    def test_transaction(self):
        self.assertTrue(isinstance(self.transaction, Transaction))
        self.assertEquals(self.transaction.__str__(),self.transaction.address)
