function Animate(id) {
	var div = document.getElementById(id);
	id = "#" + id;
	if(div.style.display == 'none') {
		div.style.display = 'block';
		$(id).slideDown(1500);
	}
	else {
		div.style.display = 'none';
		$(id).slideUp(1500);
	}
}

function previous_TranslationsClicked(btn) {

	hide_div = document.getElementById("help");
	show_div = document.getElementById("previous");

	if(btn.innerHTML == "View Alternate Translations") {
		btn.innerHTML = "Hide Alternate Translations";
		show_div.style.display = 'block';
		if(hide_div.style.display == 'block') {
			a = document.getElementById("display_help"); 
			a.innerHTML = "View Help";
			hide_div.style.display = 'none';
		}
	}
	else {
		btn.innerHTML = "View Alternate Translations";
		show_div.style.display = 'none';
	}
}

function helpClicked(btn) {
	hide_div = document.getElementById("previous");
	show_div = document.getElementById("help");

	if(btn.innerHTML == "View Help") {
		if(hide_div.style.display == 'block') {
			a = document.getElementById("prev_translations");
			a.innerHTML = "View Alternate Translations";
			hide_div.style.display = 'none';
		}
		btn.innerHTML = "Hide Help";
		show_div.style.display = 'block';
	}
	else {
		btn.innerHTML = "View Help";
		show_div.style.display = 'none';
	}
}
