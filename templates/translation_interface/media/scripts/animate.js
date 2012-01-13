/** 
 * @fileoverview This file is used for animation and other display effects.
 * @author Chinmay Vaishampayan (chinmay@cse.iitb.ac.in)
 */

/**
 *it Animates the < div > whose id is passed.
 *@author Chinmay Vaishampayan (chinmay@cse.iitb.ac.in)
 *@param {String} id id of element which is to be animated.
 */
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

/**
 *Called when button Display Help/Hide Help is clicked. Toggles the text on button and calls Animate function.
 *@author Chinmay Vaishampayan (chinmay@cse.iitb.ac.in)
 *@param {HTML Element} btn Button on clicking which function was called.
 *@param {String} div id of element which is to be animated.
 */
function helpClicked(btn, div) {
	if(btn.innerHTML == "Display Help") {
		btn.innerHTML = "Hide Help";
	}
	else {
		btn.innerHTML = "Display Help";
	}
	Animate(div);
}

/**
 *Changes text of button btn to text and after 3 seconds call another function  which changes it back to old Text. It also changes the class of button (and in turn display Style). Called  by saveWords funtion in predict file.
 *@author Chinmay Vaishampayan (chinmay@cse.iitb.ac.in)
 *@param {HTML Element} btn Button on clicking which function was called.
 *@param {String} text Text to be displayed on button (btn)
 */
function editSaveButton(btn, text) {
	var oldText = btn.innerHTML;
	btn.innerHTML = text;
	btn.setAttribute('class', 'saved');
	var func = "resetSaveButton(" + btn + ", " + oldText + ")";
	setTimeout("resetSaveButton('btnSave', 'Save All New Words')", 3000);
}

/**
 *Called by editSaveButton function after delay of 3 seconds. It changes text of button to text and resets the class of button (and in turn its display style).
 *@author Chinmay Vaishampayan (chinmay@cse.iitb.ac.in)
 *@param {String} id ID of element(button) whose text is to be changed.
 *@param {String} text Text to be displayed on element(button).
 */
function resetSaveButton(id, text) {
	var btn = document.getElementById(id);
	btn.innerHTML = text;
	btn.setAttribute('class', 'save');
}