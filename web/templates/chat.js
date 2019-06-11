function whoami(){
        $.ajax({
            url:'/current',
            type:'GET',
            contentType: 'application/json',
            dataType:'json',
            success: function(response){
                alert(JSON.stringify(response));
                $('#cu_username').html("@" + response['username']);
                var name = response['name']+" "+response['fullname'];
                $('#cu_name').html(name);
            },
            error: function(response){
                alert(JSON.stringify(response));
            }
        });
    }

    var usersFlag = false;
    function allusers(){
        $.ajax({
            url:'/users',
            type:'GET',
            contentType: 'application/json',
            dataType:'json',
            success: function(response){
                //alert(JSON.stringify(response));
                var i = 0;
                if (!usersFlag){
                    $.each(response, function(){
                        var f = '<div class="alert" onclick="showMessages('+response[i].id+')" >';
                        f = f + response[i].username;
                        f = f + '</div>';
                        i = i+1;
                        $('#allusers').append(f);
                        $('#showUsers').val("Hide all users");
                        usersFlag = true;
                    });
                } else {
                    $('#allusers').html(" ");
                    $('#showUsers').val("Show all users");
                    usersFlag = false;
                }
            },
            error: function(response){
                alert(JSON.stringify(response));
            }
        });
    }

    function showMessages(id){
        var other_id = JSON.stringify({
                "id": id
            });
        console.log(id);
        $.ajax({
            url:'/current_chat',
            type:'GET',
            data : other_id,
            contentType: 'application/json',
            dataType:'json',
            success: function(response){
                alert(JSON.stringify(response));
            },
            error: function(response){
                alert('ERROR');
            }
        });
    }