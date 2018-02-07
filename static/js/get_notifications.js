
notifications = []

function setAsSeen(){
    var seen = new XMLHttpRequest();
    var params = "username=" + username;

    seen.open('POST', `http://${document.domain}:${location.port}/set_as_seen`, true); 
    seen.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    seen.send(params);
}

function createTable(){
    var table = document.createElement('table');
    table.style.width = '100%';
    table.setAttribute('border', '1');

    thead = document.createElement('thead');
	    var tr = document.createElement('tr');
	    var th_1 = document.createElement('th');
	    th_1.innerHTML = "Le";
	    tr.appendChild(th_1);

	    var th_2 = document.createElement('th');
	    th_2.innerHTML = "Objet";
	    tr.appendChild(th_2);
    thead.appendChild(tr);
    table.appendChild(thead);

    var tbdy = document.createElement('tbody');
    n = notifications.length;
    n--;
    for (n ; n >= 0 ; n--) {
        var tr = document.createElement('tr');

            var td_1 = document.createElement('td');
            td_1.innerHTML = notifications[n]['created_at']
            tr.appendChild(td_1)

            var td_2 = document.createElement('td');
            td_2.innerHTML = notifications[n]['message']
            tr.appendChild(td_2)
        
        tbdy.appendChild(tr);
    }
    table.appendChild(tbdy);

	footer = document.getElementsByTagName('footer')
	document.body.insertBefore(table, footer[0]);

}


function getNotif(){
	var req = new XMLHttpRequest();
    username = document.getElementById('my_user_name').innerHTML;
    var params = "username=" + username;

	req.onreadystatechange = function() {
		if (req.readyState == 4 && req.status == 200) {
            notifications = JSON.parse(req.response);
            if (notifications.length  != 0){
            	createTable();
            	setAsSeen();
            }
		}
	}

	req.open('POST', `http://${document.domain}:${location.port}/notifications`, true);
    req.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    req.send(params);
}

window.onlaod = getNotif();