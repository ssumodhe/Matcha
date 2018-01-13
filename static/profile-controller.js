
function displayForm(who){

	form_name = "form_" + who;
	document.forms[form_name].removeAttribute("hidden");

}

function unDisplayForm(who){

	form_name = "form_" + who;
	document.forms[form_name].setAttribute("hidden", true);

}