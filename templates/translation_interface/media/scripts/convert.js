/** 
 * @fileoverview This file Transliterates the given English text into Hindi.
 * @author Chinmay Vaishampayan (chinmay@cse.iitb.ac.in)
 */

/**
 *It Converts/Transliterates the English text to Hindi
 *@author Chinmay Vaishampayan (chinmay@cse.iitb.ac.in)
 *@param {String} str Text which is to be Transliterated
 *@returns Unicode String Transliterated into Hindi
 *@type String
 */
function Convert(str)
{
	/* Dependent Vowels and there unicodes in hex */
	var dep_vowels = {
		"`aa"	:   "\u093E",
		"`ai"	:	"\u0948",
		"`ae"	:	"\u0945",
		"`ao"	:	"\u0949",
		"`au"	:	"\u094C",
		"`ou"	:	"\u094C",
		"`ii"	:	"\u0940",
		"`ee"	:	"\u0940",
		"`ee"	:	"\u0940",
		"`uu"	:	"\u0942",
		"`oo"	:	"\u0942",
		"`RR"	:	"\u0944",
		"`R"	:	"\u0943",
		"`a"	:	"",
		"`e"	:	"\u0947",
		"`i"	:	"\u093F",
		"`o"	:	"\u094B",
		"`u"	:	"\u0941"
	}

	/* Independent Vowels */
	var indep_vowels = {
		"rri"	:	"\u090B",
		"lra"	:	"\u090C",
		"aa"	:	"\u0906",
		"ao"	:	"\u0911",
		"ai"	:	"\u0910",
		"ae"	:	"\u090D",
		"au"	:	"\u0914",
		"ou"	:	"\u0914",
		"ii"	:	"\u0908",
		"ee"	:	"\u0908",
		"uu"	:	"\u090A",
		"oo"	:	"\u090A",
		"a"		:	"\u0905",
		"e"		:	"\u090F",
		"i"		:	"\u0907",
		"o"		:	"\u0913",
		"u"		:	"\u0909"
	}

	/* Consonants */
	var consonants = {
		"ksh"	: 	"\u0915\u094D\u0937",
		"jny"	:	"\u091C\u094D\u091E",
		"kh"	:	"\u0916",
		"k"		:	"\u0915",
		"q"		:	"\u0915\u093C",
		"ngh"	:	"\u0919",
		"gh"	:	"\u0918",
		"g"		:	"\u0917",
		"ch"	:	"\u091A",
		"Ch"	:	"\u091B",
		"c"		:	"\u0915",
		"jh"	:	"\u091D",
		"j"		:	"\u091C",
		"ny"	:	"\u091E",
		"Th"	:	"\u0920",
		"T"		:	"\u091F",
		"Dh"	:	"\u0922",
		"D"		:	"\u0921",
		"N"		:	"\u0923",
		"th"	:	"\u0925",
		"t"		:	"\u0924",
		"dh"	:	"\u0927",
		"d"		:	"\u0926",
		"n"   	:	"\u0928",
		"ph"	:	"\u092B",
		"p"		:	"\u092A",
		"bh"	:	"\u092D",
		"b"		:	"\u092C",
		"m"		:	"\u092E",
		"f"		:	"\u092B",
		"y"		:	"\u092F",
		"r"		:	"\u0930",
		"l"		:	"\u0932",
		"L"		:	"\u0933",
		"v"		:	"\u0935",
		"w"		:	"\u0935",
		"sh"	:	"\u0936",
		"Sh"	:	"\u0937",
		"s"		:	"\u0938",
		"h"		:	"\u0939",
		"H"		:	"\u0939",
		"z"		:	"\u091C\u093C",
		"x"		:	"\u091C\u093C"
	}

	/* Various Signs */
	/* Like Halant, Chandrabindu etc...*/
	/*Explaination:
		Symbol:		This is what the user will enter.
		Regex:	 	This scary loooking thing is used to search symbol in string. Backslash is used to escape character.
					In regular expression, we have to esacpe a backslash to consider it literally so 
						if we want to search \~, in regular expression, it will look like \\~.
					Now problem is javascript also uses backslash as esacpe character so we have to esacpe backslash here too. so each backslash will have to be replaced by two backslashes.
						i.e. \ by \\
					Therefore our simple string \~ looks like \\\\~
		Unicode:	Thats how u have to print it in javascript
	*/
	var symbols = new Array(); {
		symbols[0] = {regex:"\\.\\)",unicode:"\u0901"};	//Chandrabindu------------------------------------------symbol: ".)"
		symbols[1] = {regex:"\\)",unicode:"\u0972"}; 	//Chandra (In Marathi)----------------------------------symbol: ")"
		symbols[2] = {regex:"\\.",unicode:"\u0902"}; 	//Anuswara - Dot above letter---------------------------symbol: "."
		symbols[3] = {regex:"!",unicode:"\u093C"}; 		//Nukta - Dot below letter------------------------------symbol: "!"
		symbols[4] = {regex:":",unicode:"\u0903"}; 		//Visarga - aha sound in last---------------------------symbol: ":"
		symbols[5] = {regex:"\\$",unicode:"\u093D"}; 	//Avagraha - 'S' like character-------------------------symbol: "$"
		symbols[6] = {regex:"`",unicode:"\u094D"}; 		//Halant------------------------------------------------symbol: "`"
		symbols[7] = {regex:"OM",unicode:"\u0950"}; 	//Symbol of AUM-----------------------------------------symbol: "OM"
		symbols[8] = {regex:"AUM",unicode:"\u0950"}; 	//Symbol of AUM-----------------------------------------symbol: "AUM"
		symbols[9] = {regex:"'",unicode:"\u0951"}; 		//Symbol of Udatta - vertical dash above a letter-------symbol: "'"
		symbols[10] = {regex:"_",unicode:"\u0952"}; 	//Anudatta - Underscore below letter--------------------symbol: "_"
		symbols[11] = {regex:"<",unicode:"\u0953"}; 	//Devanagari GRAVE ACCENT-------------------------------symbol: "<"
		symbols[12] = {regex:">",unicode:"\u0954"}; 	//Devanagari ACUTE ACCENT-------------------------------symbol: ">"
		symbols[13] = {regex:"\\|\\|",unicode:"\u0965"};//Dirgha viram------------------------------------------symbol: "||"
		symbols[14] = {regex:"\\|",unicode:"\u0964"}; 	//Purna viram-------------------------------------------symbol: "|"
	}

	//Characters escaped by user are replaced with # and hex code in utf-8 format.
	//if direclty replaced with there unicode format then in next loop of symbol replacement they will be replaced again and thus there will be no use of esacping by user.
	var escapedSymbolsToHashed = new Array(); {
		escapedSymbolsToHashed[0] = {regex:"\\\\\\)",unicode:"#0029"};
		escapedSymbolsToHashed[1] = {regex:"\\\\\\.",unicode:"#002E"};
		escapedSymbolsToHashed[2] = {regex:"\\\\!",unicode:"#0021"};
		escapedSymbolsToHashed[3] = {regex:"\\\\:",unicode:"#003A"};
		escapedSymbolsToHashed[4] = {regex:"\\\\\\$",unicode:"#0024"};
		escapedSymbolsToHashed[5] = {regex:"\\\\`",unicode:"#0060"};
		escapedSymbolsToHashed[6] = {regex:"\\\\'",unicode:"#0027"};
		escapedSymbolsToHashed[7] = {regex:"\\\\_",unicode:"#005F"};
		escapedSymbolsToHashed[8] = {regex:"\\\\<",unicode:"#003C"};
		escapedSymbolsToHashed[9] = {regex:"\\\\>",unicode:"#003E"};
		escapedSymbolsToHashed[10] = {regex:"\\\\\\|",unicode:"#007C"};
	}

	//escaped characters (with #) are replaced with there unicode.
	var hashedSymbolsToUnicode = new Array(); {
		hashedSymbolsToUnicode[0] = {regex:"#0029", unicode:"\u0029"};
		hashedSymbolsToUnicode[1] = {regex:"#002E", unicode:"\u002E"};
		hashedSymbolsToUnicode[2] = {regex:"#0021", unicode:"\u0021"};
		hashedSymbolsToUnicode[3] = {regex:"#003A", unicode:"\u003A"};
		hashedSymbolsToUnicode[4] = {regex:"#0024", unicode:"\u0024"};
		hashedSymbolsToUnicode[5] = {regex:"#0060", unicode:"\u0060"};
		hashedSymbolsToUnicode[6] = {regex:"#0027", unicode:"\u0027"};
		hashedSymbolsToUnicode[7] = {regex:"#005F", unicode:"\u005F"};
		hashedSymbolsToUnicode[8] = {regex:"#003C", unicode:"\u003C"};
		hashedSymbolsToUnicode[9] = {regex:"#003E", unicode:"\u003E"};
		hashedSymbolsToUnicode[10] = {regex:"#007C", unicode:"\u007C"};
	}

	var numbers = {
		"0" : "\u0966",
		"1" : "\u0967",
		"2" : "\u0968",
		"3" : "\u0969",
		"4" : "\u096A",
		"5" : "\u096B",
		"6" : "\u096C",
		"7" : "\u096D",
		"8" : "\u096E",
		"9" : "\u096F"
	}

	var i = ""; // used to get index of array index
	
	if(str.length>0) { //Transliterate only if length of string is greater than zero.
		for (i in numbers) {
			regexp = new RegExp(i, "g");
			str = str.replace(regexp, numbers[i]);
		}

		for (i=0; i<escapedSymbolsToHashed.length; ++i) {
			regexp = new RegExp(escapedSymbolsToHashed[i].regex, "g");
			str = str.replace(regexp, escapedSymbolsToHashed[i].unicode);
		}

		/* First replace the symbols */
		for (i=0; i<symbols.length; ++i) {
			regexp = new RegExp(symbols[i].regex, "g");
			str = str.replace(regexp, symbols[i].unicode);
		}
		
		/*Then we replace the consonants
			Here we replace a consonant with consonant + `
			Symbol ` helps us to distinguish between dependent vowels and independent vowels.
			If a vowel comes after consonant, it is taken as dependent vowel. All dependent vowels will be preceded by symbol `.
			This symbol also represents HALANT. 
			so if some stray ` remains after a consonant that will mean that
				No maatra was written after that consonant
					and thus that consonant is shown with halant.
		*/
		
		for (i in consonants) {
			regexp = new RegExp(i, "g");
			replace = consonants[i]+"`";
			str = str.replace(regexp, replace);
		}
		
		/* Then we replace the Vowels which are dependent...that is MAATRAs like e, o, au...etc */
		for (i in dep_vowels) {
			regexp = new RegExp(i, "g");
			str = str.replace(regexp, dep_vowels[i]);
		}
		
		/* Now we replace Vowels which are Independent, i.e. those which are not to be combined with consonat as maatras....rather shown as a separate entity */
		for (i in indep_vowels) {
			regexp = new RegExp(i, "g");
			str = str.replace(regexp, indep_vowels[i]);
		}

		/* Remember stray symbol `
			something like HALANT...... no......you should probably check up your memory.....if you manage to remember to go to doctor that is
			Anyway... story is....
				we can't display the symbol ` as it is...
					so here we replace it with unicode of what it should look like.
		*/		
		pattern  = "`";
		regexp = new RegExp(pattern, "g");
		str = str.replace(regexp, "\u094d");
		
		for (i=0; i<hashedSymbolsToUnicode.length; ++i) {
			regexp = new RegExp(hashedSymbolsToUnicode[i].regex, "g");
			str = str.replace(regexp, hashedSymbolsToUnicode[i].unicode);
		}
	}
	return str;
}