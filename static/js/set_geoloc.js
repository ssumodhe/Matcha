function successCallback(position){
	lat = position.coords.latitude;
	long = position.coords.longitude;
    console.log("Latitude : " + lat + ", longitude : " + long);
    
    var req = new XMLHttpRequest();
    var username = document.getElementById('my_user_name').innerHTML;
    // var username = "hello";
    var params = `username=${username}&lat=${lat}&long=${long}`;
    req.open('POST', `http://${document.domain}:${location.port}/set_geo`, true);
    req.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    req.send(params);
};

function errorCallback(error){
    switch(error.code){
        case error.PERMISSION_DENIED:
            console.log("L'utilisateur n'a pas autorisé l'accès à sa position");
            break;          
        case error.POSITION_UNAVAILABLE:
            console.log("L'emplacement de l'utilisateur n'a pas pu être déterminé");
            break;
        case error.TIMEOUT:
            console.log("Le service n'a pas répondu à temps");
            break;
        }
    var req = new XMLHttpRequest();
    req.open('GET', `http://${document.domain}:${location.port}/set_geo`, true);
    req.send();
};

window.onload = function send_geoloc() {
	if (navigator.geolocation) {
		navigator.geolocation.getCurrentPosition(successCallback, errorCallback);
	} else {
        console.log("Votre navigateur ne prend pas en compte la géolocalisation HTML5");
	}
}