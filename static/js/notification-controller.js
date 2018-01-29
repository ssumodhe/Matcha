
notifications = []

// function setSeen(user_id)

function displayNotif(message){

    var note = document.createElement('span');
    note.setAttribute("class", "notifications");
    note.innerHTML = message;
    if (document.body.lastChild != 'span'){
        document.body.appendChild(note);
    }
    else{
        document.body.insertBefore(note, document.body.lastChild);
    }
    // Need Jquery to use this
    // setTimeout(function() {
    //     note.fadeOut('fast');
    // }, 1000);
}

function magic_loop(){
    setTimeout(function() {
        var req = new XMLHttpRequest();
        username = document.getElementById('my_user_name').innerHTML;
        var params = "username=" + username;

        req.onreadystatechange = function() {
            if (req.readyState == 4 && req.status == 200) {
                notifications = JSON.parse(req.response);
                console.log(notifications)
                if (notifications != undefined){
                    displayNotif(notifications['0']['message']);
                }
            }
        }

        req.open('POST', `http://${document.domain}:${location.port}/unread_notif`, true); 
        req.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
        req.send(params);
        magic_loop();
    }, 3000);
}

magic_loop();