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

function getTree() {
    var tree = [
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
            levels: 1,
            state:{
                checked:false,
                disabled:false,
                expanded:false,
                selected:false
            }
        },
    ];
    return tree
};

function getBaseUrl() {
        var url = window.location.href;
        var url_list = url.split('/');
        var base_url = url_list[0] + '//' + url_list[1] + url_list[2];
        return base_url
}
function getMapfromUrl(data) {
    var base_url = getBaseUrl();
    url = base_url+data.href;
    if (data.state.selected) {
        window.location.href = url;
    }

}

// $('#menu_tree').treeview({data:getTree()});






