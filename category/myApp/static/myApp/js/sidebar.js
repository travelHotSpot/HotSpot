const facilityIcons = {
        "WIFI": '<span class=fa-stack fa-2x"><i class="fa-solid fa-wifi fa-stack-2x"></i></span>',
        "WIFI없음": '<span class=fa-stack fa-2x"><i class="fa-solid fa-ban fa-stack-2x"></i><i class="fa-solid fa-wifi fa-stack-1x"></i></span>',
        "동물출입": '<span class=fa-stack fa-2x"><i class="fa-solid fa-dog fa-stack-2x"></i></span>',
        "동물출입금지": '<span class=fa-stack fa-2x"><i class="fa-solid fa-ban fa-stack-2x"></i><i class="fa-solid fa-dog fa-stack-1x"></i></span>',
        "주차": '<span class=fa-stack fa-2x"><i class="fa-solid fa-square-parking fa-stack-2x"></i></span>',
        "주차시설없음": '<span class=fa-stack fa-2x"><i class="fa-solid fa-ban fa-stack-2x"></i><i class="fa-solid fa-square-parking fa-stack-1x"></i></span>',
        "장애시설": '<span class=fa-stack fa-2x"><i class="fa-brands fa-accessible-icon fa-stack-2x"></i></span>',
        "장애시설없음": '<span class=fa-stack fa-2x"><i class="fa-solid fa-ban fa-stack-2x"></i><i class="fa-brands fa-accessible-icon fa-stack-1x"></i></span>',
        "놀이방": '<span class=fa-stack fa-2x"><i class="fa-brands fa-fort-awesome fa-stack-2x"></i></span>',
        "놀이방시설없음": '<span class=fa-stack fa-2x"><i class="fa-solid fa-ban fa-stack-2x"></i><i class="fa-brands fa-fort-awesome fa-stack-1x"></i></span>',
        "흡연실": '<span class=fa-stack fa-2x"><i class="fa-solid fa-smoking fa-2x"></i></span>',
        "흡연실시설없음": '<span class=fa-stack fa-2x"><i class="fa-solid fa-ban-smoking fa-2x"></i></span>'
        };
Object.freeze(facilityIcons);

function loadPlace(page, sort=null, keyword=null){
    var query;
    var sorting;
    if(keyword != null){
        if(keyword != $('#search-input').val()){
            query = $('#search-input').val();
        }else{
            query = keyword;
        }
    }else{
        query = $('#search-input').val();
    }

    if(sort == null){
        var selectBox = document.getElementById('sort');
        sorting = selectBox.options[selectBox.selectedIndex].value;
    }else{
        sorting = sort;
    }

    $('.offcanvas-body').remove();
    $('#offcanvas').append('<div class="offcanvas-body px-0 justify-content-center"><div class="d-flex justify-content-center" style="height: 100%;"><div class="spinner-border align-self-center" role="status"><span class="visually-hidden">Loading...</span></div></div></div>');

    $.ajax({
        type: "GET",
        url: "/busan/getPlaceList/",
        data: {
            sort: sorting,
            q: query,
            page: page
        },
        success: function(data){
            $('.offcanvas-body').remove();
            $('#offcanvas').append(data);
            showMarker();
        },
    });
}

$('#detailModal').on('show.bs.modal', function(e) {
    setTimeout(function(e){
        // offcanvas(sidebar)'s toggle button animation
        const toggle_button = document.querySelector('.offcanvas-btn');
        toggle_button.animate(
            {
                transform: [ 'translate(350px, 0)' ]
            },
            {
                duration: 150,
                fill: 'forwards',
                easing: 'ease'
            }
        );
    }, 200);

    // fill data in modal
    var btn = $(e.relatedTarget);
    var title = btn.data('title');
    var category = btn.data('category');
    var address = btn.data('address');
    var operation_time = btn.data('op');
    var tel = btn.data('tel');
    var homepage = btn.data('homepage');
    var tag = btn.data('tag');
    var etc = btn.data('etc');
    var facility = btn.data('facility');
    var url = btn.data('kakaomap');

    var modal = $(this);
    modal.find('#detailModalLabel').text(title);
    modal.find('#detailModalCategory').text(category);
    modal.find('.addr').text(address);

    operation_time = eval(operation_time);
    modal.find('.opt').empty();
    operation_time.forEach(t => {
        if(t == "영업시간" || t == "휴무일"){
            modal.find('.opt').append('<small><strong>' + t + '</strong></small><br>');
        }else{
            modal.find('.opt').append('<small>' + t + '</small><br>');
        }
    });

    if(String(tel) != ""){
        modal.find('.tel').empty();
        modal.find('.tel').text(tel);
    }

    if(String(homepage) != ""){
        modal.find('.homepage').empty();
        modal.find('.homepage').append('<a href="' + homepage + '">' + homepage + '</a>');
    }

    if (eval(tag).length != 0){
        modal.find('.tag').empty();
        tag = eval(tag);
        tag.forEach(t => {
            modal.find('.tag').append('<small>' + t + '</small>');
        });
    }

    if (String(etc) != ""){
        modal.find('.etc').empty();
        modal.find('.etc').text(etc);
    }

    facility = eval(facility);
    modal.find('.facility').empty();
    facility.forEach(t => {
        t = t.replace(/ /g, '');
        modal.find('.facility').append(facilityIcons[t]);
    });
    modal.find('.kakaomap-url').attr('href', url);
});

$('#detailModal').on('hide.bs.modal', function(e) {
    const btn = document.querySelector('.offcanvas-btn');
    btn.animate(
        {
            transform: [ 'translate(0px, 0)' ]
        },
        {
            duration: 150,
            fill: 'forwards',
            easing: 'ease'
        }
    );
});

$('#offcanvas').on('hide.bs.offcanvas', function(e) {
    $('#detailModal').modal('hide');
});

$('#offcanvas').on('shown.bs.offcanvas', function(e) {
    $('.btn-arrow').removeClass('bi-arrow-right-square-fill');
    $('.btn-arrow').addClass('bi-arrow-left-square-fill');
});

$('#offcanvas').on('hidden.bs.offcanvas', function(e) {
    $('.btn-arrow').removeClass('bi-arrow-left-square-fill');
    $('.btn-arrow').addClass('bi-arrow-right-square-fill');
});

// sort
$('#sort').on('change', function s(e){
    loadPlace(1, e.target.value, keyword);
});