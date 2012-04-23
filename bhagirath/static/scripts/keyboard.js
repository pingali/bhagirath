/* Hindi Text Input APIS -  http://www.hinkhoj.com */
/* NOTE: Below code is taken originally from Monusoft and Modified by Hinkhoj.com */

var Vowel = new Array(123);
var VowelCombination = new Array(6);
var Consonant = new Array(123);
var ConsonantCombination = new Array(27);
var Symbol = new Array(60);
var VIRAM = 1;
var VRU = 2;
var RU = 3;
var ZWJ=4;
var ZWNJ=5;
var language = "Hindi";
var find = "";
var lists = new Array();

Symbol[32] = "\u0020"; // space
Symbol[58] = "\u0903"; // visarg
Symbol[48] = "\u0966"; //0
Symbol[49] = "\u0967"; //1
Symbol[50] = "\u0968"; //2
Symbol[51] = "\u0969"; //3
Symbol[52] = "\u096a"; //4
Symbol[53] = "\u096b"; //5
Symbol[54] = "\u096c"; //6
Symbol[55] = "\u096d"; //7
Symbol[56] = "\u096e"; //8
Symbol[57] = "\u096f"; //9

Vowel[97] = "\u0905"; //a
Vowel[65] = "\u0906"; //A
Vowel[105] = "\u0907"; //i
Vowel[73] = "\u0908"; //I
Vowel[117] = "\u0909"; //u 
Vowel[85] = "\u090a"; //U
Vowel[82] = "\u090b"; // R
Vowel[69] = "\u090d"; // E
Vowel[101] = "\u090f"; //e
Vowel[79] = "\u0911"; //O
Vowel[111] = "\u0913"; // o

VowelCombination[0] = new Array(3);
VowelCombination[0][0]= 97; //a
VowelCombination[0][1]= 97; //a
VowelCombination[0][2]= "\u0906"; //aa

VowelCombination[1] = new Array(3);
VowelCombination[1][0]= 101; //e
VowelCombination[1][1]= 101; //e
VowelCombination[1][2]= "\u0908"; //ee

VowelCombination[2] = new Array(3);
VowelCombination[2][0]= 111; //o
VowelCombination[2][1]= 111; //o
VowelCombination[2][2]= "\u090a"; //oo

VowelCombination[3] = new Array(3);
VowelCombination[3][0]= 82; //R
VowelCombination[3][1]= 85; //U
VowelCombination[3][2]= "\u090b"; 

VowelCombination[4] = new Array(3);
VowelCombination[4][0]= 97; //a
VowelCombination[4][1]= 105; //i
VowelCombination[4][2]= "\u0910"; //ai

VowelCombination[5] = new Array(3);
VowelCombination[5][0]= 97; //a
VowelCombination[5][1]= 117; //u 
VowelCombination[5][2]= "\u0914"; //au

Consonant[94] = "\u0901"; // chandrabindu
Consonant[77] = "\u0902"; // M
Consonant[107] = "\u0915"; //k
Consonant[103] = "\u0917"; //g
Consonant[106] = "\u091c"; //j
Consonant[122] = "\u091d"; //z
Consonant[84] = "\u091f"; //T
Consonant[68] = "\u0921"; //D
Consonant[78] = "\u0923"; //N
Consonant[116] = "\u0924"; //t
Consonant[100] = "\u0926"; //d
Consonant[110] = "\u0928"; //n
Consonant[112] = "\u092a"; //p
Consonant[102] = "\u092b"; //f
Consonant[98] = "\u092c"; //b
Consonant[109] = "\u092e"; //m
Consonant[121] = "\u092f"; //y
Consonant[114] = "\u0930"; //r
Consonant[108] = "\u0932"; //l
Consonant[76] = "\u0933"; //L
Consonant[118] = "\u0935"; //v
Consonant[119] = "\u0935"; //w
Consonant[115] = "\u0938"; //s
Consonant[120] = "\u0915\u094d\u0937"; //kSh
Consonant[104] = "\u0939"; //h
Consonant[97] = ""; // just empty string
Consonant[VIRAM] = "\u094d"; // half letter
Consonant[ZWJ] = "\u200D"; // ZWJ
Consonant[ZWNJ] = "\u200C"; // half letter
Consonant[65] = "\u093e"; //A
Consonant[105] = "\u093f"; //i
Consonant[73] = "\u0940"; //I
Consonant[117] = "\u0941"; //u
Consonant[85] = "\u0942"; //U
Consonant[VRU] = "\u0943"; // VRU
Consonant[69] = "\u0945"; //E
Consonant[101] = "\u0947"; //e
Consonant[79] = "\u0949"; //O
Consonant[111] = "\u094b"; //o
Consonant[75] = "\u0958"; //K
Consonant[71] = "\u095a"; //G
Consonant[90]= "\u095b"; //Z
Consonant[70]= "\u095e"; //F
Consonant[89]= "\u095f"; //Y

ConsonantCombination[0] = new Array(3);
ConsonantCombination[0][0]= 107; //k
ConsonantCombination[0][1]= 104; //h
ConsonantCombination[0][2]= "\u0916"; // kh

ConsonantCombination[1] = new Array(3);
ConsonantCombination[1][0]= 103; //g
ConsonantCombination[1][1]= 104; //h
ConsonantCombination[1][2]= "\u0918"; //gh

ConsonantCombination[2] = new Array(3);
ConsonantCombination[2][0]= 99; //c
ConsonantCombination[2][1]= 104; //h
ConsonantCombination[2][2]= "\u091a"; //ch

ConsonantCombination[3] = new Array(3);
ConsonantCombination[3][0]= 67; //C
ConsonantCombination[3][1]= 104; //h
ConsonantCombination[3][2]= "\u091b"; //Ch

ConsonantCombination[4] = new Array(3);
ConsonantCombination[4][0]= 84; //T
ConsonantCombination[4][1]= 104; //h
ConsonantCombination[4][2]= "\u0920"; //Th

ConsonantCombination[5] = new Array(3);
ConsonantCombination[5][0]= 68; //D
ConsonantCombination[5][1]= 104; //h
ConsonantCombination[5][2]= "\u0922"; //Dh

ConsonantCombination[6] = new Array(3);
ConsonantCombination[6][0]= 116; //t
ConsonantCombination[6][1]= 104; //h
ConsonantCombination[6][2]= "\u0925"; //th

ConsonantCombination[7] = new Array(3);
ConsonantCombination[7][0]= 100; //d
ConsonantCombination[7][1]= 104; //dh
ConsonantCombination[7][2]= "\u0927"; //dh

ConsonantCombination[8] = new Array(3);
ConsonantCombination[8][0]= 112; //p
ConsonantCombination[8][1]= 104; //ph
ConsonantCombination[8][2]= "\u092b"; //ph

ConsonantCombination[9] = new Array(3);
ConsonantCombination[9][0]= 98; //b
ConsonantCombination[9][1]= 104; //h
ConsonantCombination[9][2]= "\u092d"; //bh

ConsonantCombination[10] = new Array(3);
ConsonantCombination[10][0]= 115; //s
ConsonantCombination[10][1]= 104; //h
ConsonantCombination[10][2]= "\u0936"; //sh

ConsonantCombination[11] = new Array(3);
ConsonantCombination[11][0]= 83; //S
ConsonantCombination[11][1]= 104; //h
ConsonantCombination[11][2]= "\u0937"; //Sh

ConsonantCombination[12] = new Array(3);
ConsonantCombination[12][0]= 74; //J
ConsonantCombination[12][1]= 104; //h
ConsonantCombination[12][2]= "\u091c\u094d\u091e"; // Jh

ConsonantCombination[13] = new Array(3);
ConsonantCombination[13][0]= 97; //a
ConsonantCombination[13][1]= 97; //a
ConsonantCombination[13][2]= "\u093e"; //aa

ConsonantCombination[14] = new Array(3);
ConsonantCombination[14][0]= 101; //e
ConsonantCombination[14][1]= 101; //e
ConsonantCombination[14][2]= "\u0940"; //ee

ConsonantCombination[15] = new Array(3);
ConsonantCombination[15][0]= 111; //o
ConsonantCombination[15][1]= 111; //o
ConsonantCombination[15][2]= "\u0942"; //oo

ConsonantCombination[16] = new Array(3);
ConsonantCombination[16][0]= 97; //a
ConsonantCombination[16][1]= 105; //i
ConsonantCombination[16][2]= "\u0948"; //ai

ConsonantCombination[17] = new Array(3);
ConsonantCombination[17][0]= 97; //a
ConsonantCombination[17][1]= 117; //u
ConsonantCombination[17][2]= "\u094c"; //au

ConsonantCombination[18] = new Array(3);
ConsonantCombination[18][0] = 78; // N
ConsonantCombination[18][1] = 71; // G
ConsonantCombination[18][2] = "\u0919"; //NG

ConsonantCombination[19] = new Array(3);
ConsonantCombination[19][0] = 78; // N
ConsonantCombination[19][1] = 89; // Y
ConsonantCombination[19][2] = "\u091e"; //NY

ConsonantCombination[20] = new Array(3);
ConsonantCombination[20][0] = 75; // K
ConsonantCombination[20][1] = 104; // h
ConsonantCombination[20][2] = "\u0959"; //Kh

ConsonantCombination[21] = new Array(3);
ConsonantCombination[21][0] = 68; // D
ConsonantCombination[21][1] = 68; // D
ConsonantCombination[21][2] = "\u095c"; //DD

ConsonantCombination[22] = new Array(3);
ConsonantCombination[22][0] = 68; // D
ConsonantCombination[22][1] = 72; // H
ConsonantCombination[22][2] = "\u095d"; //DH

ConsonantCombination[23] = new Array(3);
ConsonantCombination[23][0] = 78; // N
ConsonantCombination[23][1] = 78; // N
ConsonantCombination[23][2] = "\u0929"; //NN

ConsonantCombination[24] = new Array(3);
ConsonantCombination[24][0] = 82; // R
ConsonantCombination[24][1] = 82; // R
ConsonantCombination[24][2] = "\u0931"; //RRa

ConsonantCombination[25] = new Array(3);
ConsonantCombination[25][0] = 76; // L
ConsonantCombination[25][1] = 76; // L
ConsonantCombination[25][2] = "\u0934"; //LL


ConsonantCombination[26] = new Array(3);
ConsonantCombination[26][0]= 106; //j
ConsonantCombination[26][1]= 104; //h
ConsonantCombination[26][2]= "\u091d"; // jh

var prevkey = 32;
var ppkey=32;
var hidden=false;
var posChanged = true;
var isEng = false;

var previousConsonant = false;
var previouspreviousConsonant = false;
var pVowel=false;
var pppC=false;
var isHinLetter=false;

function ClearAllParameters()
{
	prevkey = 32;
	hidden=false;
	posChanged = true;

	previousConsonant = false;
	previouspreviousConsonant = false;
	pppC=false;
	pVowel=false; 
	isHinLetter=false;
}

function changeCursor(txtarea)	{
	if (txtarea.createTextRange)	{
		txtarea.cursorPos = document.selection.createRange().duplicate();
	}
}
function GetVowelCombination(key0, key1)
{
	var i=0;
	for(i=0;i<VowelCombination.length;i++)
	{
		if((VowelCombination[i][0] == key0) && (VowelCombination[i][1]==key1))
			return VowelCombination[i][2];	
	}
}

function GetConsonantCombination(key0, key1)
{
	var i=0;
	for(i=0;i<ConsonantCombination.length;i++)
	{
		if((ConsonantCombination[i][0] == key0) && (ConsonantCombination[i][1]==key1))
		{
			return ConsonantCombination[i][2];
		}	
	}
}

function isLetter(aChar)
{
	return ((aChar >= 'a') && (aChar <= 'z')) ||
	((aChar >= 'A') && (aChar <= 'Z'));
}

function isDigit(aChar)
{
	return ((aChar >= '0') && (aChar <= '9'));
}

var activeWord="";
var txtFieldTTHide=false;

function hideTxtBoxTT()
{
	if(!txtFieldTTHide)
	{
		hideTooltip('txtFieldInput');
		txtFieldTTHide=true;
	}
}

function displayRelatedWords(keyChar,awTableId)
{
	switch(keyChar)
	{
	case 'a':
	case 'o':
	case 'i':
	case 'I':
	case 'e':
	case 'E':
	case 'A':
	case 'O':
	case 'u':
	case 'U':
		activeWord="";
		break;

	case 'k':
	case 'g':
	case 'c':
	case 'C':
	case 'j':
	case 'J':
	case 'z':
	case 'T':
	case 'N':
	case 't':
	case 'd':
	case 'n':
	case 'p':
	case 'f':
	case 'b':
	case 'm':
	case 'y':
	case 'l':
	case 'v':
	case 's':
	case 'w':
	case 'x':

		activeWord=keyChar;
		break;
	case 'h':
	case 'G':
	case 'Y':
	case 'K':
	case 'G':
	case 'Z':
	case 'H':
	case 'F':
	case 'S':
	case 'r':
	case 'D':
	case 'L':
		activeWord+=keyChar;
	}
	if(keyChar==" ") {
      resetTableDiv(awTableId);
    }
    else {
		displayInDiv(activeWord,awTableId);
	}
}

function displayInDiv(aw,awTableId)
{
	var divPane=document.getElementById(awTableId);
	if(divPane==null)
	{
		return; 
	}

	switch(aw)
	{
	case 'k':
		displayCombination(divPane,'k','&#x0915;');
		break;

	case 'kh':
		displayCombination(divPane,'kh','&#x0916;');
		break;
	case 'g':
		displayCombination(divPane,'g','&#x0917;');
		break;
	case 'gh':
		displayCombination(divPane,aw,'&#x0918;');
		break;
	case 'c':
		displayAdditional(divPane,'ch','cha','Cha','&#x091A;','&#x091A;','&#x091B;');
		break;
	case 'ch':
		displayCombination(divPane,'ch','&#x091A;');
		break;
	case 'Ch':
		displayCombination(divPane,'Ch','&#x091B;');
		break;
	case 'NG':
		displayCombination(divPane,aw,'&#x0919;');
		break;
	case 'j':
		displayAdditional(divPane,aw,'za','Za','&#x091C;','&#x091D;','&#x095B;');
		break;
	case 'z':
		displayCombination(divPane,aw,'&#x091D;');
		break;
	case 'NY':
		displayCombination(divPane,aw,'&#x091E;');
		break;
	case 'T':
		displayCombination(divPane,aw,'&#x091F;');
		break;
	case 'Th':
		displayCombination(divPane,aw,'&#x0920;');
		break;
	case 'D':
		displayCombination(divPane,aw,'&#x0921;');
		break;
	case 'Dh':
		displayCombination(divPane,aw,'&#x0922;');
		break;
	case 'N':
		displayCombination(divPane,aw,'&#x0923;');
		break;
	case 't':
		displayAdditional(divPane,aw,'Ta','Tha','&#x0924;','&#x091F;','&#x0920;');
		break;
	case 'th':
		displayCombination(divPane,aw,'&#x0925;');
		break;
	case 'd':
		displayAdditional(divPane,aw,'Da','Dha','&#x0926;','&#x0921;','&#x0922;');
		break;
	case 'dh':
		displayCombination(divPane,aw,'&#x0927;');
		break;
	case 'n':
		displayAdditional(divPane,aw,'Na','NNa','&#x0928;','&#x0923;','&#x0929;');
		break;
	case 'p':
		displayCombination(divPane,aw,'&#x092A;');
		break;
	case 'f':
		displayCombination(divPane,aw,'&#x092B;');
		break;
	case 'b':
		displayCombination(divPane,aw,'&#x092C;');
		break;
	case 'bh':
		displayCombination(divPane,aw,'&#x092D;');
		break;
	case 'm':
		displayCombination(divPane,aw,'&#x092E;');
		break;
	case 'y':
		displayCombination(divPane,aw,'&#x092F;');
		break;
	case 'r':
		displayCombination(divPane,aw,'&#x0930;');
		break;
	case 'l':
		displayCombination(divPane,aw,'&#x0932;');
		break;
	case 'v':
		displayCombination(divPane,aw,'&#x0935;');
	case 'w':
		displayCombination(divPane,aw,'&#x0935;');
		break;
	case 's':
		displayAdditional(divPane,aw,'sha','Sha','&#x0938;','&#x0936;','&#x0937;');
		break;
	case 'sh':
		displayCombination(divPane,aw,'&#x0936;');
		break;
	case 'Sh':
		displayCombination(divPane,aw,'&#x0937;');
		break;
	case 'h':
		displayCombination(divPane,aw,'&#x0939;');
		break;
	case 'L':
		displayCombination(divPane,aw,'&#x0933;');
		break;
	case 'kSh':
		displayCombination(divPane,aw,'&#x0915;&#x094D;&#x0937;');
		break;
	case 'x':
		displayCombination(divPane,aw,'&#x0915;&#x094D;&#x0937;');
		break;
	case 'Jh':
		displayCombination(divPane,aw,'&#x091C;&#x094D;&#x091E;');
		break;
	case 'tr':
		displayCombination(divPane,aw,'&#x0924;&#x094D;&#x0930;');
		break;
	case 'LL':
		displayCombination(divPane,aw,'&#x0934;');
		break;
	case 'K':
		displayCombination(divPane,aw,'&#x0958;');
		break;
	case 'Kh':
		displayCombination(divPane,aw,'&#x0959;');
		break;
	case 'G':
		displayCombination(divPane,aw,'&#x095A;');
		break;
	case 'Z':
		displayCombination(divPane,aw,'&#x095B;');
		break;
	case 'DD':
		displayCombination(divPane,aw,'&#x095C;');
		break;
	case 'DH':
		displayCombination(divPane,aw,'&#x095D;');
		break;
	case 'F':
		displayCombination(divPane,aw,'&#x095E;');
		break;
	case 'Y':
		displayCombination(divPane,aw,'&#x095F;');
		break;
	}
}

function Get2DArray(row,col)
{
	var lngArray= new Array(row);
	for(var i=0;i<lngArray.length;i++)
	{
		lngArray[i]= new Array(col);
	}
	return lngArray;
}

function displayAdditional(divPane,el,el2,el3,luc,luc2,luc3)
{
	var lngArray=Get2DArray(17,2);
	var normalArray=GetNormalDisplayArray(el,luc);
	lngArray[0][0]=el2;
	lngArray[0][1]=luc2;
	lngArray[1][0]=el3;
	lngArray[1][1]=luc3;
	for(var i=0;i<normalArray.length;i++)
	{
		lngArray[i+2][0]=normalArray[i][0];
		lngArray[i+2][1]=normalArray[i][1];
	}
	displayArrayInTable(divPane,lngArray);
}

function GetNormalDisplayArray(el,luc)
{
	var lngArray=Get2DArray(15,2);
	lngArray[0][0]=(el);
	lngArray[0][1]=(luc+'&#x094D;');
	lngArray[1][0]=(el+'a');
	lngArray[1][1]=(luc);
	lngArray[2][0]=(el+'A');
	lngArray[2][1]=(luc+'&#x093E;');
	lngArray[3][0]=(el+'e');
	lngArray[3][1]=(luc+'&#x0947;');
	lngArray[4][0]=(el+'ai');
	lngArray[4][1]=(luc+'&#x0948;');
	lngArray[5][0]=(el+'i');
	lngArray[5][1]=(luc+'&#x093F;');
	lngArray[6][0]=(el+'I');
	lngArray[6][1]=(luc+'&#x0940;');

	lngArray[7][0]=(el+'o');
	lngArray[7][1]=(luc+'&#x094B;');

	lngArray[8][0]=(el+'au');
	lngArray[8][1]=(luc+'&#x094C;');

	lngArray[9][0]=(el+'u');
	lngArray[9][1]=(luc+'&#x0941;');

	lngArray[10][0]=(el+'U');
	lngArray[10][1]=(luc+'&#x0942;');

	lngArray[11][0]=(el+'M');
	lngArray[11][1]=(luc+'&#x0902;');
	lngArray[12][0]=(el+'~M');
	lngArray[12][1]=(luc+'&#x0901;');
	lngArray[13][0]=(el+'^');
	lngArray[13][1]=(luc+'&#x094D;&#x200D;');
	lngArray[14][0]=(el+'^^');
	lngArray[14][1]=(luc+'&#x094D;&#x200C;');
	return lngArray;
}

function displayCombination(divPane,el,luc)
{
	var lngArray=GetNormalDisplayArray(el,luc);
	displayArrayInTable(divPane,lngArray);
}

function displaykh(divPane)
{
	divPane.innerHTML+="kh|kha|khi|khI|khe";
}

function displayArrayInTable(tableDiv,lngArray)
{
	if(tableDiv==null)
	{
		return;
	}
	else
	{
		if(tableDiv.rows!=null)
		{
			if(tableDiv.rows.length!=null)
			{
				if(tableDiv.rows.length >=2)
				{

					tableDiv.deleteRow(1);

					tableDiv.deleteRow(0); 
				}
			} 
		}
		var newRow = tableDiv.insertRow(0);
		var newCol=newRow.insertCell(0);
		newCol.innerHTML=("<span>"+lngArray[0][1]+"</span>");
		for(var i=1;i<lngArray.length;i++)
		{
			newCol=newRow.insertCell(i);
			newCol.innerHTML=("<span class='awSpan2'>"+lngArray[i][1]+"</span>");
		} 
		newRow = tableDiv.insertRow(1);
		newCol=newRow.insertCell(0);
		newCol.innerHTML=("<span>"+lngArray[0][0]+"</span>");
		for(var i=1;i<lngArray.length;i++)
		{
			newCol=newRow.insertCell(i);
			newCol.innerHTML=("<span class='awSpan2'>"+lngArray[i][0]+"</span>");
		}  
	}
}

function displayArray(divPane,lngArray)
{
	var pad="";
	if(lngArray[0][0].length==2)
	{
		pad=" ";
	}
	divPane.innerHTML+=("<span>"+lngArray[0][1]+"</span>");
	for(var i=1;i<lngArray.length;i++)
	{
		divPane.innerHTML+=("<span class='awSpan2'>"+lngArray[i][1]+pad+"</span>");
	}  
	divPane.innerHTML+="<br>";

	divPane.innerHTML+=("<span>"+lngArray[0][0]+"</span>");
	for(var i=1;i<lngArray.length;i++)
	{
		divPane.innerHTML+=("<span class='awSpan2'>"+lngArray[i][0]+"</span>");
	}  
	divPane.innerHTML+="<br>";
}

function GetKeyChar(evt)
{
	var e = window.event? event : evt;
	if( e.altKey || e.ctrlKey)
	{
		return true;
	}
	var key=0;
	var keychar='';
	if ( document.all )
	{
		key = e.keyCode;

	}	
	else
	{
		key = e.which;

	}
	if(key==null)
	{
		key=evt.keyCode?evt.keyCode:evt.which;
	}

	keychar = String.fromCharCode(key);
	return keychar;
}

function HindiKeyBoard(){}

var inputBoxIds= new Array();
var inputBoxCount=0;

function GetNewKeyboard(elemID,awTableId)
{
	GetNewKeyboard(elemID,"awTable");
}

function GetNewKeyboard(elemID,awTableId)
{
	var newHinKB= new HindiKeyBoard();
	newHinKB.prevkey = 32;
	newHinKB.ppkey=32;
	newHinKB.hidden=false;
	newHinKB.posChanged = true;
	newHinKB.isEng = false;

	newHinKB.previousConsonant = false;
	newHinKB.previouspreviousConsonant = false;
	newHinKB.pVowel=false;
	newHinKB.pppC=false;
	newHinKB.isHinLetter=false;
	newHinKB.elemID=elemID;
	newHinKB.awTableId=awTableId;
	return newHinKB;
}

function ClearAllParameters(hinKB)
{
	hinKB.prevkey = 32;
	hinKB.hidden=false;
	hinKB.posChanged = true;

	hinKB.previousConsonant = false;
	hinKB.previouspreviousConsonant = false;
	hinKB.pppC=false;
	hinKB.pVowel=false; 
	hinKB.isHinLetter=false;
}

function positionChange(evt,hinKB)
{
	var keyCode = 
		document.layers ? evt.which :
			document.all ? event.keyCode :
				document.getElementById ? evt.keyCode : 0;
	if(keyCode==null)
	{
		keyCode=(evt.keyCode)?evt.keyCode:evt.which;
	}

	if (keyCode == 123)
	{
		hinKB.isEng = !hinKB.isEng;
		ClearAllParameters(hinKB);
	}
	
	if (keyCode >= 37 && keyCode <=40)
	{
		hinKB.posChanged = true;
	}

	if(keyCode==8)
	{
		hinKB.previousConsonant=hinKB.previouspreviousConsonant;
		hinKB.previouspreviousConsonant=hinKB.pppC;
		hinKB.pppC=false;
		if(hinKB.isHinLetter)
		{
			ClearAllParameters(hinKB);
		}

		var txtInpt=document.getElementById(hinKB.elemID);
		if(txtInpt.value==null || txtInpt.value=="" || txtInpt.value.length==1)
		{
			ClearAllParameters(hinKB);
		}
	}	
}

var charArray = new Array();

function resetTableDiv(tableId)
{
    var tableDiv = document.getElementById(tableId);
    if(tableDiv.rows!=null)
		{
			if(tableDiv.rows.length!=null)
			{
				if(tableDiv.rows.length >=2)
				{
					tableDiv.deleteRow(1);
					tableDiv.deleteRow(0); 
				}
			} 
		}
}

function change(evt,hinKB)
{      
	var txtarea=document.getElementById(hinKB.elemID);
	var displace = 0;
	var text='';
	var previousValue = "";
	
	var e = window.event? event : evt;
	if( e.altKey || e.ctrlKey)
	{
		return true;
	}
	var key=0;
	var keychar='';
	var shift=false;
	var pos= 0; // doGetCaretPosition (txtarea);
	var prevpos = 0;
	if ( document.all )
	{
		key = e.keyCode;

	}	
	else
	{
		key = e.which;

	}
	if(key==null)
	{
		key=evt.keyCode?evt.keyCode:evt.which;
	}

	if ((key <32 && key!=8) || (key >=33 && key <=47) ||(key>=59 && key <=64)||(key>=91 && key<=96 && key!=94)||(key>=123 && key<=127 && key!=126) || key >255 )
	{
		ClearAllParameters(hinKB);
		return true;
	}
	
    if(key == 8)
    {
		charArray.splice(charArray.length-1,1);
		key = charArray[charArray.length-1];
		keychar = String.fromCharCode(key);
		displayRelatedWords(keychar,hinKB.awTableId);
		ClearAllParameters(hinKB);
		if(txtarea.value.length==1)
		  resetTableDiv(hinKB.awTableId);
		return true;
	}
	keychar = String.fromCharCode(key);
	charArray.push(key);
	if(hinKB.posChanged)
	{
		hinKB.prevkey = 32;
		hinKB.hidden=false;
		prevpos = 0;
		hinKB.previousConsonant = false;
		hinKB.previouspreviousConsonant = false;
		hinKB.pppC=false;
	}
	displayRelatedWords(keychar,hinKB.awTableId);
	switch(keychar)
	{
	case "a":
		var cComb = GetConsonantCombination(hinKB.prevkey,key);
		var vComb = GetVowelCombination(hinKB.prevkey,key);
		hinKB.pVowel=true;

		if(hinKB.previousConsonant)
		{
			displace =0;
			text=Consonant[key]; // nothing to append. just remove viram
			hinKB.isHinLetter=true;
		}
		else if (typeof(vComb) != 'undefined')
		{
			if(!hinKB.previouspreviousConsonant)
			{
				displace --; // aa, ai, au.......
				text = vComb;
			}
			else
			{
				displace = 0;
				text = cComb;
			}
			hinKB.isHinLetter=false;
		}
		else
		{
			displace = 0;						
			text = Vowel[key]; 
			hinKB.isHinLetter=false;
		}

		hinKB.pppC=hinKB.previouspreviousConsonant;
		hinKB.previouspreviousConsonant = hinKB.previousConsonant;
		hinKB.previousConsonant = false;
		hinKB.hidden=false;
		break;
	case "e":
	case "i":
	case "o":
	case "u":
	case "A":
	case "I":
	case "U":
	case "O":
	case "E":
		var cComb = GetConsonantCombination(hinKB.prevkey,key);
		var vComb = GetVowelCombination(hinKB.prevkey,key);
		hinKB.pVowel=true;
		hinKB.isHinLetter=false;
		if(hinKB.previousConsonant)
		{
			displace =0;
			text=Consonant[key]; // nothing to append. just remove viram
		}
		else if (typeof(vComb) != 'undefined')
		{
			if(!hinKB.previouspreviousConsonant)
			{
				displace --; // aa, ai, au.......
				text = vComb;
			}
			else
			{
				if(hinKB.prevkey!=key)
				{
					displace = 0;
				}
				else
				{
					displace =displace-1;
				}
				text = cComb ;
			}
		}
		else
		{
			displace = 0;
			text = Vowel[key]; 
		}
		hinKB.pppC=hinKB.previouspreviousConsonant;
		hinKB.previouspreviousConsonant = hinKB.previousConsonant;
		hinKB.previousConsonant = false;
		hinKB.hidden=false;
		break;
	case 'R':
		if(hinKB.previousConsonant)
		{
			displace=0; // replace the viram
			text = Consonant[VRU];
			// here no need for another U in VRU. by detecting VR it is assumed the whole word
		}
		else
		{
			displace=0; // nothing to displace
			text = Vowel[key];
		}
		hinKB.pppC=hinKB.previouspreviousConsonant;
		hinKB.previouspreviousConsonant = hinKB.previousConsonant;
		hinKB.previousConsonant = false;
		hinKB.hidden = false;
		hinKB.prevkey = key;
		hinKB.pVowel=true;
		hinKB.isHinLetter=false;
		break;
	case '~':
		displace = 0;
		text = "~";
		hinKB.pppC=hinKB.previouspreviousConsonant;
		hinKB.previouspreviousConsonant = hinKB.previousConsonant;
		hinKB.previousConsonant = false;
		hinKB.hidden = false;
		prevchar = keychar;
		hinKB.pVowel=true;
		hinKB.isHinLetter=false;
		break;
	case '^':
		if(hinKB.prevkey==126)
		{
			displace -=1;
			text="^";
		}else if(hinKB.previousConsonant)
		{
			text = Consonant[VIRAM]+Consonant[ZWJ] ;
		}
		else if(hinKB.prevkey == key)
		{
			displace -=2;
			text = Consonant[VIRAM]+Consonant[ZWNJ] ;
		}
		else
		{
			text="^";
		}
		hinKB.pppC=hinKB.previouspreviousConsonant;
		hinKB.previouspreviousConsonant = hinKB.previousConsonant;
		hinKB.previousConsonant = false;
		hinKB.hidden = false;
		prevchar = keychar;
		hinKB.isHinLetter=false;
		break;

	case 'M':
		if(hinKB.prevkey!=126)
		{
			displace = 0;
			text = Consonant[key];
		}
		else
		{
			displace -=1;
			text = Consonant[94];
		}
		hinKB.pppC=hinKB.previouspreviousConsonant;
		hinKB.previouspreviousConsonant = hinKB.previousConsonant;
		hinKB.previousConsonant = false;
		hinKB.hidden = false;
		prevchar = hinKB.keychar;
		hinKB.pVowel=true;
		hinKB.isHinLetter=false;
		break;
	case ' ':
		hinKB.pVowel=false;                      
		if(hinKB.prevkey==32)
		{
			return;
		}

		displace = 0;

		text = Symbol[key];
		hinKB.pppC=hinKB.previouspreviousConsonant;
		hinKB.previouspreviousConsonant = hinKB.previousConsonant;
		hinKB.previousConsonant = false;
		hinKB.hidden = false;
		hinKB.ppkey=hinKB.prevkey;
		hinKB.prevkey = key;
		hinKB.isHinLetter=false;
		break;
	default:
		var cComb = GetConsonantCombination(hinKB.prevkey,key);
	hinKB.pVowel=false; 
	hinKB.isHinLetter=false;
	if (hinKB.hidden)
	{
		if(typeof(cComb) !='undefined')
		{
			displace = 0; // because previous word was not shown in textarea.
			if(hinKB.previouspreviousConsonant)
			{
				text = Consonant[VIRAM]+cComb ;//+ Consonant[VIRAM]; // letter + viram
			}
			else
			{
				text = cComb;
			}
			ClearAllParameters(hinKB);
			hinKB.previouspreviousConsonant = false;
			hinKB.pppC=false;
			hinKB.previousConsonant = true;
		}
		else if (typeof(Consonant[key]) !='undefined')
		{
			displace = 0;
			if(hinKB.previousConsonant && !hinKB.previouspreviousConsonant)
			{
				text = Consonant[VIRAM]+Consonant[key] ;//+ Consonant[VIRAM]; // letter + viram
			}
			else
			{
				text = Consonant[key] ;
			}
			ClearAllParameters(hinKB);
			hinKB.pppC=hinKB.previouspreviousConsonant;
			hinKB.previouspreviousConsonant = hinKB.previousConsonant;
			hinKB.previousConsonant = true;
			hinKB.hidden = false;
		}
		else
		{
			displace =0;
			hinKB.pppC=hinKB.previouspreviousConsonant;
			hinKB.previouspreviousConsonant = hinKB.previousConsonant;
			hinKB.previousConsonant = false;
		}
	}
	else
	{
		if(typeof(cComb) !='undefined')
		{
			displace -=1; // for d, dh, D, Dh etc.
			text = cComb;
			ClearAllParameters(hinKB);
			hinKB.pppC=hinKB.previouspreviousConsonant;
			hinKB.previouspreviousConsonant = false;
			hinKB.previousConsonant = true;
		}
		else if(typeof(Consonant[key])!='undefined')
		{
			displace = 0;
			if(hinKB.previousConsonant && !hinKB.previouspreviousConsonant)
			{
				text = Consonant[VIRAM]+Consonant[key] ;//+ Consonant[VIRAM]; // letter + viram
			}
			else
			{
				text = Consonant[key] ;

			}
			ClearAllParameters(hinKB);
			hinKB.pppC=hinKB.previouspreviousConsonant;
			hinKB.previouspreviousConsonant = hinKB.previousConsonant;
			hinKB.previousConsonant = true;
		}
		else if (typeof(Symbol[key]) != 'undefined')
		{
			displace =0;
			text = Symbol[key];
			hinKB.pppC=hinKB.previouspreviousConsonant;
			hinKB.previouspreviousConsonant = hinKB.previousConsonant;
			hinKB.previousConsonant = false;
		}
		else
		{
			hinKB.pppC=hinKB.previouspreviousConsonant;
			hinKB.previouspreviousConsonant = hinKB.previousConsonant;
			hinKB.previousConsonant = true;
			hinKB.hidden = true;
		}

	}
	}
	hinKB.ppkey=hinKB.prevkey;
	hinKB.prevkey = key;


	if(txtarea.setSelectionRange)
	{
		// Mozilla specific
		pos = txtarea.selectionStart;
		var s1 = txtarea.value.substring(0,pos + displace);
		var s2 = txtarea.value.substring(pos, txtarea.value.length);
		var scrollPos = txtarea.scrollTop;
		if(typeof(text) != 'undefined')
			prevpos = pos + displace + text.length;
		else
			prevpos = pos + displace;
		txtarea.value = s1 + text + s2;

		txtarea.scrollTop = scrollPos;
		txtarea.focus();
		txtarea.setSelectionRange(prevpos,prevpos);
	}
	else if (txtarea.createTextRange && txtarea.cursorPos)
	{
		// IE specific
		var range = txtarea.cursorPos;
		range.moveStart('character', displace);
		range.text =	(range.text.charAt(range.text.length - 1)	== ' ' ? text +	' '	: text);
		range.collapse(false);
		range.scrollIntoView(true);
	}
	else
	{
		// Other browser
		if (displace==0)
		{
			txtarea.value += text;
		}
		else
		{
			txtarea.value =	txtarea.value.substring(0, txtarea.value.length-1) + text;
		}
	}
	txtarea.focus();
	hinKB.posChanged=false;
	return false;
}
function processInput(evt,hinKB)
{

	return change(evt,hinKB);
}


/* HinkHoj APIs */
function TextAreaInput()
{
	//parameters
	//Id
	//Name
	//Class
	//Value
	//Size
	//Rows
	//Columns
	//Logo
	//UseGoogle
}

function CreateHindiTextArea(elementId)
{
	//alert("CreateHindiTextArea");
	CreateCustomHindiTextArea(elementId,"",50,3,false);
}
function CreateCustomHindiTextArea(elementId,defaultValue,columns,rows,showHelp)
{
	//alert("CreateCustomHindiTextArea");
	textAreaInpt= new TextAreaInput();
	textAreaInpt.Id=elementId;
	textAreaInpt.Name=elementId;
	textAreaInpt.Value=defaultValue;
	textAreaInpt.Cols=columns;
	textAreaInpt.Rows=rows;
	textAreaInpt.Help=showHelp;
	textAreaInpt.UseHinkhoj=true;
	CreateHindiTextAreaSelectedParam(textAreaInpt);
}

function CreateCustomHindiGTextArea(elementId,defaultValue,columns,rows)
{
	//alert("CreateCustomHindiTextArea");
	textAreaInpt= new TextAreaInput();
	textAreaInpt.Id=elementId;
	textAreaInpt.Name=elementId;
	textAreaInpt.Value=defaultValue;
	textAreaInpt.Cols=columns;
	textAreaInpt.Rows=rows;
	hinTextBoxObj.Help=false;
	hinTextBoxObj.UseHinkhoj=false;
	hinTextBoxObj.Logo=false;
	CreateHindiTextAreaSelectedParam(textAreaInpt);
}

function CreateHindiTextAreaSelectedParam(textAreaParam)
{ 
//	alert("in CreateHindiTextAreaSelectedParam: Id = "+textAreaParam.Id);
	if(textAreaParam.Id==null)
	{
		alert("Error: Id can't be NULL");
		return;
	}
	var awId=textAreaParam.Id+"_awTable";
	var cbId=textAreaParam.Id+"_cbId";
	//alert(awId);
	if(textAreaParam.UseHinkhoj)
	{
		inputBoxIds[inputBoxCount] =GetNewKeyboard(textAreaParam.Id,awId);
	}
	document.write("<textarea ");
	if(textAreaParam.Cols!=null)
	{
		document.write(" cols='"+textAreaParam.Cols+"'" );
	}
	if(textAreaParam.Rows!=null)
	{
		document.write(" rows='"+textAreaParam.Rows+"'" );
	}
	if(textAreaParam.Class!=null)
	{
		document.write(" Class='"+textAreaParam.Class+"'" );
	}
//	alert(textAreaParam.Name);
	if(textAreaParam.Name!=null)
	{
		document.write(" Name='"+textAreaParam.Name+"'" );
	}

	document.write(" id='"+textAreaParam.Id+"' ");
	if(textAreaParam.UseHinkhoj)
	{
		document.write(" onkeypress='if (!inputBoxIds["+inputBoxCount+"].isEng){ return processInput(event,inputBoxIds["+inputBoxCount+"]);} else {return true;}' onKeyUp='changeCursor(this);' onkeydown='positionChange(event,inputBoxIds["+inputBoxCount+"]);' onFocus='changeCursor(this);' onClick='changeCursor(this);'");
	}
	document.write(" >");


	if(textAreaParam.Value!=null)
	{
		//alert(textAreaParam.Value);
		document.write(textAreaParam.Value);
	}
	document.write("</textarea>");
	if(!textAreaParam.UseHinkhoj)
	{
		document.write('<input type="checkbox" id="'+cbId+'" onclick="javascript:checkboxClickHandler(\''+cbId+'\')" checked>Hindi-[<font color="green">Use <b>ALT-k</b> to change langauge</font>]</input>');
	}
	if(textAreaParam.Help!=null && textAreaParam.Help)
	{
		
		divSuggestBox = document.createElement('div');
		divSuggestBox.setAttribute('id','translated_sentence_awId' ); 
		divSuggestBox.setAttribute('border','0' );
		divSuggestBox.setAttribute('class','awDiv' );  
		divSuggestBox.innerHTML = "<center><table width='100%' id='"+awId+"' border='0' class='awDiv'></table></center>";
		document.getElementById("suggest").appendChild(divSuggestBox);
	}
	if(textAreaParam.UseHinkhoj)
	{
		inputBoxCount++;
	}
}
// CODE FOR AUTO-CORRECTION IN TRANSLITERATOR STARTS HERE
var find_word;
function getOption(find){
		var textnode ="";
		var left = 60; //left coordinate of input box relative to its parent element.
		var top = 35; //top coordinate of input box relative to its parent element.
		var numLines=0;
		var max = 0;
		find_word = find;
	
		req_url = '/account/translate/autocorrect/'+find;
		
		$.get(req_url, function(data){
			var lines = new Array();
			lines = data.split(' ');	
			lists = lines;
			
			for(i in lines) {
				numLines += parseInt((lines[i].length)/42); //42 characters in one line.
				if (parseInt(lines[i].length) > max) {
					max = parseInt(lines[i].length);
				}
			}
			max = max*10;
			numLines += lines.length;
			
			var element = document.getElementById("translated_sentence")
			var pos = GetCaretPosition(element);
			
			if (pos > 67) {
				pos = pos/67;
			}
			left += 450; //8 pixels horizontoly for one character
			top += (numLines*10) + 80; //approx height of line in pixels.
			left += pos;
		
			dict = document.createElement("div");
			dict.setAttribute('id',"autocorrect");
			dict.setAttribute('class',"autocorrectclass");
			dict.style.left = left + "px";
			dict.style.top = top + "px";
			dict.style.width = max + "px";
			 
		
			document.getElementById("translate").appendChild(dict);
			
			for(i in lines) {
				divSuggestWrd = document.createElement('div');
				divSuggestWrd.setAttribute('id', "div" + lines[i]);
				divSuggestWrd.setAttribute('class','divWord');
				divSuggestWrd.onmouseover = HandleMouseOverDivAutoCorrect;
 				divSuggestWrd.onclick = HandleClickOnDivAutoCorrect;
				
				aSuggestWrd = document.createElement('a');
				aSuggestWrd.setAttribute('id',lines[i]);
				aSuggestWrd.setAttribute('class','suggestWord');
				aSuggestWrd.setAttribute('href',"");
 				aSuggestWrd.onmouseover = HandleMouseOverAAutoCorrect;
 				aSuggestWrd.onkeydown = SuggestionKeyDownAutoCorrect;
 				aSuggestWrd.onfocus = HighlightAutoCorrect;
				textNode = document.createTextNode(lines[i]);
				
				aSuggestWrd.appendChild(textNode);
				divSuggestWrd.appendChild(aSuggestWrd);
				dict.appendChild(divSuggestWrd);
			}
		});
	}

function HandleClickOnDivAutoCorrect(){
	//id is divXYZ, we want XYZ which is the id of < a > element which is main for us.
	var id = document.getElementById(((this.id).substring(3))).id;
	//complete word when user clicks on it.
	CompleteAutoCorrect(id, find_word);
	return false;
}
	
function HandleMouseOverAAutoCorrect() {
	this.focus();
}
function HandleMouseOverDivAutoCorrect() {
	document.getElementById((this.id).substring(3)).focus();
}	
	
function SuggestionKeyDownAutoCorrect(event) {
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
		var divSuggestBox = document.getElementById("suggest");
		if(divSuggestBox != null ) {
			document.getElementById("translate").removeChild(divSuggestBox);
		}
		document.getElementById("input").focus();
		gEscapePressed = 1;
	}
	else if(keyCode == 13 || keyCode == 9) { //13 = Enter, 9 = TAB
		CompleteAutoCorrect(this, document.getElementById("translated_sentence"));
		return false;
	}
	else if(keyCode == 32) { //32 = space
		CompleteAutoCorrect(this, document.getElementById("translated_sentence"));
	}
	else if(keyCode == 38 || keyCode == 40) { //38=Up Key, 40 = Down Key
		for(i in gSuggestions) {
			document.getElementById(lists[i]).setAttribute('class', 'suggestWord');
		}
		for(i in lists) {
			selected++;
			if(lists[i] == this.id) {
				break;
			}
		}
		if(keyCode == 38) {
			selected--;
			if(selected == -1) {
				selected = lists.length - 1;
			}
		}
		else if(keyCode == 40) {
			selected++;
			if (selected == lists.length) {
					selected = 0;
			}				
		}
		document.getElementById(lists[selected]).focus();
		return false;
	}
	
}
	
function CompleteAutoCorrect(id, source) {
	$('#autocorrect').remove();
	var text1 = document.getElementById("translated_sentence").value;
	var text = "";
	
	var word = text1.split(' ');
	
	$(function() {	
		for (i = 0; i < word.length; i++) {
			
		    if (word[i]==source)
		    {	
		        word[i] = id;
		    }
		    text = text + word[i] + ' ';
		}
	});

	document.getElementById("translated_sentence").value = text;
	$('#autocorrect').remove();
}

function HighlightAutoCorrect(){
	for(i in lists) {
		document.getElementById(lists[i]).setAttribute('class', 'suggestWord');
		document.getElementById("div" + lists[i]).setAttribute('class', 'divWord');
	}
	this.setAttribute('class', 'suggestWordHighlight');
	document.getElementById("div" + this.id).setAttribute('class', 'divWordHighlight');
}

// CODE FOR AUTO-CORRECTION IN TRANSLITERATOR ENDS HERE