import requests
import json
import os
from pathlib import Path
from django.http import HttpResponse, JsonResponse
from datetime import datetime
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
from .models import MainSpot
from .forms import CommentForm

# 카카오 API를 사용하는데 필요한 key를 keys.json에서 찾아 kakao_key에 보관
BASE_DIR = Path(__file__).resolve().parent.parent
key_file = os.path.join(BASE_DIR, 'keys.json')
with open(key_file) as in_file:
    keys = json.loads(in_file.read())
    kakao_key = keys["KAKAO_API"]

# Create your views here.
def showTable(request):
    sqlQuery = [0] * 17
    fetchResultQuery = [0] * 17
    hotspot_list = [0] * 51

    with connection.cursor() as cursor:

        sqlQuery[0] = "SELECT * FROM testdatabase.place JOIN testdatabase.top_place WHERE testdatabase.place.name = testdatabase.top_place.place AND address LIKE '부산 해운대구%' ORDER BY SCORE DESC LIMIT 3 "
        cursor.execute(sqlQuery[0])
        fetchResultQuery[0] = cursor.fetchall()

        sqlQuery[1] = "SELECT * FROM testdatabase.place JOIN testdatabase.top_place WHERE testdatabase.place.name = testdatabase.top_place.place AND address LIKE '부산 동래구%' ORDER BY SCORE DESC LIMIT 3 "
        cursor.execute(sqlQuery[1])
        fetchResultQuery[1] = cursor.fetchall()

        sqlQuery[2] = "SELECT * FROM testdatabase.place JOIN testdatabase.top_place WHERE testdatabase.place.name = testdatabase.top_place.place AND address LIKE '부산 연제구%' ORDER BY SCORE DESC LIMIT 3 "
        cursor.execute(sqlQuery[2])
        fetchResultQuery[2] = cursor.fetchall()

        sqlQuery[3] = "SELECT * FROM testdatabase.place JOIN testdatabase.top_place WHERE testdatabase.place.name = testdatabase.top_place.place AND address LIKE '부산 강서구%' ORDER BY SCORE DESC LIMIT 3 "
        cursor.execute(sqlQuery[3])
        fetchResultQuery[3] = cursor.fetchall()

        sqlQuery[4] = "SELECT * FROM testdatabase.place JOIN testdatabase.top_place WHERE testdatabase.place.name = testdatabase.top_place.place AND address LIKE '부산 사상구%' ORDER BY SCORE DESC LIMIT 3 "
        cursor.execute(sqlQuery[4])
        fetchResultQuery[4] = cursor.fetchall()

        sqlQuery[5] = "SELECT * FROM testdatabase.place JOIN testdatabase.top_place WHERE testdatabase.place.name = testdatabase.top_place.place AND address LIKE '부산 부산진구%' ORDER BY SCORE DESC LIMIT 3 "
        cursor.execute(sqlQuery[5])
        fetchResultQuery[5] = cursor.fetchall()

        sqlQuery[6] = "SELECT * FROM testdatabase.place JOIN testdatabase.top_place WHERE testdatabase.place.name = testdatabase.top_place.place AND address LIKE '부산 수영구%' ORDER BY SCORE DESC LIMIT 3 "
        cursor.execute(sqlQuery[6])
        fetchResultQuery[6] = cursor.fetchall()

        sqlQuery[7] = "SELECT * FROM testdatabase.place JOIN testdatabase.top_place WHERE testdatabase.place.name = testdatabase.top_place.place AND address LIKE '부산 기장군%' ORDER BY SCORE DESC LIMIT 3 "
        cursor.execute(sqlQuery[7])
        fetchResultQuery[7] = cursor.fetchall()

        sqlQuery[8] = "SELECT * FROM testdatabase.place JOIN testdatabase.top_place WHERE testdatabase.place.name = testdatabase.top_place.place AND address LIKE '부산 남구%' ORDER BY SCORE DESC LIMIT 3 "
        cursor.execute(sqlQuery[8])
        fetchResultQuery[8] = cursor.fetchall()

        sqlQuery[9] = "SELECT * FROM testdatabase.place JOIN testdatabase.top_place WHERE testdatabase.place.name = testdatabase.top_place.place AND address LIKE '부산 동구%' ORDER BY SCORE DESC LIMIT 3 "
        cursor.execute(sqlQuery[9])
        fetchResultQuery[9] = cursor.fetchall()

        sqlQuery[10] = "SELECT * FROM testdatabase.place JOIN testdatabase.top_place WHERE testdatabase.place.name = testdatabase.top_place.place AND address LIKE '부산 사하구%' ORDER BY SCORE DESC LIMIT 3 "
        cursor.execute(sqlQuery[10])
        fetchResultQuery[10] = cursor.fetchall()

        sqlQuery[11] = "SELECT * FROM testdatabase.place JOIN testdatabase.top_place WHERE testdatabase.place.name = testdatabase.top_place.place AND address LIKE '부산 서구%' ORDER BY SCORE DESC LIMIT 3 "
        cursor.execute(sqlQuery[11])
        fetchResultQuery[11] = cursor.fetchall()

        sqlQuery[12] = "SELECT * FROM testdatabase.place JOIN testdatabase.top_place WHERE testdatabase.place.name = testdatabase.top_place.place AND address LIKE '부산 중구%' ORDER BY SCORE DESC LIMIT 3 "
        cursor.execute(sqlQuery[12])
        fetchResultQuery[12] = cursor.fetchall()

        sqlQuery[13] = "SELECT * FROM testdatabase.place JOIN testdatabase.top_place WHERE testdatabase.place.name = testdatabase.top_place.place AND address LIKE '부산 영도구%' ORDER BY SCORE DESC LIMIT 3 "
        cursor.execute(sqlQuery[13])
        fetchResultQuery[13] = cursor.fetchall()

        sqlQuery[14] = "SELECT * FROM testdatabase.place JOIN testdatabase.top_place WHERE testdatabase.place.name = testdatabase.top_place.place AND address LIKE '부산 북구%' ORDER BY SCORE DESC LIMIT 3 "
        cursor.execute(sqlQuery[14])
        fetchResultQuery[14] = cursor.fetchall()

        sqlQuery[15] = "SELECT * FROM testdatabase.place JOIN testdatabase.top_place WHERE testdatabase.place.name = testdatabase.top_place.place AND address LIKE '부산 금정구%' ORDER BY SCORE DESC LIMIT 3 "
        cursor.execute(sqlQuery[15])
        fetchResultQuery[15] = cursor.fetchall()

        connection.commit()
        connection.close()
        j = 0
        for i in range(0, 48, 3):
            for row in fetchResultQuery[i // 3]:
                hotspot_list[j] = ({'Name': row[1]})
                j = j + 1

        spots = MainSpot.objects.all().values().order_by('-weighted_rate')

        spot_pg = Paginator(spots, per_page=8)
        page = int(request.GET.get('page', 1))
        spot_list = spot_pg.get_page(page)

        for s in spot_list:
            s["category"] = ','.join(eval(s["category"]))
            s["operation_time"] = eval(s["operation_time"])
            s["tag"] = eval(s["tag"])
            s["facility"] = eval(s["facility"])

        festivals = Festival.objects.filter(end_date__gt=datetime.now()).order_by('start_date')

        festival_pg = Paginator(festivals, 3)
        page = int(request.GET.get('page', 1))
        festival_list = festival_pg.get_page(page)

    return render(request, 'myApp/index.html', {'hotspot': hotspot_list, 'festival_list': festival_list, 'spot_list': spot_list})


def show_festival(request):
    '''
    축제 목록을 보여주는 페이지
    @param request: pagination을 위한 page
    @return: 해당 page에 해당하는 축제 목록
    '''
    festivals = Festival.objects.filter(end_date__gt=datetime.now()).order_by('start_date')

    festival_pg = Paginator(festivals, 6)
    page = int(request.GET.get('page', 1))
    festival_list = festival_pg.get_page(page)

    return render(request, 'myApp/festival.html', {'festival_list': festival_list})


def festival_detail(request, festival_id):
    '''
    축제 상세설명을 보여주는 페이지
    @param request:
    @param festival_id: 상세설명을 볼 축제의 고유번호
    @return: 축제 정보, 사진, 댓글 폼, 댓글
    '''
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
    '''
    댓글 작성
    @param request:
    @param festival_id: 댓글을 등록할 축제 고유번호
    @return: 댓글 등록이 성공하면 해당 축제 상세페이지로 redirect
    '''
    festival_article = get_object_or_404(Festival, festival_id=festival_id)
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
    '''
    댓글 삭제
    @param request:
    @param festival_id: 삭제할 댓글이 있는 축제 고유번호
    @param comment_id: 댓글 번호
    @return: 축제 상세페이지로 redirect
    '''
    festival = get_object_or_404(Festival, festival_id=festival_id)
    comment = get_object_or_404(CommentFestival, comment_id=comment_id, festival_id=festival_id)
    if request.POST['password'] == comment.passwd:
        comment.delete()
    return redirect('festival_detail', festival_id=festival.festival_id)


def busan(request):
    '''
    지도와 검색창을 갖춘 페이지
    @param request: pagination을 위한 page, 메인페이지에서 특정 구를 선택해 넘어오는 경우를 표시하는 gu
    @return:
    '''
    gu = request.GET.get("gu")
    return render(request, 'myApp/busan.html', {'gu': gu})


def get_place_list(request):
    '''
    검색창을 결과를 보여주는 페이지
    @param request: pagination을 위한 page, 정렬 방식을 담은 sort, 검색어를 담은 q
    @return: 검색 결과와 정렬 방식, 검색어를 다시 돌려줌
    '''
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
        spots = spots.order_by('-weighted_rate')

    spot_pg = Paginator(spots, per_page=10)
    page = int(request.GET.get('page', 1))
    spot_list = spot_pg.get_page(page)

    for s in spot_list:
        s["category"] = ','.join(eval(s["category"]))
        s["operation_time"] = eval(s["operation_time"])
        s["tag"] = eval(s["tag"])
        s["facility"] = eval(s["facility"])

    return render(request, 'myApp/busan_offcanvas_body.html',
                  {'spot_list': spot_list, 'sort': sort_param, 'keyword': query_param})


def get_route(request):
    '''
    요청한 경로에 대한 카카오 모빌리티의 길찾기 api 결과를 돌려줌
    @param request: 출발지 origin, 경유지 waypoints, 도착지 destination
    @return: api 응답 결과와 경로 좌표를 json으로 return
    '''
    origin = request.GET.get("origin")
    destination = request.GET.get("destination")
    waypoints = request.GET.get("waypoints")

    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'KakaoAK ' + kakao_key,
    }
    json_data = {
        'priority': 'RECOMMEND',
        'car_type': 1,
        'origin': json.loads(origin),
        'destination': json.loads(destination),
        'waypoints': json.loads(waypoints),
    }

    response = requests.post('https://apis-navi.kakaomobility.com/v1/waypoints/directions', headers=headers,
                             json=json_data)
    response = response.json()

    if response["routes"][0]["result_code"] == 0:
        positions = []
        for section in response["routes"][0]["sections"]:
            for road in section["roads"]:
                for position in road["vertexes"]:
                    positions.append(position)

        edited_response = {
            "summary": response['routes'][0]['summary'],
            "positions": positions
        }
        return JsonResponse(json.dumps(edited_response, ensure_ascii=False), safe=False)
    else:
        return JsonResponse(response, safe=False)


def dashboard(request):
    spots = Place.objects.all().values().order_by('-weighted_rate')

    spot_pg = Paginator(spots, per_page=100)
    page = int(request.GET.get('page', 1))
    spot_list = spot_pg.get_page(page)

    for s in spot_list:
        s["category"] = ','.join(eval(s["category"]))
        s["operation_time"] = eval(s["operation_time"])
        s["tag"] = eval(s["tag"])
        s["facility"] = eval(s["facility"])

    return render(request, 'myApp/dashboard.html', {'spot_list': spot_list})
