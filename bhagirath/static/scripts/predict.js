/** 
 * This file is used to predict the possible autocompletions of some word i n input field. 
 * As a whole this file handles task of suggesting and showing word suggestions. Variable 
 * starting from g are Global Variable. 
 */

var gWords;
var gDelimeters = new Array(' ', '\t', '\n', '-', '|', '(', ')', ',');
var gWordStart; //To store position where we have to apply autocomplete.
var gWordEnd;
var gSuggestions = new Array();
var gEscapePressed = 0;

/**
 *Fucntion to get caret position.
 *@author tkirby [Courtsey: http://web.archive.org/web/20080214051356/http://www.csie.ntu.edu.tw/~b88039/html/jslib/caret.html]
 *@param {HTML Element} node Element in which caret position is required.
 *@returns Position of Caret
 *@type Int
 */
 function GetCaretPosition(node) {
	 //node.focus(); 
	 /* without node.focus() IE will returns -1 when focus is not on node */
	 if(node.selectionStart) return node.selectionStart;
	 else if(!document.selection) return 0;
	 var c = "\001";
	 var sel = document.selection.createRange();
	 var dul = sel.duplicate();
	 var length = 0;
	 dul.moveToElementText(node);
	 sel.text = c;
	 length	= (dul.text.indexOf(c));
	 sel.moveStart('character',-1);
	 sel.text = "";
	 return length;
}

/**
 *Fucntion to set caret position. 
 *@author m2pc [http://www.webdeveloper.com/forum/showthread.php?t=74982]
 *@param {HTML Element} oField Field in which caret position is to be set.
 *@param {Int} iCaretPos Index where caret position will be set.
 *@returns Nothing  is returned.
 *@type Void
 */
function SetCaretPosition(oField, iCaretPos) {
     // IE Support
     if(document.selection) { 
		oField.focus (); // Set focus on the element
		var oSel = document.selection.createRange (); // Create empty selection range
		oSel.moveStart ('character', -oField.value.length); // Move selection start and end to 0 position

		// Move selection start and end to desired position
		oSel.moveStart ('character', iCaretPos);
		oSel.moveEnd ('character', 0);
		oSel.select ();
	}
	// Firefox support
	else if(oField.selectionStart || oField.selectionStart == '0') {
		oField.selectionStart = iCaretPos;
		oField.selectionEnd = iCaretPos;
		oField.focus ();
	}
}

/**
 *This function predicts the possible completions of the words. 
 *@author Chinmay Vaishampayan
 */
function Predict(result) {
	var input = document.getElementById("translated_sentence");
	var caret = GetCaretPosition(input);
	var i=0;
	var text = input.value;
	var ld_index = -1; //index of last delimeter before caret position.
	var string; //stored  suggestions array converted to string.		
	var gWords = result;
	
	var divSuggestBox = document.getElementById("suggestion");
	if(divSuggestBox!=null) {
		document.getElementById("translate").removeChild(divSuggestBox);
	}
	
	//Set ld_index - last delimeter index
	for(i=0; i<gDelimeters.length; i++) {
		if(ld_index < text.lastIndexOf(gDelimeters[i], caret - 1)) {
			ld_index = text.lastIndexOf(gDelimeters[i], caret - 1);
		}
	}
	
	gWordStart = ld_index+1;
	gWordEnd = caret;
	
	var left_str = text.substring(0, ld_index); //Left part of string
	var word = text.substring(ld_index+1, caret);
	var right_str = text.substring(caret); 
	
	if(gWords) {
		gSuggestions = gWords;
		
		//if escape was pressed, don't show suggestions. Necessary because escape press is taken as keydown event.
		if(gEscapePressed == 1) {
			gEscapePressed = 0;
		}
		else {
			ShowSuggest(input);
		}
	}
}

function ShowSuggest(element) {
	//show suggestions only if there are suggestions !!!
	if(gSuggestions.length >=1) {
		var i=0; //for iterating in array.
		var left = 60; //left coordinate of input box relative to its parent element.
		var top = 35; //top coordinate of input box relative to its parent element.
		var lines; //will contain each line in text as array.
		var numLines=0; //calculate numLines. both due to \n and if sentence is typed larger than width of box.
		var text;
		var display = ""; //what to display in suggestions box.
		var divSuggestBox; //Will contain suggestion
		var divSuggestWord; //will contain single suggestion
		var aSuggestWord; //link element inside divSuggestWord, will contain suggestion
		var textNode; //text inside <a href=""> </a> element
		
		text = element.value;
		
		// we need to find out the position of caret in pixels. no need for text after caret.
		text = text.substring(0, GetCaretPosition(element)); 

		lines = text.split("\n");
		for(i in lines) {
			numLines += parseInt((lines[i].length)/42); //42 characters in one line.
		}
		numLines += lines.length;
		
		pos = GetCaretPosition(element);
		if (pos > 67) {
			pos = pos/67;
		}
		left += 450; //8 pixels horizontoly for one character
		top += (numLines*10) + 80; //approx height of line in pixels.
		left += pos;
		
		divSuggestBox  = document.createElement('div');
		divSuggestBox.setAttribute('id',"suggestion"); //Set its ID
		divSuggestBox.style.left = left + "px";
		divSuggestBox.style.top = top + "px";
		
		document.getElementById("translate").appendChild(divSuggestBox);
	
		for(i in gSuggestions) {
			divSuggestWord = document.createElement('div');
			divSuggestWord.setAttribute('id', "div" + gSuggestions[i]);
			divSuggestWord.setAttribute('class','divWord');
			divSuggestWord.onmouseover = HandleMouseOverDiv
 			divSuggestWord.onclick = HandleClickOnDiv;
			
			aSuggestWord = document.createElement('a');
			aSuggestWord.setAttribute('id',gSuggestions[i]);
			aSuggestWord.setAttribute('class','suggestWord');
			aSuggestWord.setAttribute('href',"");
 			aSuggestWord.onmouseover = HandleMouseOverA;
 			aSuggestWord.onkeydown = SuggestionKeyDown;
 			aSuggestWord.onfocus = Highlight;
			textNode = document.createTextNode(gSuggestions[i]);
			
			aSuggestWord.appendChild(textNode);
			divSuggestWord.appendChild(aSuggestWord);
			divSuggestBox.appendChild(divSuggestWord);
		}
		element.onkeydown = TextAreaKeyDown;
		element.onclick = HnadleClickOnTextArea;
	}
}

/**
 *Handles Click event on div which contains single suggestion word. It calls Complete function which completes the word in input textarea.
 *@author Chinmay Vaishampayan (chinmay@cse.iitb.ac.in)
 *@returns False. Means click is done browser needn't do anymore processing of this event. In effect, we have stopped click on div to do anything other than what we want.
 *@type Boolean
 */
function HandleClickOnDiv() {
	//id is divXYZ, we want XYZ which is the id of < a > element which is main for us.
	var id = document.getElementById(((this.id).substring(3))).id;
	//complete word when user clicks on it.
	Complete(document.getElementById(id), document.getElementById("translated_sentence"));
	return false;
}

/**
 *Completes the word in input textarea and its converetd version in output area.
 *@author Chinmay Vaishampayan (chinmay@cse.iitb.ac.in)
 *@param {HTML Element} source ID of source is same as word to be completed (whats writen in suggestion area)
 *@param {HTML Element} target Input Text area in which word is to be competed.
 */
function Complete(source, target) {
	var completeWord = source.id; //data of div is i.e. the word is same as id.
	
	var leftPart;
	var rightPart;
	var text;
	
	text = document.getElementById(target.id).value;
	leftPart = text.substring(0, gWordStart);
	rightPart = text.substring(gWordEnd+1);
	target.value = leftPart + completeWord + rightPart;
	
	var divSuggestBox = document.getElementById("suggestion");
	document.getElementById("translate").removeChild(divSuggestBox);
	target.focus();
	SetCaretPosition(target, gWordStart + completeWord.length);
}

/**
 *Function is used to escape characters which can be harmful to Regular Expression. Escaping is done using \
 *@author Simon Willison [http://simonwillison.net/2006/Jan/20/escape/].
 *@param {String} text Text in which characters are to be escaped.
 *@returns Escaped 
 *@type String
 */
function Escape(text) {
	if (text.length>0) {
		var specials = ['/', '.', '*', '+', '?', '|', '(', ')', '[', ']', '{', '}', '\\'];
		regexp = new RegExp('(\\' + specials.join('|\\') + ')', 'g');
  }
  return text.replace(regexp, '\\$1');
}

/**
 *Handles Mouse Over condition on < a > element. Ultimately, onFocus event is called.
 *@author Chinmay Vaishampayan (chinmay@cse.iitb.ac.in)
 */
function HandleMouseOverA() {
	this.focus();
}

/**
 *Handles Mouse Over condition on <di> element. Ultimately onFocus event is called.
 *@author Chinmay Vaishampayan (chinmay@cse.iitb.ac.in)
 */
function HandleMouseOverDiv() {
	document.getElementById((this.id).substring(3)).focus();
}

/**
 *Handles keyDown event	 on Suggestion Box. Ryan Coopers Website[http://www.ryancooper.com/resources/keycode.asp] was helpful in quickly detecting keycodes of various Keys.
 *@author Chinmay Vaishampayan (chinmay@cse.iitb.ac.in)
 *@param {HTML EVENT} event Event which took place. In this case, keyDown event.
 *@returns False in some cases. Like TAB when we want to autocomplete but not to go on next HTML element.
 *@type boolean
 */
function SuggestionKeyDown(event) {
	var keyCode;
	var i=0;
	var selected=-1;
	if(window.event) {
		keyCode = window.event.keyCode;
	}
	else if(event) {
		keyCode = event.which;
	}
	if(keyCode == 27) { //27 = escape key
		var divSuggestBox = document.getElementById("suggestion");
		if(divSuggestBox != null ) {
			document.getElementById("translate").removeChild(divSuggestBox);
		}
		document.getElementById("translated_sentence").focus();
		gEscapePressed = 1;
	}
	else if(keyCode == 13 || keyCode == 9) { //13 = Enter, 9 = TAB
		Complete(this, document.getElementById("translated_sentence"));
		return false;
	}
	else if(keyCode == 32) { //32 = space
		Complete(this, document.getElementById("translated_sentence"));
	}
	else if(keyCode == 38 || keyCode == 40) { //38=Up Key, 40 = Down Key
		for(i in gSuggestions) {
			document.getElementById(gSuggestions[i]).setAttribute('class', 'suggestWord');
		}
		for(i in gSuggestions) {
			selected++;
			if(gSuggestions[i] == this.id) {
				break;
			}
		}
		if(keyCode == 38) {
			selected--;
			if(selected == -1) {
				selected = gSuggestions.length - 1;
			}
		}
		else if(keyCode == 40) {
			selected++;
			if (selected == gSuggestions.length) {
					selected = 0;
			}				
		}
		document.getElementById(gSuggestions[selected]).focus();
		return false;
	}
	
}

/**
 *Handles keyDown event	 on TextArea. Ryan Coopers Website[http://www.ryancooper.com/resources/keycode.asp] was helpful in quickly detecting keycodes of various Keys.
 *@author Chinmay Vaishampayan (chinmay@cse.iitb.ac.in)
 *@param {HTML Element} event Event which took place. In this case, keyDown event.
 *@returns False in some cases. Like TAB when we want to autocomplete but not to go on next HTML element.
 *@type boolean
 */
function TextAreaKeyDown(event) {
	var divSuggestBox = document.getElementById("suggestion");
	if(divSuggestBox != null) {
		var keyCode;
		if(window.event) {
			keyCode = window.event.keyCode;
		}
		else if(event) {
			keyCode = event.which;
		}
		
		if(keyCode == 27) {
			document.getElementById("translate").removeChild(divSuggestBox);
			gEscapePressed = 1;
			this.focus();
		}
		else if(keyCode == 9) {
			return false;
		}
		else if(keyCode == 38){
			document.getElementById(gSuggestions[(gSuggestions.length)-1]).focus();
			return false;
		}
		else if(keyCode == 40){
			document.getElementById(gSuggestions[0]).focus();
			return false;
		}
	}
}

/**
 *Highlights focused element/suggestion contained < a > and < div > which contains < a >. Also UnHighlights all other suggestions. Called on "onfocus" Event. For ex. when sugestion is focused.
 *@author Chinmay Vaishampayan (chinmay@cse.iitb.ac.in)
 *@param {HTML Element} none this pointer is passed internally.
 */
function Highlight(){
	for(i in gSuggestions) {
		document.getElementById("div" + gSuggestions[i]).setAttribute('class', 'suggestWord');
		document.getElementById("div" + gSuggestions[i]).setAttribute('class', 'divWord');
	}
	this.setAttribute('class', 'suggestWordHighlight');
	document.getElementById("div" + this.id).setAttribute('class', 'divWordHighlight');
}

/**
 *Handles Click event on TextArea. Removes suggestion box if present.
 *@author Chinmay Vaishampayan (chinmay@cse.iitb.ac.in)
 */
function HnadleClickOnTextArea() {
	var divSuggestBox = document.getElementById("suggestion");
	document.getElementById("translate").removeChild(divSuggestBox);
}