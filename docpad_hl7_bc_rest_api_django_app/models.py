# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models


# Create your models here.
class Transaction(models.Model):

    address = models.CharField(max_length=255)
    transaction = models.TextField()
    public_key = models.TextField()

    class Meta:
        verbose_name = u'Transaction'
        verbose_name_plural = u'Transactions'

    def __str__(self):
        return self.address



