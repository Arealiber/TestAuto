$(document).ready(function () {
    $("#jump_page").click(function () {
        var page_num = $("#input_page").val();
        var link_url = window.location.href;
        var index = link_url.lastIndexOf("\/");
        link_url = link_url.substring(0, index+1);
        window.location.href= link_url + page_num
    })
});





