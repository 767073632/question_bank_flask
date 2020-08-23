;
var account_index_ops = {

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
    },
    ops:function (act,id) {
        callback = {
            "ok":function () {
                        $.ajax({
                url: common_ops.bulidUrl('/account/ops'),
                type: "POST",
                data: {'act':act,'uid':id},
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
};

$(document).ready(function () {
    account_index_ops.init();
});