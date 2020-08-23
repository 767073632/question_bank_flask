;
var category_question_index_ops = {

    init: function () {
        this.eventBind()
    },
    eventBind: function () {
        var that = this;
        $(".wrap_search .search").click(function () {
            $(".wrap_search").submit();
        });
        $(".remove").click(function () {
            that.ops("remove",$(this).attr('data'))
        });
        $(".recover").click(function () {
             that.ops("recover",$(this).attr('data'))
        });
        $(".add").click(function () {
             that.ops("add",$(this).attr('data'))
        });
    },
    ops:function (act,id) {
        if (act=='add'){
            window.location.href = common_ops.bulidUrl('/question/type2_index?&parent_id='+id)
        }
        else{
        callback = {
            "ok":function () {
                        $.ajax({
                url: common_ops.bulidUrl('/question/type1_ops'),
                type: "POST",
                data: {'act':act,'id':id},
                dataType: 'json',
                success: function (res) {
                    callback = null;
                    if (res.code == 200) {
                        callback = function () {
                            window.location.href = window.location.href;
                        }
                    }
                    common_ops.alert(res.msg, callback);
                }
        })
            },
            'cancel':null
        }
        common_ops.confirm((act=='remove'?'确认删除吗?':'确认恢复吗?'),callback=callback)
            }
    }

};

$(document).ready(function () {
    category_question_index_ops.init();
});