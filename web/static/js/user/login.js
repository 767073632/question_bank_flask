;
var user_login_ops = {
    init: function () {
        this.eventBind()
    },
    eventBind: function () {
        $(".login_wrap .do_login").click(function () {
            var btn_target=$(this);

            if(btn_target.hasClass('disable')){
                common_ops.alert("正在处理,请勿重复提交~~");
            }

            var login_name = $(".login_wrap input[name=login_name]").val();
            var login_pwd = $(".login_wrap input[name=login_pwd]").val();

            if (login_pwd == undefined || login_name < 1) {
                common_ops.alert("请输入正确的登录信息")
            }
            if (login_pwd == undefined || login_pwd < 1) {
                common_ops.alert("请输入正确的登录信息")
            }

            btn_target.addClass('disable')
            $.ajax({
                url: common_ops.bulidUrl('/user/login'),
                type: "POST",
                data: {"login_name": login_name, "login_pwd": login_pwd},
                dataType: 'json',
                success: function (res) {
                    btn_target.removeClass('disable')
                    callback = null;
                    if (res.code == 200) {
                        callback = function () {
                            window.location.href = common_ops.bulidUrl('/')
                        }
                    }
                    common_ops.alert(res.msg, callback)
                }
            })
        });
    }
}

$(document).ready(function () {
    user_login_ops.init()
})