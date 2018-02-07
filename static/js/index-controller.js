// onfocus and onblur : pour quand on arrive ou quitte un input
// https://www.w3schools.com/jsref/event_onblur.asp
// https://www.w3schools.com/jsref/tryit.asp?filename=tryjsref_onblur
// https://www.w3schools.com/jsref/tryit.asp?filename=tryjsref_onblur_onfocus

// Check reg ex match with:
// https://www.w3schools.com/jsref/tryit.asp?filename=tryjsref_match_regexp


window.onload=function(){
// check file index.php on desktop
}


function checkInputs(form){
	var controller = 0;
	form_name = document.forms[form].getAttribute("name");
	inputs = document.forms[form_name].getElementsByTagName("input");
	spans = document.forms[form_name].getElementsByTagName("span");

	for (index = 0; index < inputs.length; ++index) {
		if (inputs[index].value != "")
			controller++;
	}
	if (controller == inputs.length && spans[0] == undefined){
		document.forms[form_name]["submit"].removeAttribute("disabled");
		return 0;
	}
	return 1;
}

function checkSubmit(form, attr){
	form_name = document.forms[form].getAttribute("name");
	check_value = document.forms[form_name][attr].value;
	check_disabled = document.forms[form_name]["submit"].getAttribute("disabled");
	if (check_value == "" && check_disabled == null )
		document.forms[form_name]["submit"].setAttribute("disabled", true);
	if (check_value != "" && checkInputs(form) != '1'){
		document.forms[form_name]["submit"].removeAttribute("disabled");
	}
}


function checkUsername() {
	username = document.forms["signup"]["username"].value;
	if (username == ''){
		// alert("Signfier: Il semblerait que le champ pseudo soit vide!");
		document.forms["signup"]["username"].style.backgroundColor = "rgba(199, 0, 57, 0.3)"

		var span = document.createElement('span');
		span.innerHTML = "Ce champs est vide.";
		span.setAttribute("id", "form_error");
		
		next_elem = document.forms["signup"]["username"].nextSibling;
		if (next_elem.nodeName.toLowerCase() != 'span')
			document.forms["signup"].insertBefore(span, next_elem);
	}
	else{
		document.forms["signup"]["username"].style.backgroundColor = "rgba(157, 255, 51, 0.3)"

		next_elem = document.forms["signup"]["username"].nextSibling;
		if (next_elem.nodeName.toLowerCase() == 'span')
			next_elem.remove();
	}
	checkInputs('0');
}

function checkEmail() {
	email = document.forms["signup"]["email"].value;
	regex = email.match(/^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/);
	if (email == ''){
		document.forms["signup"]["email"].style.backgroundColor = "rgba(199, 0, 57, 0.3)"

		var span = document.createElement('span');
		span.innerHTML = "Ce champs est vide.";
		span.setAttribute("id", "form_error");
		
		next_elem = document.forms["signup"]["email"].nextSibling;
		if (next_elem.nodeName.toLowerCase() != 'span')
			document.forms["signup"].insertBefore(span, next_elem);
	}
	else if (regex == null){
		document.forms["signup"]["email"].style.backgroundColor = "rgba(199, 0, 57, 0.3)"

		var span = document.createElement('span');
		span.innerHTML = "L'email est invalide";
		span.setAttribute("id", "form_error");
		
		next_elem = document.forms["signup"]["email"].nextSibling;
		if (next_elem.nodeName.toLowerCase() != 'span')
			document.forms["signup"].insertBefore(span, next_elem);
		else{
			next_elem.remove();
			next_elem = document.forms["signup"]["email"].nextSibling;
			document.forms["signup"].insertBefore(span, next_elem);
		}
	}
	else{
		document.forms["signup"]["email"].style.backgroundColor = "rgba(157, 255, 51, 0.3)"
		
		next_elem = document.forms["signup"]["email"].nextSibling;
		if (next_elem.nodeName.toLowerCase() == 'span')
			next_elem.remove();
	}
	checkInputs('0');
}

function checkPassword(){
	pswd = document.forms["signup"]["password"].value;
	regex = pswd.match(/^(?=.*[A-Z])(?=.*[a-z])(?=.*[0-9])[A-Za-z0-9_#@%\*\-]{8,24}$/);

	next_elem = document.forms["signup"]["password"].nextSibling;
	if (next_elem.nodeName.toLowerCase() == 'span' && next_elem.id != "form_info")
		next_elem.remove();

	if (regex == null){
		document.forms["signup"]["password"].style.backgroundColor = "rgba(199, 0, 57, 0.3)"
	}
	else{
		document.forms["signup"]["password"].style.backgroundColor = "rgba(157, 255, 51, 0.3)"
		
		next_elem = document.forms["signup"]["password"].nextSibling;
		if (next_elem.nodeName.toLowerCase() == 'span')
			next_elem.remove();
	}

	checkInputs('0');
}

function checkIdentical() {
	pswd = document.forms["signup"]["password"].value;
	pswd_2 = document.forms["signup"]["password_2"].value;

	if (pswd != pswd_2 || pswd == ""){
		document.forms["signup"]["password_2"].style.backgroundColor = "rgba(199, 0, 57, 0.3)";
		return 1;
	}
	else{
		document.forms["signup"]["password_2"].style.backgroundColor = "rgba(157, 255, 51, 0.3)";
		checkSubmit('0', 'password_2');
		checkInputs('0');
	}
	return 0;


}

function displayInfo(status) {
	elem = document.forms["signup"]["password"];
	next_elem = document.forms["signup"]["password"].nextSibling;

	if (status == '0'){
		var span = document.createElement('span');
		span.innerHTML = "Votre mot de passe doit avoir entre 8 et 24 caractères, <br> \
					et contenir au moins des lettres en minuscules, majuscules et des chiffres.";
		span.setAttribute("id", "form_info");

		if (next_elem.nodeName.toLowerCase() != 'span')
			document.forms["signup"].insertBefore(span, next_elem);
	}
	if (status == '1'){
		if (next_elem.nodeName.toLowerCase() == 'span' && next_elem.id == "form_info")
			next_elem.remove();
			
	}
}


























