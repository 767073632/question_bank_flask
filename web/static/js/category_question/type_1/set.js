;
var upload = {
    error: function (msg) {
        common_ops.alert(msg);
    },
    success: function (file_key) {
        if (!file_key) {
            return;
        }
        var html = '<img src="' + common_ops.buildPicUrl(file_key) + '"/>'
            + '<span class="fa fa-times-circle del del_image" data="' + file_key + '"></span>';

        if ($(".upload_pic_wrap .pic-each").size() > 0) {
            $(".upload_pic_wrap .pic-each").html(html);
        } else {
            $(".upload_pic_wrap").append('<span class="pic-each">' + html + '</span>');
        }
        category_type1_set_ops.delete_img();
    }
};
var category_type1_set_ops = {
    init: function () {
        this.eventBind();
        this.delete_img();
    },
    eventBind: function () {
        $(".upload_pic_wrap input[name=pic]").change(function () {
            $(".upload_pic_wrap").submit();
        });

        $(".wrap_category_type1_set .save").click(function () {
            var btn_target = $(this);
            if (btn_target.hasClass('disable')) {
                common_ops.alert("正在处理,请勿重复提交~~");
            }
            var id = $(" input[name=id]").val();

            var name_tagert = $(" input[name=name]");
            var name = name_tagert.val();

            var type_tagert = $(" select[name=type]");
            var type = type_tagert.val();

            var price_tagert = $(" input[name=price]");
            var price = price_tagert.val();

            var is_free_tagert = $("select[name=is_free]");
            var is_free = is_free_tagert.val();

            var is_hot_tagert = $(" select[name=is_hot]");
            var is_hot = is_hot_tagert.val();

            if (!name || name.length < 2) {
                common_ops.tip("请输入2位以上的专业名", name_tagert);
                return false
            }
            if (parseFloat(price) <= 0) {
                common_ops.tip("请输入符合规范的售卖价格~~", price_tagert);
                return false
            }
            var main_image = $(".pic-each .del_image").attr("data");
            var data = {
                'id': id, "name": name, "type": type,
                'is_hot': is_hot, 'is_free': is_free,
                'price': price,'main_image': $(".pic-each .del_image").attr("data"),
            };
            btn_target.addClass('disable');
            $.ajax({
                url: common_ops.bulidUrl('/question/type1_set'),
                type: "POST",
                data: data,
                dataType: 'json',
                success: function (res) {
                    btn_target.removeClass('disable');
                    callback = null;
                    if (res.code == 200) {
                        callback = function () {
                            window.location.href = common_ops.bulidUrl('/question/type1_index');
                        }
                    }
                    common_ops.alert(res.msg, callback);
                }
            })
        });
    },
    delete_img: function () {
        $(".del_image").unbind().click(function () {
            $(this).parent().remove();
        })
    }
};

$(document).ready(function () {
    category_type1_set_ops.init();
});