var req = new XMLHttpRequest();
var params = "username=totolapaille";

req.onreadystatechange = function()
    {
        if (req.readyState == 4 && req.status == 200)
        {	
        	notifications = JSON.parse(req.response);
            console.log(JSON.parse(req.response)); // Another callback here
        }
    }

req.open('POST', `http://${document.domain}:${location.port}/notifications`, true); 

req.setRequestHeader("Content-type", "application/x-www-form-urlencoded");

req.send(params);
