function checkKey(e, form){
	console.log(e.keyCode)
	console.log("form = " + form)
	if (e.keyCode == 13){
		document.forms[form].submit();
	}
	return;
}