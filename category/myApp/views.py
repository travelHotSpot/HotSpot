from django.shortcuts import render
from django.db import connection

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
            hotspot_list.append({'Name' : row[0], 'Address' : row[1], 'Category' : row[2], 'Search' : row[3]})

    return render(request, 'myApp\index.html', {"hotspot" : hotspot_list})