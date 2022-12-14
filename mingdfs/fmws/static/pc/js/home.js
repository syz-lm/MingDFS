$(function () {
    function stop() {
        return false;
    }

    document.oncontextmenu = stop;

    responsive();

    setInterval(function () {
        var d = new Date();
        var date = d.toLocaleDateString();
        var time = d.toLocaleTimeString();
        $('.now').html(date + ' ' + time);
    }, 1000);

    all_file_size();
    page_files();
    get_total_pages();
});

$(".logout").click(function () {
    $.ajax({
        url: "/user/logout",
        type: 'GET',
        cache: false,
        contentType: "application/x-www-form-urlencoded",
        dataType: "json",
        success: function (data) {
            if (data.status == 1) {
                location.href = '/user/login';
            } else {
                location.href = '/user/login';
            }
        },
        error: function (err) {
            alert("网络错误");
        },
        async: true
    });
});

function responsive() {
}

$(window).resize(function () {
    responsive()
});

$(".files").on("contextmenu", "table > .file > .file_name", function () {
    $(".popu_menu > .layout").css({
        "left": 0,
        "top": 0
    });
    $(".clicked_dom").attr("value", $(this).html());
    $(".popu_menu").show();
    $(".popu_menu > .layout").css({
        "left": $(this).offset().left + $(this).width() - $(document).scrollLeft(),
        "top": $(this).offset().top - $(document).scrollTop()
    });

    var tui = $(this).attr("third_user_id");
    var ci = $(this).attr("category_id");
    var fe = $(this).attr("file_extension");
    var t = $(this).attr('title');

    $(".yj_title").html(t);
    $(".yj_category_id").html(ci);
    $(".yj_third_user_id").html(tui);
    $(".yj_file_extension").html(fe);
});

$(".popu_menu > .layout > .cancel").click(function () {
    $(".popu_menu").hide();
});

$(".popu_menu > .layout > .download").click(function () {
    var api_key = $(".api_key").html().trim();
    var title = $(".yj_title").html().trim();
    var category_id = $(".yj_category_id").html().trim();
    var third_user_id = $(".yj_third_user_id").html().trim();
    var file_extension = $(".yj_file_extension").html().trim();

    var api_key = $(".api_key").html().trim();
    var title = $(".yj_title").html().trim();
    var category_id = $(".yj_category_id").html().trim();
    var third_user_id = $(".yj_third_user_id").html().trim();
    var file_extension = $(".yj_file_extension").html().trim();

    $(".look_panel > .layout > .lp_header > .lp_title").html(title);

    $.ajax({
        type: 'GET',
        url: "/file/download",
        data: {
            'api_key': api_key,
            'third_user_id': third_user_id,
            'title': title,
            'category_id': category_id,
            'expire': 9000
        },
        cache: false,
        contentType: "application/x-www-form-urlencoded",
        dataType: "json",
        success: function (data) {
            console.log(data.status);

            if (data.status == 1) {
                var url = data.data[0]['url'];
                window.open(url);
            } else {
                alert('获取失败');
            }
        },
        error: function (err) {
            alert('网络错误');
        },
        async: true,
    });
    $(".popu_menu").hide();
});


$(".popu_menu > .layout > .get_video_first_photo").click(function () {
    var api_key = $(".api_key").html().trim();
    var title = $(".yj_title").html().trim();
    var category_id = $(".yj_category_id").html().trim();
    var third_user_id = $(".yj_third_user_id").html().trim();
    var file_extension = $(".yj_file_extension").html().trim();

    var api_key = $(".api_key").html().trim();
    var title = $(".yj_title").html().trim();
    var category_id = $(".yj_category_id").html().trim();
    var third_user_id = $(".yj_third_user_id").html().trim();
    var file_extension = $(".yj_file_extension").html().trim();

    $(".look_panel").show();

    $(".look_panel > .layout > .lp_header > .lp_title").html(title);

    $.ajax({
        type: 'GET',
        url: "/file/get_video_first_photo",
        data: {
            'api_key': api_key,
            'third_user_id': third_user_id,
            'title': title,
            'category_id': category_id,
            'expire': 9000
        },
        cache: false,
        contentType: "application/x-www-form-urlencoded",
        dataType: "json",
        success: function (data) {
            console.log(data.status);

            if (data.status == 1) {
                var url = data.data[0]['url'];
                $(".look_panel > .layout > .lp_content").attr("src", url);
                $(".popu_menu").hide();
            } else {
                alert('获取失败');
            }
        },
        error: function (err) {
            alert('网络错误');
        },
        async: true,
    });
    $(".popu_menu").hide();
});


$(".popu_menu > .layout > .look").click(function () {
    $(".look_panel > .layout").css({
        position: "absolute",
        width: "50%",
        height: "50%",
        left: "50%",
        top: "50%",
        transform: "translate(-50%, -50%)"
    });
    $(".look_panel").show();

    var api_key = $(".api_key").html().trim();
    var title = $(".yj_title").html().trim();
    var category_id = $(".yj_category_id").html().trim();
    var third_user_id = $(".yj_third_user_id").html().trim();
    var file_extension = $(".yj_file_extension").html().trim();

    $(".look_panel > .layout > .lp_header > .lp_title").html(title);

    $.ajax({
        type: 'GET',
        url: "/file/download",
        data: {
            'api_key': api_key,
            'third_user_id': third_user_id,
            'title': title,
            'category_id': category_id,
            'expire': 9000
        },
        cache: false,
        contentType: "application/x-www-form-urlencoded",
        dataType: "json",
        success: function (data) {
            console.log(data.status);

            if (data.status == 1) {
                var url = data.data[0]['url'];
                $(".look_panel > .layout > .lp_content").attr("src", url);
                $(".popu_menu").hide();

                page_files();
            } else {
                alert('获取失败');
            }
        },
        error: function(err) {
            alert('网络错误');
        },
        async: true,
    });
});


$(".lp_title").click(function () {
    if ($(".lp_win_ts").html().trim() == "translate(-50%, -50%)") {
        $(".look_panel > .layout").css({
            position: "absolute",
            width: "100%",
            height: "100%",
            left: "0",
            top: "0",
            transform: "translate(0, 0)"
        });
        $(".lp_win_ts").html("translate(0, 0)")
    }
    else {
        $(".look_panel > .layout").css({
            position: "absolute",
            width: "50%",
            height: "50%",
            left: "50%",
            top: "50%",
            transform: "translate(-50%, -50%)"
        });
        $(".lp_win_ts").html("translate(-50%, -50%)")
    }
});

$(".lp_title").contextmenu(function () {
    $(".look_panel > .layout > .lp_header > .lp_title").html("");
    $(".look_panel > .layout > .lp_content").attr("src", "about:blank");

    $(".look_panel").hide();
});

$(".popu_menu > .layout > .edit").click(function () {
    var file_name = $(".clicked_dom").attr("value");

    $(".edit_panel").show();

    $(".popu_menu").hide();
});

$(".edit_panel > .layout > .ep_edit > .ep_submit").click(function () {
    var api_key = $(".api_key").html().trim();
    var title = $(".yj_title").html().trim();
    var category_id = $(".yj_category_id").html().trim();
    var third_user_id = $(".yj_third_user_id").html().trim();
    var file_extension = $(".yj_file_extension").html().trim();

    var new_third_user_id = $(".edit_panel > .layout > .ep_edit > input:nth-child(1)").val().trim();
    var new_title = $(".edit_panel > .layout > .ep_edit > input:nth-child(2)").val().trim();
    var new_category_id = $(".edit_panel > .layout > .ep_edit > input:nth-child(3)").val().trim();
    var new_file_extension = $(".edit_panel > .layout > .ep_edit > input:nth-child(4)").val().trim();

    if (new_third_user_id == "" || new_title == "" || new_category_id == "" || new_file_extension == "") {
        alert("表单不能为空");
        return
    }

    var files = $(".edit_panel > .layout > .ep_edit > input:nth-child(5)")[0].files;
    if (files.length != 0) {
        var form_data = new FormData();
        form_data.append('api_key', api_key);
        form_data.append('src_third_user_id', third_user_id);
        form_data.append('src_title', title);
        form_data.append('src_category_id', category_id);
        form_data.append('src_file_extension', file_extension);
        form_data.append('new_third_user_id', new_third_user_id);
        form_data.append('new_title', new_title);
        form_data.append('new_category_id', new_category_id);
        form_data.append('new_file_extension', new_file_extension);
        form_data.append('upload_file_name', files[0]);

        $.ajax({
            type: 'POST',
            url: "/file/edit",
            data: form_data,
            cache: false,
            contentType: false,
            dataType: "json",
            processData: false,
            success: function (data) {
                console.log(data.status);

                if (data.status == 1) {
                    alert('编辑成功');
                    var current_page = parseInt($(".current_page").html());
                    page_files(current_page);
                    $(".edit_panel > .layout > .ep_edit > input").val("");
                } else {
                    alert('编辑失败');
                    $(".edit_panel > .layout > .ep_edit > input").val("");
                }
            },
            error: function(err) {
                alert('网络错误');
                $(".edit_panel > .layout > .ep_edit > input").val("");
            },
            async: true,
            xhr: progress
        });
    }
    else {
        var form_data = {
            'api_key': api_key,
            'src_third_user_id': third_user_id,
            'src_title': title,
            'src_category_id': category_id,
            'src_file_extension': file_extension,
            'new_third_user_id': new_third_user_id,
            'new_title': new_title,
            'new_category_id': new_category_id,
            'new_file_extension': new_file_extension
        };

        $.ajax({
            type: 'POST',
            url: "/file/edit",
            data: form_data,
            cache: false,
            contentType: "application/x-www-form-urlencoded",
            dataType: "json",
            success: function (data) {
                console.log(data.status);

                if (data.status == 1) {
                    alert('编辑成功');
                    var current_page = parseInt($(".current_page").html());
                    page_files(current_page);
                    $(".edit_panel > .layout > .ep_edit > input").val("");
                } else {
                    alert('编辑失败');
                    $(".edit_panel > .layout > .ep_edit > input").val("");
                }
            },
            error: function (err) {
                alert('网络错误');
                $(".edit_panel > .layout > .ep_edit > input").val("");
            },
            async: true,
        });
    }

    $(".edit_panel").hide();
});

$(".edit_panel > .layout > .ep_edit > .ep_cancel").click(function () {
    $(".edit_panel > .layout > .ep_edit > input").val("");
    $(".edit_panel").hide();
});

$(".popu_menu > .layout > .delete").click(function () {
    var file_name = $(".clicked_dom").attr("value");

    var api_key = $(".api_key").html().trim();
    var title = $(".yj_title").html().trim();
    var category_id = $(".yj_category_id").html().trim();
    var third_user_id = $(".yj_third_user_id").html().trim();
    var file_extension = $(".yj_file_extension").html().trim();

    $.ajax({
        type: 'POST',
        url: "/file/delete",
        data: {
            'api_key': api_key,
            'third_user_id': third_user_id,
            'title': title,
            'category_id': category_id,
            'file_extension': file_extension
        },
        cache: false,
        contentType: "application/x-www-form-urlencoded",
        dataType: "json",
        success: function (data) {
            console.log(data.status);

            if (data.status == 1) {
                alert('删除成功');
                all_file_size();
                get_total_pages();
                var current_page = parseInt($(".current_page").html());
                page_files(current_page);
            } else {
                alert('删除失败');
            }
        },
        error: function(err) {
            alert('网络错误');
        },
        async: true,
    });
    $(".popu_menu").hide();
});

$(".upload_file").click(function () {
    $('.upload_panel > .layout > input').val("");

    $(".upload_panel").show();
});

$(".submit_upload").click(function () {
    var file_name = $(".upload_panel > .layout > input[name='file_name']").val().trim();

    $(this).attr("disabled", true);
    $(this).html('正在上传，请勿点击');

    if (file_name == '') {
        alert('文件名不能为空');
        $(".submit_upload").attr("disabled", false);
        $(".submit_upload").html('提交');

        return
    }
    var api_key = $(".api_key").html().trim();

    var formData = new FormData();
    formData.append('api_key', api_key);
    formData.append('title', file_name);
    formData.append('upload_file_name', $(".upload_panel > .layout > input[name='upload_file_name']")[0].files[0]);

    $.ajax({
        type: 'POST',
        url: "/file/upload",
        data: formData,
        cache: false,
        processData: false,
        contentType: false,
        dataType: "json",
        success: function (data) {
            console.log(data.status);

            if (data.status == 1) {
                alert('上传成功');
                all_file_size();
                get_total_pages();
                page_files();
            } else {
                alert('上传失败');
            }

            $(".submit_upload").attr("disabled", false);
            $(".submit_upload").html('提交');
            $(".upload_panel").hide();
        },
        error: function(err) {
            alert('网络错误');
            $(".submit_upload").attr("disabled", false);
            $(".submit_upload").html('提交');
            $(".upload_panel").hide();
        },
        async: true,
        xhr: progress
    });
});

$(".submit_cancel").click(function () {
    $('.upload_panel > .layout > input').val("");
    $(".upload_panel").hide();
});


/* 进度条不知道如何做对话框 */
function set_progress(num) {
    $("#upload_progressbar > .layout > meter").attr("value", num);
}

function show_progress() {
    $("#upload_progressbar").show();
}

function reset_progress() {
    $("#upload_progressbar").hide();
    $("#upload_progressbar > .layout > meter").attr("value", "0");
}

function progress() {
    show_progress();
    xhr_obj = new XMLHttpRequest();
    if(xhr_obj.upload){ // check if upload property exists
        xhr_obj.upload.addEventListener('progress',function(e){
            var loaded = e.loaded; //已经上传大小情况
            var total = e.total; //附件总大小
            var percent = Math.abs(100 * loaded / total);
            set_progress(percent);

            if (percent == 100) {
                reset_progress();
            }
        }, false); // for handling the progress of the upload
    }

    return xhr_obj;
}

function all_file_size() {
    var api_key = $(".api_key").html().trim();
    $.ajax({
        type: 'POST',
        url: "/file/all_file_size",
        contentType: "application/x-www-form-urlencoded",
        data: {
            "api_key": api_key
        },
        cache: false,
        dataType: "json",
        success: function (data) {
            console.log(data.status);

            if (data.status == 1) {
                $(".all_file_size").html('已使用磁盘空间: ' + (data.data[0]['all_file_size'] / 1024 / 1024 / 1024).toFixed(2) + 'GB');
            } else {
                $(".all_file_size").html('已使用磁盘空间: 获取失败');
            }
        },
        error: function(err) {
            alert('网络错误');
        },
        async: true,
    });
}

function page_files(page) {
    var api_key = $(".api_key").html().trim();

    var page = page || $(".page").val();

    $.ajax({
        type: 'POST',
        url: "/file/page_files",
        contentType: "application/x-www-form-urlencoded",
        data: {
            "api_key": api_key,
            "page": page
        },
        cache: false,
        dataType: "json",
        success: function (data) {
            console.log(data.status);

            if (data.status == 1) {
                var cs = "<tr>\n" +
                    "                    <th>标题</th>\n" +
                    "                    <th>文件名</th>\n" +
                    "                    <th>大小(字节)</th>\n" +
                    "                    <th>创建时间</th>\n" +
                    "                    <th>最后一次修改时间</th>\n" +
                    "                    <th>最后一次访问时间</th>\n" +
                    "                </tr>";
                for (var n = 0; n < data.data.length; n++) {
                    var file_name = data.data[n]['file_name'];
                    var third_user_id = data.data[n]['third_user_id'];
                    var title = data.data[n]['title'];
                    var category_id = data.data[n]['category_id'];
                    var file_size = data.data[n]['file_size'];
                    var file_extension = data.data[n]['file_extension'];
                    var add_time = data.data[n]['add_time'];
                    var last_edit_time = data.data[n]['last_edit_time'];
                    var last_access_time = data.data[n]['last_access_time'];

                    var tmp = "<tr class='file'>" +
                        "<td class='fs_title'>" + title + "</td>" +
                        "<td class='file_name' file_extension='" + file_extension + "' third_user_id='" + third_user_id + "' title='" + title + "' category_id='" + category_id + "'>" + file_name + "</td>" +
                        "<td>" + file_size + "</td>" +
                        "<td>" + new Date(add_time * 1000).toLocaleString() + "</td>" +
                        "<td>" + new Date(last_edit_time * 1000).toLocaleString() + "</td>"
                    if (last_access_time == 0)
                        tmp += "<td>还未访问过</td>";
                    else
                        tmp = tmp + "<td>" + new Date(last_access_time * 1000).toLocaleString() + "</td></tr>";

                    cs += tmp;
                }
                $(".files > table").html(cs);
            } else {
            }
        },
        error: function(err) {
            alert('网络错误');
        },
        async: true,
    });
}


function get_total_pages() {
    var api_key = $(".api_key").html().trim();

    $.ajax({
        type: 'POST',
        url: "/file/get_total_pages",
        contentType: "application/x-www-form-urlencoded",
        data: {
            "api_key": api_key
        },
        cache: false,
        dataType: "json",
        success: function (data) {
            console.log(JSON.stringify(data));
            if (data.status == 1) {
                $(".total_pages").html(data.data[0]['total_pages']);
            }
        },
        error: function(err) {
            alert('网络错误');
        },
        async: true,
    });
}


$(".go").click(function () {
    var total_pags = parseInt($(".total_pages").html());
    var go = parseInt($(".page").val());
    if (total_pags < go || go < 1) {
        alert("跳转页数有误");
        return;
    }

    $(".current_page").html(go);
    page_files(go);
});

$(".pre").click(function () {
    var total_pags = parseInt($(".total_pages").html());
    var current_page = parseInt($(".current_page").html());
    if (total_pags < current_page - 1 || current_page - 1 < 1) {
        alert("跳转页数有误");
        return;
    }

    $(".page").val(current_page - 1);
    $(".current_page").html(current_page - 1);
    page_files(current_page - 1);
});

$(".next").click(function () {
    var total_pags = parseInt($(".total_pages").html());
    var current_page = parseInt($(".current_page").html());
    if (total_pags < current_page + 1) {
        alert("跳转页数有误");
        return;
    }

    $(".page").val(current_page + 1);
    $(".current_page").html(current_page + 1);
    page_files(current_page + 1);
});