function getData(){
        $('#action').html("<img src=\"/static/images/loading.gif\">");
        var username = $('#username').val();
        var password = $('#password').val();
        var message = JSON.stringify({
                "username": username,
                "password": password
            });

        $.ajax({
            url:'/authenticate',
            type:'POST',
            contentType: 'application/json',
            data : message,
            dataType:'json',
            success : function(response){

            },
            error: function(response){
                //alert(JSON.stringify(response));
                if (response['status'] == 401){
                    $('#action').html("<img src=\"/static/images/cross.png\" width='100px'>");
                } else {
                    $('#action').html("<img src=\"/static/images/check.png\">");
                }
            }
        });
    }