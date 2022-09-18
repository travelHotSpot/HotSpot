import django
import csv
import os
import sys

sys.path.append('C:\\Users\\JungJiYong\\PycharmProjects\\HotspotProject\\category')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'category.settings')
django.setup()

from myApp.models import TopFood

def insertHotspot():
    with open('./csvfile/food_recommend_list.csv',encoding='cp949') as in_file:
        rd = csv.reader(in_file)
        next(rd, None)
        for line in rd:
            TopFood.objects.create(place=line[0],score=line[1])


insertHotspot()