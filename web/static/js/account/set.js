;
var account_set_ops = {
    init: function () {
        this.eventBind()
    },
    eventBind: function () {
        $(".wrap_account_set .save").click(function () {
            var btn_target=$(this);
            if(btn_target.hasClass('disable')){
                common_ops.alert("正在处理,请勿重复提交~~");
            }
            var uid = $(" input[name=id]").val();

            var nickname_tagert = $(" input[name=nickname]");
            var nickname = nickname_tagert.val();

            var email_tagert = $(" input[name=email]");
            var email = email_tagert.val();

            var mobile_tagert = $(" input[name=mobile]");
            var mobile = mobile_tagert.val();

            var login_name_tagert = $("input[name=login_name]");
            var login_name = login_name_tagert.val();

            var login_pwd_tagert = $(" input[name=login_pwd]");
            var login_pwd = login_pwd_tagert.val();

            if (!nickname || nickname.length < 2) {
                common_ops.tip("请输入正确的姓名",nickname_tagert);
                return false
            }
            if (!email || email.length < 2) {
                common_ops.tip("请输入正确的邮箱",email_tagert);
                return false
            }
            if (!mobile || mobile.length < 11) {
                common_ops.tip("请输入正确的手机号",mobile_tagert);
                return false
            }
            if (!login_name || login_name.length < 2) {
                common_ops.tip("请输入正确的登录名",login_name_tagert);
                return false
            }
             if (!login_pwd || login_pwd.length < 6) {
                common_ops.tip("请输入正确的密码",login_pwd_tagert);
                return false
            }

            btn_target.addClass('disable');
            $.ajax({
                url: common_ops.bulidUrl('/account/set'),
                type: "POST",
                data: {'id':uid,"nickname": nickname, "email": email,'login_name':login_name,'login_pwd':login_pwd,'mobile':mobile},
                dataType: 'json',
                success: function (res) {
                    btn_target.removeClass('disable');
                    callback = null;
                    if (res.code == 200) {
                        callback = function () {
                            window.location.href = common_ops.bulidUrl('/account/index');
                        }
                    }
                    common_ops.alert(res.msg, callback);
                }
            })
        });
    }
};

$(document).ready(function () {
    account_set_ops.init();
});