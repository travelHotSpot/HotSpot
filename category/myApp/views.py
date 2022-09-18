from django.shortcuts import render, redirect, get_object_or_404
from django.db import connection
from django.core.paginator import Paginator
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.http import require_POST
from django.db.models import Q
from .models import Festival
from .models import FestivalInfo
from .models import FestivalImg
from .models import Trend
from .models import CommentFestival
from .models import Place
from .forms import CommentForm


# Create your views here.
def showTable(request):
    sqlQuery = [0] * 17
    fetchResultQuery = [0] * 17
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

        trends = Trend.objects.all().values().order_by('search_sum')

        trends_pg = Paginator(trends, 3)
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
    try:
        comments = CommentFestival.objects.filter(festival_id=festival_id)
    except CommentFestival.DoesNotExist:
        comments = []

    comment_form = CommentForm()
    return render(request, 'myApp/festival_detail.html', {'festival': festival, 'festival_info': festival_info,
                                                          'festival_img': festival_img, 'comments': comments,
                                                          'comment_form': comment_form})


@require_POST
def create_comment_festival(request, festival_id):
    festival_article = get_object_or_404(Festival, festival_id=festival_id)
    # if request.method == 'POST':
    comment_form = CommentForm(request.POST)
    if comment_form.is_valid():
        # comment_form.save()
        comment = comment_form.save(commit=False)
        comment.festival_id = festival_id
        # comment.username = request.session['username']
        # comment.comment_pw = request.session['password']
        comment.save()
        return redirect('festival_detail', festival_id=festival_article.festival_id)
    else:
        comment_form = CommentForm()
    return render(request, 'myApp/festival_detail.html', {'form': comment_form})


@require_POST
def delete_comment_festival(request, festival_id, comment_id):
    festival = get_object_or_404(Festival, festival_id=festival_id)
    comment = get_object_or_404(CommentFestival, comment_id=comment_id, festival_id=festival_id)
    if request.POST['password'] == comment.passwd:
        comment.delete()
    return redirect('festival_detail', festival_id=festival.festival_id)


def busan(request):
    gu = request.GET.get("gu")
    return render(request, 'myApp/busan.html', {'gu': gu})


def get_place_list(request):
    sort_param = request.GET.get("sort")
    query_param = request.GET.get("q", None)

    if query_param:
        spots = Place.objects.filter(Q(name__contains=query_param) | Q(category__contains=query_param) |
                                     Q(address__contains=query_param) | Q(tag__contains=query_param)) \
            .distinct().values()
    else:
        spots = Place.objects.all().values()

    if sort_param:
        if sort_param == "name":
            spots = spots.order_by('name')
        elif sort_param == "rating":
            spots = spots.order_by('-weighted_rate')
        else:
            spots = spots.order_by('place_id')
    else:
        spots = spots.order_by('place_id')

    for s in spots:
        s["category"] = ','.join(eval(s["category"]))
        s["operation_time"] = eval(s["operation_time"])
        s["tag"] = eval(s["tag"])
        s["facility"] = eval(s["facility"])

    spot_pg = Paginator(spots, per_page=10)
    page = int(request.GET.get('page', 1))
    spot_list = spot_pg.get_page(page)

    return render(request, 'myApp/busan_offcanvas_body.html',
                  {'spot_list': spot_list, 'sort': sort_param, 'keyword': query_param})
