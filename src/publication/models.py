from django.db import models
from indicator.models import Indicators
from institution.models import Institutions
from geography.models import Area

class Publishes(models.Model):
    inst_instid = models.ForeignKey(Institutions, models.DO_NOTHING, db_column='inst_instid', related_name='publishes_by_institution') 
    indic_indicid = models.ForeignKey(Indicators, models.DO_NOTHING, db_column='indic_indicid', related_name='publishes_by_indicator')
    area_areaid = models.ForeignKey(Area, models.DO_NOTHING, db_column='area_areaid', related_name='publishes_by_area')
    value = models.DecimalField(max_digits=25, decimal_places=5)  # max_digits and decimal_places have been guessed, as this database handles decimal fields as float
    value_normalized = models.DecimalField(max_digits=25, decimal_places=5, blank=True, null=True)  # max_digits and decimal_places have been guessed, as this database handles decimal fields as float
    date_from = models.DateField(primary_key=True)
    date_until = models.DateField()
    date_published = models.DateField(blank=True, null=True)
    date_updated = models.DateField()
    YES_NO_CHOICES = [
        ('Y', 'Yes'),
        ('N', 'No'),
    ]
    is_forecast = models.CharField(max_length=1, choices=YES_NO_CHOICES)

    class Meta:
        managed = False
        db_table = 'publishes'
        unique_together = (('inst_instid', 'indic_indicid', 'area_areaid', 'date_from', 'date_until', 'is_forecast'),)

