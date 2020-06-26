$(function () {
    responsive();
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
    $(".files").css({
        'height': $(window).height() - $(".header").height() - $(".status_line").height()
    })
}

$(window).resize(function () {
    responsive()
});