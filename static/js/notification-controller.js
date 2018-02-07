
notifications = []

function setAsSeen(){
    var seen = new XMLHttpRequest();
    var params = "username=" + username;

    seen.open('POST', `http://${document.domain}:${location.port}/set_as_seen`, true); 
    seen.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    seen.send(params);
}

function displayNotif(message){

    var note = document.createElement('span');
    note.setAttribute("class", "notifications");
    note.innerHTML = message;
    notif_div = document.getElementById('notif')
    if (notif_div.lastChild.nodeName != 'span'){
        notif_div.appendChild(note);
    }
    else{
        notif_div.insertBefore(note, document.body.lastChild);
    }
    setAsSeen();
}

function magic_loop(){
    setTimeout(function() {
        var req = new XMLHttpRequest();
        username = document.getElementById('my_user_name').innerHTML;
        var params = "username=" + username;

        req.onreadystatechange = function() {
            if (req.readyState == 4 && req.status == 200) {
                notifications = JSON.parse(req.response);
                if (notifications.length  != 0){
                    var i = 0;
                    while (notifications[i]){
                        displayNotif(notifications[i]['message']);
                        i++;
                    }
                }
            }
        }

        req.open('POST', `http://${document.domain}:${location.port}/unread_notif`, true); 
        req.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
        req.send(params);
        magic_loop();
    }, 3000);

    setTimeout(function(){
        undisplay = document.getElementsByClassName("notifications");
        n = undisplay.length;
        n--;
        while (0 <= n){
            undisplay[n].remove();
            n--;
        }
    }, 20000)
}

magic_loop();