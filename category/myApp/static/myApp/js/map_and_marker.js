var sidebarMarkerList = [];
var hopeListmarkers = [];
var startingMarker;
var endingMarker;
var nameList = [];
var polyline;

var callbackCounter = 0;
var infowindow = new kakao.maps.InfoWindow({zIndex:1});

// offcanvas에 있는 10개 위치의 마커를 표시
function showMarker(){
    callbackCounter = 0;
    for(var i = 0; i < sidebarMarkerList.length; i++){
        sidebarMarkerList[i].setMap(null);
    }
    sidebarMarkerList = [];
    nameList = [];

    var geocoder = new kakao.maps.services.Geocoder();
    var nameNode = document.querySelectorAll('.ms-2 .d-flex .mb-1');
    for(var i = 0; i < nameNode.length; i++){
        nameList.push(nameNode[i].innerText);
    }

    var pList = document.getElementsByClassName('address');
    var addrList = [];
    for(var i = 0; i < pList.length; i++){
        var addr = pList[i].innerText;
        if (addr.search(/\((우\))/gi) != -1){
            addr = addr.slice(0, addr.search(/\((우\))/gi) - 1);
        }
        if (addr.search(/층/) != -1){
            addr = addr.slice(0, addr.lastIndexOf(' '));
        }
        addrList.push(addr);
    }
    addrList.forEach((addr, idx) => {
        geocoder.addressSearch(addr, function(result, status){
            if(status === kakao.maps.services.Status.OK){
                var coords = new kakao.maps.LatLng(result[0].y, result[0].x);
                var innerCounter = callbackCounter;

                var imageSrc = 'https://t1.daumcdn.net/localimg/localimages/07/mapapidoc/marker_number_blue.png',
                    imageSize = new kakao.maps.Size(36, 37),
                    imgOptions =  {
                        spriteSize : new kakao.maps.Size(36, 691),
                        spriteOrigin : new kakao.maps.Point(0, (idx*46)+10),
                        offset: new kakao.maps.Point(13, 37)
                    },
                    markerImage = new kakao.maps.MarkerImage(imageSrc, imageSize, imgOptions),
                        marker = new kakao.maps.Marker({
                        position: coords,
                        image: markerImage
                    });

                var title = nameList[idx];
                kakao.maps.event.addListener(marker, 'mouseover', function() {
                    displayInfowindow(marker, title);
                });

                kakao.maps.event.addListener(marker, 'mouseout', function() {
                    infowindow.close();
                });

                kakao.maps.event.addListener(marker, 'click', function(){
                    var position = (this).getPosition();
                    map.setLevel(7, {anchor: new kakao.maps.LatLng(position.Ma, position.La)});
                });

                sidebarMarkerList[idx] = marker;
                marker.setMap(map);
            }
        });
    });


}

function displayInfowindow(marker, title) {
    var content = '<div style="padding:5px;z-index:1;">' + title + '</div>';

    infowindow.setContent(content);
    infowindow.open(map, marker);
}

function addHopeList(name, addr, tel){
    var startPoint = document.querySelector('#starting-point .info h5').innerText;
    var endPoint = document.querySelector('#ending-point .info h5').innerText;
    var itemList = document.querySelectorAll('#placesList .item');
    var listLen = itemList.length;
    if(listLen == 5){
        alert('출발지, 도착지를 제외하고 5개를 넘길 수 없습니다.');
        return;
    }

    if(name == startPoint || name == endPoint){
        alert('출발지, 도착지로 지정된 곳입니다.');
        return;
    }

    for(var i = 0; i < itemList.length; i++){
        var item = itemList[i];
        var itemName = item.querySelector('.info span h5').innerText;

        if(name == itemName){
            alert('이미 추가된 항목은 넣을 수 없습니다.');
            return;
        }
    }

    if (addr.search(/\((우\))/gi) != -1){
        addr = addr.slice(0, addr.search(/\((우\))/gi) - 1);
    }
    if (addr.search(/층/) != -1){
        addr = addr.slice(0, addr.lastIndexOf(' '));
    }

    var geocoder = new kakao.maps.services.Geocoder();
    geocoder.addressSearch(addr, function(result, status){
        if(status === kakao.maps.services.Status.OK){
            var coords = new kakao.maps.LatLng(result[0].y, result[0].x),
                place = {"name": name, "addr": addr, "tel": tel, "coords": coords};
            var listEl = document.getElementById('placesList'),
                menuEl = document.getElementById('menu_wrap'),
                fragment = document.createDocumentFragment(),
                bounds = new kakao.maps.LatLngBounds(),
                listStr = '';

            var placePosition = new kakao.maps.LatLng(place.coords.Ma, place.coords.La),
                marker = addMarker(placePosition, listLen),
                itemEl = getListItem(listLen, place);
                fragment.appendChild(itemEl);
                listEl.appendChild(fragment);
                menuEl.scrollTop = 0;
        }
    });
}

function getListItem(index, place) {
    var el = document.createElement('li'),
        itemStr = '<span class="markerbg marker_' + (index+1) + '"></span>' +
                    '<div class="info">' +
                    '   <span>' +
                    '   <h5>' + place.name + '</h5>' +
                    '   <button class="btn btn-primary" onclick="setStart(' + (index + 1) + ', \'' + place.name + '\',\'' + place.addr + '\',\'' + place.tel + '\');">출발</button>' +
                    '   <button class="btn btn-primary" onclick="setEnd(' + (index + 1) + ', \'' + place.name + '\',\'' + place.addr + '\',\'' + place.tel + '\');">도착</button>' +
                    '   <i class="bi bi-arrow-up" onclick="moveItem(' + (index + 1) + ', \'up\')"></i>' +
                    '   <i class="bi bi-arrow-down" onclick="moveItem(' + (index + 1) + ', \'down\')"></i>' +
                    '   <i class="bi bi-x" onclick="deList(' + (index + 1) + ')"></i>' +
                    '   </span>';

    if (place.addr) {
        itemStr += '    <span class="addr">' + place.addr + '</span>';
    }

    itemStr += '  <span class="tel">' + place.tel  + '</span>' +
                '</div>';

    el.innerHTML = itemStr;
    el.className = 'item';

    return el;
}

function addMarker(position, idx, title) {
    var imageSrc = RED_MARKER_SRC,
        imageSize = new kakao.maps.Size(36, 37),
        imgOptions =  {
            spriteSize : new kakao.maps.Size(39, 733),
            spriteOrigin : new kakao.maps.Point(0, (idx*50)+2),
            offset: new kakao.maps.Point(13, 37)
        },
        markerImage = new kakao.maps.MarkerImage(imageSrc, imageSize, imgOptions),
        marker = new kakao.maps.Marker({
            position: position,
            image: markerImage
        });

    for(var i = 0; i < sidebarMarkerList.length; i++){
        if(sidebarMarkerList[i].getPosition().getLat() == marker.getPosition().getLat() &&
            sidebarMarkerList[i].getPosition().getLng() == marker.getPosition().getLng()){
            sidebarMarkerList[i].setMap(null);
            break;
        }
    }

    marker.setMap(map);
    hopeListmarkers.push(marker);
    return marker;
}

function setStart(idx, name, addr, tel){
    var divBox = document.getElementById('starting-point');
    var infoBox = divBox.getElementsByClassName('info');
    var ul = document.getElementById('placesList');
    var lis = ul.getElementsByTagName('li');
    lis[idx - 1].remove();

    infoBox[0].getElementsByTagName('h5')[0].innerText = name;
    infoBox[0].getElementsByClassName('addr')[0].innerText = addr;
    infoBox[0].getElementsByClassName('tel')[0].innerText = tel;

    // 출발지 존재 시 마커 삭제
    if(startingMarker != null){
        startingMarker.setMap(null);
    }

    var orig_marker = hopeListmarkers[idx - 1];
    startingMarker = hopeListmarkers[idx - 1];

    var imageSrc = STARTING_POINT_MARKER_SRC,
        imageSize = new kakao.maps.Size(24, 35),
        markerImage = new kakao.maps.MarkerImage(imageSrc, imageSize);

    startingMarker.setImage(markerImage);
    orig_marker.setMap(null);
    hopeListmarkers.splice(idx - 1, 1);
    startingMarker.setMap(map);
    refreshHopeList();
}

function setEnd(idx, name, addr, tel){
    var divBox = document.getElementById('ending-point');
    var infoBox = divBox.getElementsByClassName('info');
    var ul = document.getElementById('placesList');
    var lis = ul.getElementsByTagName('li');
    lis[idx - 1].remove();

    infoBox[0].getElementsByTagName('h5')[0].innerText = name;
    infoBox[0].getElementsByClassName('addr')[0].innerText = addr;
    infoBox[0].getElementsByClassName('tel')[0].innerText = tel;

    // 도착지 존재 시 마커 삭제
    if(endingMarker != null){
        endingMarker.setMap(null);
    }

    var orig_marker = hopeListmarkers[idx - 1];
    endingMarker = hopeListmarkers[idx - 1];

    var imageSrc = ENDING_POINT_MARKER_SRC,
        imageSize = new kakao.maps.Size(24, 35),
        markerImage = new kakao.maps.MarkerImage(imageSrc, imageSize);

    endingMarker.setImage(markerImage);
    orig_marker.setMap(null);
    hopeListmarkers.splice(idx - 1, 1);
    endingMarker.setMap(map);
    refreshHopeList();
}

function refreshHopeList(){
    var ul = document.getElementById('placesList');
    var lis = ul.getElementsByTagName('li');
    for(var i = 0; i < lis.length; i++){
        var li = lis[i];
        var marker = li.getElementsByClassName('markerbg');
        marker[0].className = "markerbg marker_" + (i + 1);

        var name = li.getElementsByTagName('h5')[0].innerText,
            addr = li.getElementsByClassName('addr')[0].innerText,
            tel = li.getElementsByClassName('tel')[0].innerText,
            deListBtn = li.getElementsByClassName('bi-x')[0],
            upArrow = li.getElementsByClassName('bi-arrow-up')[0],
            downArrow = li.getElementsByClassName('bi-arrow-down')[0],
            btns = li.getElementsByTagName('button');
        deListBtn.setAttribute("onClick", "deList(" + (i + 1) + ")");
        upArrow.setAttribute("onClick", "moveItem(" + (i + 1) + ", 'up')");
        downArrow.setAttribute("onClick", "moveItem(" + (i + 1) + ", 'down')");
        btns[0].setAttribute("onClick", "setStart(" + (i + 1) + ",\'" + name + "\', \'" + addr + "\', \'" + tel + "\')");
        btns[1].setAttribute("onClick", "setEnd(" + (i + 1) + ",\'" + name + "\', \'" + addr + "\', \'" + tel + "\')");

        // 마커 번호 변경
        var imageSrc = RED_MARKER_SRC,
        imageSize = new kakao.maps.Size(36, 37),
        imgOptions =  {
            spriteSize : new kakao.maps.Size(39, 733),
            spriteOrigin : new kakao.maps.Point(0, (i*50)+2),
            offset: new kakao.maps.Point(13, 37)
        },
        markerImage = new kakao.maps.MarkerImage(imageSrc, imageSize, imgOptions);

        var markerImage = new kakao.maps.MarkerImage(imageSrc, imageSize, imgOptions);
        hopeListmarkers[i].setImage(markerImage);
    }
}

function deList(idx){
    hopeListmarkers[idx - 1].setMap(null);

    for(var i = 0; i < sidebarMarkerList.length; i++){
        if(sidebarMarkerList[i].getPosition().getLat() == hopeListmarkers[idx - 1].getPosition().getLat() &&
            sidebarMarkerList[i].getPosition().getLng() == hopeListmarkers[idx - 1].getPosition().getLng()){
            sidebarMarkerList[i].setMap(map);
            break;
        }
    }

    hopeListmarkers.splice(idx - 1, 1);
    var ul = document.getElementById('placesList');
    var lis = ul.getElementsByTagName('li');
    lis[idx - 1].remove();
    refreshHopeList();
}

function deleteEndPointMarker(se){
    if(se == "start"){
        if(startingMarker == null){
            alert('출발지가 없습니다.');
            return;
        }
        startingMarker.setMap(null);
        startingMarker = null;
        var divBox = document.getElementById('starting-point'),
            infoBox = divBox.getElementsByClassName('info');

        infoBox[0].getElementsByTagName('h5')[0].innerText = '';
        infoBox[0].getElementsByClassName('addr')[0].innerText = '';
        infoBox[0].getElementsByClassName('tel')[0].innerText = '';
    }else{
        if(endingMarker == null){
                alert('도착지가 없습니다.');
                return;
            }
            endingMarker.setMap(null);
            endingMarker = null;
            var divBox = document.getElementById('ending-point'),
                infoBox = divBox.getElementsByClassName('info');

            infoBox[0].getElementsByTagName('h5')[0].innerText = '';
            infoBox[0].getElementsByClassName('addr')[0].innerText = '';
            infoBox[0].getElementsByClassName('tel')[0].innerText = '';
    }
}

function moveItem(idx, direction){
    var ul = document.getElementById('placesList');
    var lis = ul.getElementsByTagName('li');
    if((idx == 1 && direction == "up") || (idx == lis.length && direction == "down")){
        alert('옮길 수 없습니다.');
        return;
    }
    if(direction == "up"){
        [hopeListmarkers[idx - 1], hopeListmarkers[idx - 2]] = [hopeListmarkers[idx - 2], hopeListmarkers[idx - 1]];
        var $li = $("#placesList li:nth-child(" + idx + ")");
        $li.prev().before($li);
        refreshHopeList();
    }
    if(direction == "down"){
        [hopeListmarkers[idx - 1], hopeListmarkers[idx]] = [hopeListmarkers[idx], hopeListmarkers[idx - 1]];
        var $li = $("#placesList li:nth-child(" + idx + ")");
        $li.next().after($li);
        refreshHopeList();
    }
}

function findRoute(){
    if(polyline != null){
        polyline.setMap(null);
        polyline = null;
    }

    if(startingMarker == null){
        alert('출발지를 지정해주세요');
        return;
    }

    if(endingMarker == null){
        alert('도착지를 지정해주세요');
        return;
    }

    var origin = {"name": document.querySelector('#starting-point .info h5').innerText,
                  "x": startingMarker.getPosition().getLng(), "y": startingMarker.getPosition().getLat()
                  };
    var destination = {"name": document.querySelector('#ending-point .info h5').innerText,
                        "x": endingMarker.getPosition().getLng(), "y": endingMarker.getPosition().getLat(),
                       };
    var waypoints = [];
    var ul = document.getElementById('placesList');
    var lis = ul.getElementsByTagName('li');
    for(var i = 0; i < lis.length; i++){
        var waypoint = {"name": lis[i].querySelector('.info span h5').innerText,
                        "x": hopeListmarkers[i].getPosition().getLng(), "y": hopeListmarkers[i].getPosition().getLat(),
                        };
        waypoints.push(waypoint);
    }

    $.ajax({
        type: "GET",
        url: "/api/getRoute/",
        data: {
            origin: JSON.stringify(origin),
            destination: JSON.stringify(destination),
            waypoints: JSON.stringify(waypoints)
        },
        success: function(data){
            var jsonObj = JSON.parse(data);
            var linePath = [];

            for(var i = 0; i < jsonObj["positions"].length;){
                linePath.push(new kakao.maps.LatLng(jsonObj["positions"][i + 1], jsonObj["positions"][i]));
                i += 2;
            }
            polyline = new kakao.maps.Polyline({
                path: linePath,
                strokeWeight: 5,
                strokeColor: '#e834eb',
                strokeOpacity: 1,
                strokeStyle: 'solid',
            });

            polyline.setMap(map);
        },
    });
}