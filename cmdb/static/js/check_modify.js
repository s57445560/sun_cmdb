function submit_modify() {
    var data_dic={};
    $('input').each(function (i) {

        var v = $(this).val();
        var n = $(this).attr('name');
        data_dic[n]=v;
        console.log(v);
                if(i==2){
            return false
        }
    });
    console.log(data_dic);
    $('.span_error').text('');
    $('.help_h6').text('');
    $.ajax({
        url:'/modify/1/',
        type:'POST',
        data:data_dic,
        dataType:'json',
        success:function (data) {
            if(data.status){
                // location.href = '/home/'
                $('#check_close').click();
                window.location.reload();
                console.log('chenggong')
            }else{
                if(data.pwd_status){
                $.each(data.message,function (k,v) {
                    $('input[name="'+k+'"]').parent().next().text(v[0].message);
                })
                }else{
                    $('.help_h6').text(data.message);
                }
            }
        }
    });
}