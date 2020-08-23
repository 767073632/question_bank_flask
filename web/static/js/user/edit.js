;
var user_edit_ops = {
    init: function () {
        this.eventBind()
    },
    eventBind: function () {
        $(".user_edit_wrap .save").click(function () {
            var btn_target=$(this);
            if(btn_target.hasClass('disable')){
                common_ops.alert("正在处理,请勿重复提交~~");
            }

            var nickname_tagert = $(".user_edit_wrap input[name=nickname]");
            var nickname = nickname_tagert.val();

            var email_tagert = $(".user_edit_wrap input[name=email]");
            var email = email_tagert.val();


            if (!nickname || nickname.length < 2) {
                common_ops.tip("请输入正确的姓名",nickname_tagert);
                return false
            }
            if (!email || email.length < 2) {
                common_ops.tip("请输入正确的邮箱",email_tagert);
                return false
            }

            btn_target.addClass('disable');
            $.ajax({
                url: common_ops.bulidUrl('/user/edit'),
                type: "POST",
                data: {"nickname": nickname, "email": email},
                dataType: 'json',
                success: function (res) {
                    btn_target.removeClass('disable');
                    callback = null;
                    if (res.code == 200) {
                        callback = function () {
                            window.location.href = window.location.href
                        }
                    }
                    common_ops.alert(res.msg, callback)
                }
            })
        });
    }
};

$(document).ready(function () {
    user_edit_ops.init();
});