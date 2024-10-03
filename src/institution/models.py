from django.db import models

class Institutions(models.Model):
    instid = models.CharField(primary_key=True, max_length=8)
    name = models.CharField(max_length=120)
    abbreviation = models.CharField(max_length=8, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    url = models.CharField(max_length=120, blank=True, null=True)
    country = models.CharField(max_length=3, blank=True, null=True)
    type = models.CharField(max_length=3, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'institutions'