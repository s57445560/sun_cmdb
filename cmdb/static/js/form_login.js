/**
 * Created by 杨 on 2016/11/29.
 */

function submit_login() {
    var data_dic={};
    $('input').each(function () {
        var v = $(this).val();
        var n = $(this).attr('name');
        data_dic[n]=v;  
    });
    console.log(data_dic);
    $('.span_error').text('');
     $('.help_h4').text('');
    $.ajax({
        url:'/auth_login/',
        type:'POST',
        data:data_dic,
        dataType:'json',
        success:function (data) {
            if(data.status){
                location.href = '/home/'
            }else{
                if(data.pwd_status){
                $.each(data.message,function (k,v) {
                    $('input[name="'+k+'"]').parent().next().text(v[0].message);
                })
                }else{
                    $('.help_h4').text(data.message);
                }
            }
        }
    });
}

function submit_register() {
    var data_dic={};
    $('input').each(function () {
        var v = $(this).val();
        var n = $(this).attr('name');
        data_dic[n]=v;
    });
    console.log(data_dic);
    $('.span_error').text('');
     $('.help_h5').text('');
    $.ajax({
        url:'/auth_register/',
        type:'POST',
        data:data_dic,
        dataType:'json',
        success:function (data) {
            if(data.status){
                location.href = '/home/'
            }else{
                if(data.pwd_status){
                $.each(data.message,function (k,v) {
                    $('input[name="'+k+'"]').parent().next().text(v[0].message);
                })
                }else{
                    $('.help_h5').text(data.message);
                }
            }
        }
    });
}