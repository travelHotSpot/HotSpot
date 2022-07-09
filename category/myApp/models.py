from django.db import models

# Create your models here.
class Hotspot(models.Model):
    name = models.CharField(db_column='Name', primary_key=True, max_length=255)  # Field name made lowercase.
    address = models.CharField(db_column='Address', max_length=255)  # Field name made lowercase.
    category = models.CharField(db_column='Category', max_length=255)  # Field name made lowercase.
    search = models.BigIntegerField(db_column='Search')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Hotspot'