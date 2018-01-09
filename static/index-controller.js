// onfocus and onblur : pour quand on arrive ou quitte un input
// https://www.w3schools.com/jsref/event_onblur.asp
// https://www.w3schools.com/jsref/tryit.asp?filename=tryjsref_onblur
// https://www.w3schools.com/jsref/tryit.asp?filename=tryjsref_onblur_onfocus

// Check reg ex match with:
// https://www.w3schools.com/jsref/tryit.asp?filename=tryjsref_match_regexp

function checkInputs(form){
	var controller = 0;
	form_name = document.forms[form].getAttribute("name");
	inputs = document.forms[form_name].getElementsByTagName("input");
	for (index = 0; index < inputs.length; ++index) {
		if (inputs[index].value != "")
			controller++;
	}
	if (controller == inputs.length){
		document.forms[form_name]["submit"].removeAttribute("disabled");
		return 0;
	}
	return 1;


}

function checkLastInputs(form, attr){
	form_name = document.forms[form].getAttribute("name");
	check_value = document.forms[form_name][attr].value;
	check_disabled = document.forms[form_name]["submit"].getAttribute("disabled");
	

	if (check_value == "" && check_disabled == null )
		document.forms[form_name]["submit"].createAttribute("disabled");
	if (check_value != "" && checkInputs(form) != 1)
		document.forms[form_name]["submit"].removeAttribute("disabled");

}


function checkUsername() {
	username = document.forms["signup"]["username"].value;
	if (username == ''){
		// alert("Signfier: Il semblerait que le champ pseudo soit vide!");
		document.forms["signup"]["username"].style.backgroundColor = "rgba(199, 0, 57, 0.4)"

		var span = document.createElement('span');
		span.innerHTML = "Ce champs est vide.";
		span.setAttribute("id", "form_error");
		
		next_elem = document.forms["signup"]["username"].nextSibling;
		document.forms["signup"].insertBefore(span, next_elem);
	}
	// else if (username == db->username){
	// 	alert("Signfier: Ce pseudo existe déja!");
	// 	document.forms["signup"]["username"].style.backgroundColor = "rgba(199, 0, 57, 0.4)"
	// }
	else{
		document.forms["signup"]["username"].style.backgroundColor = "rgba(157, 255, 51, 0.4)"

		next_elem = document.forms["signup"]["username"].nextSibling;
		if (next_elem.nodeName.toLowerCase() == 'span')
			next_elem.remove();
	}
	checkInputs('0');
}

function checkEmail() {
	email = document.forms["signup"]["email"].value;
	if (email == ''){
		// alert("Signfier: Il semblerait que le champ pseudo soit vide!");
		document.forms["signup"]["email"].style.backgroundColor = "rgba(199, 0, 57, 0.4)"

		var span = document.createElement('span');
		span.innerHTML = "Ce champs est vide.";
		span.setAttribute("id", "form_error");
		
		next_elem = document.forms["signup"]["email"].nextSibling;
		document.forms["signup"].insertBefore(span, next_elem);
	}
	// else if (email == db->email){
	// 	alert("Signfier: Cet email existe déja!");
	// 	document.forms["signup"]["email"].style.backgroundColor = "rgba(199, 0, 57, 0.4)"
	// }
	else{
		document.forms["signup"]["email"].style.backgroundColor = "rgba(157, 255, 51, 0.4)"
		
		next_elem = document.forms["signup"]["email"].nextSibling;
		if (next_elem.nodeName.toLowerCase() == 'span')
			next_elem.remove();
	}
	checkInputs('0');
}


