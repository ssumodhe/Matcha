function checkMax(attr){
	attr_min = attr + "_min";
	attr_max = attr + "_max";

	min_value = document.forms['filtres'][attr_min].value;
	max_value = document.forms['filtres'][attr_max].value;
	
	if (attr_max == "pop_score_max"){
		res = min_value % 10;
		diff = 10 - parseInt(res);
		document.forms['filtres'][attr_min].value = parseInt(min_value) - parseInt(res);
		min_value = parseInt(min_value) + diff;

	}
	else{
		min_value = parseInt(min_value) + 1;
	}
	document.forms['filtres'][attr_max].setAttribute("min", min_value);
}