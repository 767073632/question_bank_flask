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
        $(".true_remove").click(function () {
            that.ops("true_remove",$(this).attr('data'))
        });
        $(".upload_file").change(function () {
            that.uplod_file_the_execl();
        })
    },
    ops:function (act,id) {
        callback = {
            "ok":function () {
                        $.ajax({
                url: common_ops.bulidUrl('/question/question_ops'),
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
        if(act=='true_remove')
        {
            common_ops.confirm('真的删除吗?!!!!!',callback=callback);
        }

    },
    uplod_file_the_execl:function () {
        var file_input = $(".upload_file");
        var name = file_input.val();
        var formData = new FormData();
        var parent_id = $(".upload_file").attr('data');
        formData.append("file",file_input[0].files[0]);
        formData.append("name",name);
        formData.append("parent_id",parent_id);
        if(name.split('.')[1]!='xlsx'){
            common_ops.alert('文件格式不对!');
            return;
        }


        callback = {
            "ok":function () {
                        $.ajax({
                url: common_ops.bulidUrl('/question/upload_the_execl'),
                type: "POST",
                data: formData,
                contentType: false,
                processData:false,
                beforeSend:function(){
                    common_ops.alert('数据上传中...')
                },
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
            'cancel':function (){$(".upload_file").val('')}
        }
        common_ops.confirm('确定上传'+name+'吗?',callback=callback);
    }

};

$(document).ready(function () {
    category_question_index_ops.init();
});