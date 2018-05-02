$(document).ready(function () {
    $("#jump_page").click(function () {
        var max_num = $('#jump_page').data('page_num');
        var time_url = $('#jump_page').data('time_url');
        var page_num = $("#input_page").val();
        var link_url = window.location.href;
        var index = link_url.lastIndexOf("\/");
        link_url = link_url.substring(0, index+1);
        if (page_num > max_num || !page_num){
            if (page_num){
                window.location.href= link_url + max_num + time_url
            }
        }else {
            window.location.href= link_url + page_num + time_url
        }
    })
});





