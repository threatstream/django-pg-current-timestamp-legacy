# -*- coding: utf-8 -*-

from django.db import models

class TestModel(models.Model):
	value = models.CharField(max_length=100)
	created_ts = models.DateTimeField(auto_now_add=True, null=False, blank=False)
	modified_ts = models.DateTimeField(auto_now=True, null=False, blank=False)

