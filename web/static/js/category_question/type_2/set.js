;
var category_type1_set_ops = {
    init: function () {
        this.eventBind()
    },
    eventBind: function () {
        $(".wrap_category_type1_set .save").click(function () {
            var btn_target=$(this);
            if(btn_target.hasClass('disable')){
                common_ops.alert("正在处理,请勿重复提交~~");
            }
            var id = $(" input[name=id]").val();
            var parent_id = $("input[name=parent_id]").val();

            var name_tagert = $(" input[name=name]");
            var name = name_tagert.val();

            var is_free_tagert = $("select[name=is_free]");
            var is_free = is_free_tagert.val();


            if (!name || name.length < 1) {
                common_ops.tip("请输入1位以上的章节名",name_tagert);
                return false
            }



            btn_target.addClass('disable');
            $.ajax({
                url: common_ops.bulidUrl('/question/type2_set'),
                type: "POST",
                data: {'id':id,"name": name, "parent_id": parent_id,'is_free':is_free},
                dataType: 'json',
                success: function (res) {
                    btn_target.removeClass('disable');
                    callback = null;
                    if (res.code == 200) {
                        callback = function () {
                            window.location.href = common_ops.bulidUrl('/question/type2_index?parent_id='+parent_id);
                        }
                    }
                    common_ops.alert(res.msg, callback);
                }
            })
        });
    }
};

$(document).ready(function () {
    category_type1_set_ops.init();
});