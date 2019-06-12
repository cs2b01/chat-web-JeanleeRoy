

function whoami(){
        $.ajax({
            url:'/current',
            type:'GET',
            contentType: 'application/json',
            dataType:'json',
            success: function(response){
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
        $('#Enviar').on("click", function(){ sendMessage(id); });
        var id_data = JSON.stringify({
                "id": id
            });
        $.ajax({
            url:'/current_chat',
            type:'POST',
            data : id_data,
            contentType: 'application/json',
            dataType:'json',
            success: function(response){
                $('#mensajes').html("");
                var i = 0;
                $.each(response, function(){
                    var f = '<div class="msg">';
                    f = f + response[i].content;
                    f = f + '</div>';
                    $('#mensajes').append(f);
                    i++;
                });
            },
            error: function(){
                alert('ERROR');
            }
        });
    }

    
    function sendMessage(id) {
        var text_content = $('#texto').val();
        var msg_data = JSON.stringify({
                "content" : text_content,
                "user_to_id": id
            });
        $.ajax({
            url:'/send_message',
            type:'POST',
            contentType: 'application/json',
            data : msg_data,
            dataType:'json',
            success : function(){
                alert('ok');
            },
            error: function(response){
                if (response['status'] === 401){
                    alert("No se envio el mensaje :(")
                } /*else {
                    var f = '<div class="msg">';
                    f = f + text_content;
                    f = f + '</div>';
                    $('#mensajes').append(f);
                }*/
            }
        });
    }