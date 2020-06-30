function search(){
          
    var url = $("#url").val();
    var chk = $("#chk").is(":checked");
    var cookie = $("#cookie").val();
    console.log(url);
    $.ajax({

        type:"POST"
        ,url: "http://127.0.0.1:8000/api/search"
        ,data :{ URL_DATA: url, use_cookie: chk, cookie: cookie }
        ,success: function(res){

            $('#Result_modal').modal('show')
            console.log(res)

        }
        ,beforeSend:function(){
    
            $('.wrap-loading').removeClass('display-none');

        }
        ,complete:function(){

            $('.wrap-loading').addClass('display-none');
        }

        ,error:function(e){

            //조회 실패일 때 처리

        }
    });
}
function cookie_box(){

    var chk = document.getElementById('chk');

    if(chk.checked == true){
            
        document.getElementById('cookie').setAttribute('class', 'cookieTerm');
                        
    }
    else{

        document.getElementById('cookie').setAttribute('class', 'cookieTerm display-none');
  
   }

}

