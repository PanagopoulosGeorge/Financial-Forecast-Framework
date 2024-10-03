from django.db import models
from institution.models import Institutions

class Indicators(models.Model):
    inst_instid = models.ForeignKey(Institutions, models.DO_NOTHING, db_column='inst_instid')
    indicid = models.CharField(primary_key=True, max_length=32)  # The composite primary key (indicid, inst_instid) found, that is not supported. The first column is selected.
    name = models.CharField(max_length=255)
    abbreviation = models.CharField(max_length=32)
    unit_measure = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'indicators'
        unique_together = (('indicid', 'inst_instid'),)