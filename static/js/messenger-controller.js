function checkKey(e, form){
	if (e.keyCode == 13){
		document.forms[form].submit()
	}
	return;
}


function defineConv(me, other){
	frame = document.getElementById("frame");
	url = "/dialog/" + me + "&" + other;
	frame.setAttribute("src", url);

	to = document.getElementById("to");
	to.setAttribute("value", other);

	form = document.getElementById("message");
	form.removeAttribute("hidden");
}