
notifications = []

function magic_loop(){
    setTimeout(function() {
        var req = new XMLHttpRequest();
        username = document.getElementById('my_user_name').innerHTML
        var params = "username=" + username;

        req.onreadystatechange = function() {
            if (req.readyState == 4 && req.status == 200) {
                notifications = JSON.parse(req.response);
            }
        }

        req.open('POST', `http://${document.domain}:${location.port}/unread_notif`, true); 
        req.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
        req.send(params);
        magic_loop();
    }, 3000);
}

magic_loop();