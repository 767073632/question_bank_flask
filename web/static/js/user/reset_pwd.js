;
var reset_pwd_ops = {
    init: function () {
        this.eventBind()
    },
    eventBind: function () {
        $(".save").click(function () {
            var btn_target=$(this);
            if(btn_target.hasClass('disable')){
                common_ops.alert("正在处理,请勿重复提交~~");
            }

            var old_password_tagert = $("input[id=old_password]");
            var old_password = old_password_tagert.val();

            var new_password_tagert = $("input[id=new_password]");
            var new_password = new_password_tagert.val();


            if (!old_password || old_password.length < 6) {
                common_ops.tip("请输入不少于6位的密码",old_password_tagert);
                return false
            }
            if (!new_password || new_password.length < 6) {
                common_ops.tip("请输入不少于6位的密码",new_password_tagert);
                return false
            }

            btn_target.addClass('disable');
            $.ajax({
                url: common_ops.bulidUrl('/user/reset-pwd'),
                type: "POST",
                data: {"old_password": old_password, "new_password": new_password},
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
    reset_pwd_ops.init();
});