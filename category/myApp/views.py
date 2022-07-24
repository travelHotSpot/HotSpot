from django.shortcuts import render
from django.db import connection
from django.core.paginator import Paginator
from .models import Festival
from .models import FestivalInfo
from .models import FestivalImg

# Create your views here.
def showTable(request):
    hotspot_list = []
    with connection.cursor() as cursor:
        sqlQuery = "SELECT * FROM testdatabase.Hotspot ORDER BY SEARCH DESC LIMIT 3"
        cursor.execute(sqlQuery)
        fetchResultQuery = cursor.fetchall()

        connection.commit()
        connection.close()

        for row in fetchResultQuery:
            hotspot_list.append({'Name': row[0], 'Address': row[1], 'Category': row[2], 'Search': row[3]})

    return render(request, 'myApp/index.html', {"hotspot": hotspot_list})


def show_festival(request):
    festivals = Festival.objects.all().values().order_by('festival_id')

    festival_pg = Paginator(festivals, 10)
    page = int(request.GET.get('page', 1))
    festival_list = festival_pg.get_page(page)

    return render(request, 'myApp/festival.html', {'festival_list': festival_list})


def festival_detail(request, festival_id):
    festival = Festival.objects.get(festival_id=festival_id)
    festival_info = FestivalInfo.objects.get(festival_id=festival_id)
    festival_img = FestivalImg.objects.filter(festival_id=festival_id)

    return render(request, 'myApp/festival_detail.html', {'festival': festival, 'festival_info': festival_info,
                                                          'festival_img': festival_img})
