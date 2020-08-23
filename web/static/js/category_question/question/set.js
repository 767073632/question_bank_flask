;
var category_type1_set_ops = {
    init: function () {
        this.eventBind();
    },
    eventBind: function () {
        var that = this;
        $(".minus_choice").click(that.minus_choice);
        $(".add_choice").click(that.add_choice);
        $("select[name='type']").change(that.select_type);
        $(".wrap_category_type1_set .save").click(function () {
            var btn_target=$(this);
            if(btn_target.hasClass('disable')){
                common_ops.alert("正在处理,请勿重复提交~~");
            }
            var type = $(" select[name=type]").val();
            var name = $("textarea[name=name]").val();

            if(type==1||type==2){
                var choice_inputs = $(".single_choice input[name=choice]");
                var choices='';
                for (i=0;i<choice_inputs.length;i++){
                    var input = choice_inputs[i];
                    if(!input.value){
                        common_ops.tip('请输入信息',input)
                    }
                    choices+=input.value+'#$'
                }
                var answer = $("input[name='answer']").val();
                if(!answer){
                common_ops.tip('请输入答案',$("input[name='answer']"));
            }
            }//if type==1 or 2


            if(type==3){

                var choices = '';
                var answer = $("textarea[name='answer']").val();
                if(!answer){
                common_ops.tip('请输入答案',$("input[name='answer']"));
            }
                choices = answer;
            }//if type==3

            if(type==4){
                var choices = name;
                var answer = String($("input[type='radio']:checked").val());
            }

            var id = $("input[name='id']").val();
            var parent_id = $("input[name='parent_id']").val();
            var explanation = $("textarea[name=explanation]").val();
            if(!explanation){
                common_ops.tip('请输入解析',$("textarea[name=explanation]"));
            }


            btn_target.addClass('disable');
            $.ajax({
                url: common_ops.bulidUrl('/question/question_set'),
                type: "POST",
                data: {'id':id,"name": name, "type": type,'parent_id':parent_id,'choices':choices,'answer':answer,'explanation':explanation},
                dataType: 'json',
                success: function (res) {
                    btn_target.removeClass('disable');
                    callback = null;
                    if (res.code == 200) {
                        callback = function () {
                            window.location.href = common_ops.bulidUrl('/question/question_index?parent_id='+parent_id);
                        }
                    }
                    btn_target.removeClass('disable');
                    common_ops.alert(res.msg, callback);
                }
            })

        });

    },
    add_choice:function () {
        var div_html = '                <div class="col-lg-10">' +
            '                    <input type="text" class="form-control" placeholder="请输入选项内容" name="choice" value="">' +
            '                </div>';
        var div = $(".add_choice").parent();
        var label = div.prev();
        var label_html = '<label class="col-lg-2 control-label">'+label.html()+'</label>';
        label.before(label_html);
        label.before(div_html);
        label.html(String.fromCharCode((label.html()[0].charCodeAt()+1))+':');
    },
    minus_choice:function () {
        var div = $(".add_choice").parent();
        var label = div.prev();
        label.prev().remove();
        label.prev().remove();
        label.html(String.fromCharCode((label.html()[0].charCodeAt()-1))+':');
    },
    select_type:function () {
       var type = $("select[name='type']").val();
       if(type==1 || type==2){
           $(".single_choice").show();
            $(".judgment").hide();
            $(".anser_question").hide();
       }
       if(type==3){
           $(".single_choice").hide();
            $(".judgment").hide();
           $(".anser_question").show();
       }
       if(type==4){
           $(".single_choice").hide();
           $(".anser_question").hide();
            $(".judgment").show();
       }
    }
};

$(document).ready(function () {
    category_type1_set_ops.init();
});