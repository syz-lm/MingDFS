$(".send_check_code").click(function () {
    var email = $("input[name='email']").val();

    if (email == "") {
        alert("邮箱不能为空");
        return;
    }

     $.ajax({
        url: "/user/send_check_code",
        type: 'POST',
        cache: false,
        contentType: "application/x-www-form-urlencoded",
        data: {
            email: email,
        },
        dataType: "json",
        success: function (data) {
            if (data.status == 1) {
                alert("发送验证码成功");
                $(".send_check_code").hide();
                    $(".send_check_code").attr('disabled', 'true');
                    $(".send_check_code").show();
                    var n = 60;
                    var i = setInterval(function () {
                        $(".send_check_code").html(n + "秒");
                        n -= 1;
                    }, 1000);
                    setTimeout(function () {
                        $(".send_check_code").removeAttr('disabled');
                        $(".send_check_code").html("发送验证码");
                        clearInterval(i);
                    }, 60000);
            } else {
                alert("发送验证码失败");
            }
        },
        error: function (err) {
            alert("网络错误");
        },
        async: true
    });
});


$(".submit").click(function () {
    var user_name = $("input[name='user_name']").val();
    var passwd = $("input[name='passwd']").val();
    var re_passwd = $("input[name='re_passwd']").val();
    var email = $("input[name='email']").val();
    var check_code = $("input[name='check_code']").val();

    if (user_name == "" || passwd == "" || re_passwd == "" ||
        email == "" || check_code == "") {
        alert("表单不能为空");
        return
    }

    if (passwd != re_passwd) {
        alert("确认密码不正确");
        return;
    }

    $.ajax({
        url: "/user/change_passwd",
        type: 'POST',
        cache: false,
        contentType: "application/x-www-form-urlencoded",
        data: {
            user_name: user_name,
            passwd: passwd,
            re_passwd: re_passwd,
            email: email,
            check_code: check_code
        },
        dataType: "json",
        success: function (data) {
            if (data.status == 1) {
                alert("注册成功");
                location.href = '/user/login';
            } else {
                alert("注册失败");
            }
        },
        error: function (err) {
            alert("网络错误");
        },
        async: true
    });
});