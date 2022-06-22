from django.shortcuts import render,redirect
from django.db import connection
import csv

def Home(request):
    hotspot_list = []
    with connection.cursor() as cursor:
        #query문 생성 및 실행
        sqlQuery = "SELECT * FROM testdatabase.Hotspot"
        cursor.execute(sqlQuery)
        fetchResultQuery = cursor.fetchall()

        connection.commit()
        connection.close()
        #각 row마다 값을 hotspot_list에 저장
        for temp in fetchResultQuery:
            eachRow = {'Name': temp[0], 'Address': temp[1], 'Category': temp[2], 'Search': temp[3]}
            hotspot_list.append(eachRow)
    return render(request,'myApp/main.html',{"hotspot": hotspot_list})

def insertHotspot(request):
    with connection.cursor() as cursor:
        #csv파일 읽어오기
        hotspot = open(r'myApp/templates/myApp/20220623012515_인기관광지_전체.csv')
        reader = csv.reader(hotspot)
        i = 0
        for row in reader:
            if i>0:
                #table에 csv 내용 삽입
                sqlInsertQuery = "INSERT IGNORE INTO testdatabase.Hotspot(Name,Address,Category,Search) VALUES ('"+row[1]+"',\
                '"+row[2]+"','"+row[3]+"','"+row[4]+"')"
                cursor.execute(sqlInsertQuery)
            i+=1
        connection.commit()
        connection.close()
    return redirect("home")