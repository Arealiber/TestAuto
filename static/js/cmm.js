$(document).ready(function () {
    $("#jump_page").click(function () {
        var max_num = $('#jump_page').data('page_num');
        var time_url = $('#jump_page').data('time_url');
        var page_num = $("#input_page").val();
        var link_url = window.location.href;
        var index = link_url.lastIndexOf("\/");
        link_url = link_url.substring(0, index + 1);
        if (page_num > max_num || !page_num) {
            if (page_num) {
                window.location.href = link_url + max_num + time_url
            }
        } else {
            window.location.href = link_url + page_num + time_url
        }
    })
});
function getTree() {
    return [
        {
            text: "参数管理",
            tags: ['available'],
            color: "#8f9baa",
            backColor: "transparent",
            href: "/parameter/1",
            levels: 1,
        },
        {
            text: "接口管理",
            tags: ['available'],
            color: "#8f9baa",
            backColor: "transparent",
            href: "/interface/1",
            levels: 1,
        },
        {
            text: "用例管理",
            tags: ['available'],
            color: "#8f9baa",
            backColor: "transparent",
            href: "/use_case/1",
            levels: 1,
            state:{
                expanded: true
            }
        },
        {
            text: "批次管理",
            tags: ['available'],
            color: "#8f9baa",
            backColor: "transparent",
            href: "/batch/1",
            levels: 1,
        },
        {
            text: "运行日志",
            tags: ['available'],
            color: "#8f9baa",
            backColor: "transparent",
            href: "/use_case_run_log/1",
            levels: 1,
        },
        {
            text: "报表",
            tags: ['available'],
            color: "#8f9baa",
            backColor: "transparent",
            href: "/#",
            levels: 1,
        },
        {
            text: "注销",
            tags: ['available'],
            color: "#8f9baa",
            backColor: "transparent",
            href: "/#",
            levels: 1
        }]

}


function getBaseUrl() {
    var url = window.location.href;
    var url_list = url.split('/');
    return url_list[0] + '//' + url_list[1] + url_list[2];
}

function getMapfromUrl(data) {
    var base_url = getBaseUrl();
    url = base_url + data.href;
    if (data.state.selected) {
        data.state.selected = true;
        window.location.href = url;
    }

}
var treeview_data = '';
function treeview_ajax() {
    return $.ajax({
        type: 'post',
        url: '/menu_tree/info',
        data: JSON.stringify({}),
        contentType: "application/json; charset=utf-8",
        dataType: "json",
        success: function (response) {
            var menu_tree = response.res;
            treeview_data = getTree();
            treeview_data[2]['nodes'] = [];
            $.each(menu_tree, function (i, business_info) {
                treeview_data[2]['nodes'].push({
                    text: business_info.business_line.business_name,
                    tags: ['available'],
                    color: "#8f9baa",
                    backColor: "transparent",
                    levels: 2,
                    nodes: []
                });
                if (business_info.business_line.system_line.length > 0) {
                    $.each(business_info.business_line.system_line, function (j, system_info) {
                        treeview_data[2]['nodes'][i]['nodes'].push({
                            text: system_info.system_name,
                            tags: ['available'],
                            color: "#8f9baa",
                            backColor: "transparent",
                            levels: 3,
                            select_node:'',
                            nodes: []
                        });
                        if (system_info.function_line.length > 0) {
                            $.each(system_info.function_line, function (k, function_info) {
                                var function_text = function_info.function_name;
                                case_num = function_info.use_case_list.length;
                                if (case_num > 0) {
                                    function_text = function_text + '(' + case_num + ')'
                                }
                                treeview_data[2]['nodes'][i]['nodes'][j]['nodes'].push({
                                    text: function_text,
                                    tags: ['available'],
                                    color: "#8f9baa",
                                    backColor: "transparent",
                                    levels: 4,
                                    nodes: []
                                });
                                $.each(function_info.use_case_list, function(x, use_case){
                                    var use_case_text = x + 1 + '.' + use_case;
                                    treeview_data[2]['nodes'][i]['nodes'][j]['nodes'][k]['nodes'].push({
                                        text: use_case_text,
                                        tags: ['available'],
                                        color: "black",
                                        backColor: "white",
                                        levels: 4,
                                        nodes: []
                                    })
                                })
                            });
                        }
                    });
                }
            });
        }
    });
}





