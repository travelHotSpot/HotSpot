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

class CommentFestival(models.Model):
    comment_id = models.AutoField(primary_key=True)
    festival = models.ForeignKey('Festival', models.DO_NOTHING)
    username = models.CharField(max_length=10)
    passwd = models.CharField(max_length=10)
    content = models.TextField()
    created_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'comment_festival'

class Festival(models.Model):
    festival_id = models.BigAutoField(primary_key=True)
    festival_name = models.CharField(max_length=255, db_collation='utf8mb4_0900_ai_ci')
    latitude = models.DecimalField(max_digits=12, decimal_places=10, blank=True, null=True)
    longitude = models.DecimalField(max_digits=13, decimal_places=10, blank=True, null=True)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    image_url = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'festival'


class FestivalImg(models.Model):
    festival_img_id = models.BigAutoField(primary_key=True)
    festival = models.ForeignKey(Festival, models.DO_NOTHING)
    image_url = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'festival_img'


class FestivalInfo(models.Model):
    festival_info_id = models.BigAutoField(primary_key=True)
    festival = models.OneToOneField(Festival, models.DO_NOTHING)
    host = models.CharField(max_length=100, blank=True, null=True)
    phone_number = models.CharField(max_length=255, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    organizer_info = models.CharField(max_length=100, blank=True, null=True)
    performance_time = models.TextField(blank=True, null=True)
    place_of_event = models.TextField(blank=True, null=True)
    homepage = models.CharField(max_length=255, blank=True, null=True)
    fee = models.TextField(blank=True, null=True)
    detail_info = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'festival_info'


class Trend(models.Model):
    seq_no = models.AutoField(primary_key=True)
    day_rank = models.IntegerField()
    keyword = models.CharField(max_length=45)
    area_name = models.CharField(max_length=45)
    mobile_search = models.IntegerField()
    pc_search = models.IntegerField()
    search_sum = models.IntegerField()
    search_date = models.DateField()

    class Meta:
        managed = False
        db_table = 'trend'
