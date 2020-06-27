$(function () {
    responsive();

    setInterval(function () {
        var d = new Date();
        var date = d.toLocaleDateString();
        var time = d.toLocaleTimeString();
        $('.now').html(date + ' ' + time);
    }, 1000);
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
                alert("退出成功");
                location.href = '/user/login';
            } else {
                alert("退出失败");
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

$(".files").on("click", "table > tbody > .file > .file_name", function () {
    $(".popu_menu > .layout").css({
        "left": 0,
        "top": 0
    });
    $(".clicked_dom").attr("value", $(this).html());
    $(".popu_menu").show();
    $(".popu_menu > .layout").css({
        "left": $(this).offset().left + $(this).width(),
        "top": $(this).offset().top
    });
});

$(".popu_menu > .layout > .cancel").click(function () {
    $(".popu_menu").hide();
});

$(".popu_menu > .layout > .re_name").click(function () {
    var file_name = $(".clicked_dom").attr("value");

    $(".popu_menu").hide();
});

$(".popu_menu > .layout > .delete").click(function () {
    var file_name = $(".clicked_dom").attr("value");

    $(".popu_menu").hide();
});

$(".upload_file").click(function () {
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