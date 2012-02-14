function Animate(id) {
	var div = document.getElementById(id);
	id = "#" + id;
	if(div.style.display == 'none') {
		$(id).slideDown(1500);
	}
	else {
		$(id).slideUp(1500);
	}
}

function previous_TranslationsClicked(btn, div) {
	if(btn.innerHTML == "View Alternate Translations") {
		btn.innerHTML = "Hide Alternate Translations";
	}
	else {
		btn.innerHTML = "View Alternate Translations";
	}
	Animate(div);
}

function helpClicked(btn, div) {
	if(btn.innerHTML == "View Help") {
		btn.innerHTML = "Hide Help";
	}
	else {
		btn.innerHTML = "View Help";
	}
	Animate(div);
}
