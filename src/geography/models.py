from django.db import models

class Area(models.Model):
    areaid = models.CharField(primary_key=True, max_length=36)
    name = models.CharField(max_length=480)
    description = models.CharField(max_length=480, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'area'
