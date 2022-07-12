import django
import csv
import os
import sys

sys.path.append('C:\\Users\\JungJiYong\\PycharmProjects\\HotspotProject\\category')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'category.settings')
django.setup()

from myApp.models import Hotspot

def insertHotspot():
    with open('./csvfile/20220623012515_인기관광지_전체.csv') as in_file:
        rd = csv.reader(in_file)
        next(rd, None)
        for line in rd:
            Hotspot.objects.create(name=line[1], address=line[2], category=line[3], search=line[4])


insertHotspot()