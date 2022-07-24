from django.shortcuts import render
from django.db import connection
from django.core.paginator import Paginator
from .models import Festival
from .models import FestivalInfo
from .models import FestivalImg
from .models import Trend


# Create your views here.
def showTable(request):
    sqlQuery = [0]* 17
    fetchResultQuery = [0]* 17
    hotspot_list = [0] * 51
    with connection.cursor() as cursor:

        sqlQuery[0] = "SELECT * FROM testdatabase.Hotspot WHERE Address LIKE '경기%' ORDER BY SEARCH DESC LIMIT 3 "
        cursor.execute(sqlQuery[0])
        fetchResultQuery[0] = cursor.fetchall()

        sqlQuery[1] = "SELECT * FROM testdatabase.Hotspot WHERE Address LIKE '강원%' ORDER BY SEARCH DESC LIMIT 3 "
        cursor.execute(sqlQuery[1])
        fetchResultQuery[1] = cursor.fetchall()

        sqlQuery[2] = "SELECT * FROM testdatabase.Hotspot WHERE Address LIKE '서울%' ORDER BY SEARCH DESC LIMIT 3 "
        cursor.execute(sqlQuery[2])
        fetchResultQuery[2] = cursor.fetchall()

        sqlQuery[3] = "SELECT * FROM testdatabase.Hotspot WHERE Address LIKE '인천%' ORDER BY SEARCH DESC LIMIT 3 "
        cursor.execute(sqlQuery[3])
        fetchResultQuery[3] = cursor.fetchall()

        sqlQuery[4] = "SELECT * FROM testdatabase.Hotspot WHERE Address LIKE '충남%' ORDER BY SEARCH DESC LIMIT 3 "
        cursor.execute(sqlQuery[4])
        fetchResultQuery[4] = cursor.fetchall()

        sqlQuery[5] = "SELECT * FROM testdatabase.Hotspot WHERE Address LIKE '충북%' ORDER BY SEARCH DESC LIMIT 3 "
        cursor.execute(sqlQuery[5])
        fetchResultQuery[5] = cursor.fetchall()

        sqlQuery[6] = "SELECT * FROM testdatabase.Hotspot WHERE Address LIKE '세종%' ORDER BY SEARCH DESC LIMIT 3 "
        cursor.execute(sqlQuery[6])
        fetchResultQuery[6] = cursor.fetchall()

        sqlQuery[7] = "SELECT * FROM testdatabase.Hotspot WHERE Address LIKE '대전%' ORDER BY SEARCH DESC LIMIT 3 "
        cursor.execute(sqlQuery[7])
        fetchResultQuery[7] = cursor.fetchall()

        sqlQuery[8] = "SELECT * FROM testdatabase.Hotspot WHERE Address LIKE '경북%' ORDER BY SEARCH DESC LIMIT 3 "
        cursor.execute(sqlQuery[8])
        fetchResultQuery[8] = cursor.fetchall()

        sqlQuery[9] = "SELECT * FROM testdatabase.Hotspot WHERE Address LIKE '경남%' ORDER BY SEARCH DESC LIMIT 3 "
        cursor.execute(sqlQuery[9])
        fetchResultQuery[9] = cursor.fetchall()

        sqlQuery[10] = "SELECT * FROM testdatabase.Hotspot WHERE Address LIKE '대구%' ORDER BY SEARCH DESC LIMIT 3 "
        cursor.execute(sqlQuery[10])
        fetchResultQuery[10] = cursor.fetchall()

        sqlQuery[11] = "SELECT * FROM testdatabase.Hotspot WHERE Address LIKE '울산%' ORDER BY SEARCH DESC LIMIT 3 "
        cursor.execute(sqlQuery[11])
        fetchResultQuery[11] = cursor.fetchall()

        sqlQuery[12] = "SELECT * FROM testdatabase.Hotspot WHERE Address LIKE '부산%' ORDER BY SEARCH DESC LIMIT 3 "
        cursor.execute(sqlQuery[12])
        fetchResultQuery[12] = cursor.fetchall()

        sqlQuery[13] = "SELECT * FROM testdatabase.Hotspot WHERE Address LIKE '전북%' ORDER BY SEARCH DESC LIMIT 3 "
        cursor.execute(sqlQuery[13])
        fetchResultQuery[13] = cursor.fetchall()

        sqlQuery[14] = "SELECT * FROM testdatabase.Hotspot WHERE Address LIKE '전남%' ORDER BY SEARCH DESC LIMIT 3 "
        cursor.execute(sqlQuery[14])
        fetchResultQuery[14] = cursor.fetchall()

        sqlQuery[15] = "SELECT * FROM testdatabase.Hotspot WHERE Address LIKE '광주%' ORDER BY SEARCH DESC LIMIT 3 "
        cursor.execute(sqlQuery[15])
        fetchResultQuery[15] = cursor.fetchall()

        sqlQuery[16] = "SELECT * FROM testdatabase.Hotspot WHERE Address LIKE '제주%' ORDER BY SEARCH DESC LIMIT 3 "
        cursor.execute(sqlQuery[16])
        fetchResultQuery[16] = cursor.fetchall()


        connection.commit()
        connection.close()
        j = 0
        for i in range(0,51,3):
            for row in fetchResultQuery[i//3]:
                hotspot_list[j] = ({'Name' : row[0], 'Address' : row[1], 'Category' : row[2], 'Search' : row[3]})
                j = j + 1

        festivals = Festival.objects.all().values().order_by('festival_id')

        festival_pg = Paginator(festivals, 3)
        page = int(request.GET.get('page', 1))
        festival_list = festival_pg.get_page(page)

        trends = Trend.objects.all().values().order_by('-search_value')

        trends_pg = Paginator(trends,3)
        page = int(request.GET.get('page', 1))
        trends_list = trends_pg.get_page(page)

    return render(request, 'myApp/index.html', {'hotspot': hotspot_list, 'festival_list': festival_list,
                                                'trends_list': trends_list})


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
