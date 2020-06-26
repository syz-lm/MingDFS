$(".submit").click(function () {
    var user_name = $("input[name='user_name']").val();
    var passwd = $("input[name='passwd']").val();

    if (user_name == "" || passwd == "") {
        alert("表单不能为空");
        return
    }

    $.ajax({
        url: "/user/login",
        type: 'POST',
        cache: false,
        contentType: "application/x-www-form-urlencoded",
        data: {
            user_name: user_name,
            passwd: passwd,
        },
        dataType: "json",
        success: function (data) {
            if (data.status == 1) {
                alert("登录成功");
                location.href = '/home';
            } else {
                alert("登录失败");
            }
        },
        error: function (err) {
            alert("网络错误");
        },
        async: true
    });
});

$(".register").click(function () {
    location.href = '/user/register'
});


$(".change_passwd").click(function () {
    location.href = '/user/change_passwd'
});
