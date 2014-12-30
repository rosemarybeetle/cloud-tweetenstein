/* --------------------------------------
-----------------------------------------
Andrew Lewis 2014
Canvas visualiser script to ingest tweet data and turn it into something else
v.1 31 Jan 2014 - test
github
*/

/* -------------
if (Modernizr.canvas) {
   console.log ("let's draw some shapes!")
} else {
   console.log("no native canvas support available :( ")
}
Optional test script to identify any elements (and handle them if necessary
------------------*/
function speakTest(speech)
{
//speech=screenames[ran];
console.log('test alert')
//var gurl= Trim('http://translate.google.com/translate_tts?ie=UTF-8&q='+speech);
console.log(speech);
//console.log(gurl);
document.getElementById('framer').src = 'http://translate.google.com/translate_tts?&tl=en-US&ie=UTF-8&q='+speech;

}
function screenSize()
{
window.W=document.body.clientWidth;
window.H=document.body.clientHeight;
}
//-------------------------------Set Up------------------------
function yep() {
 console.log ('yep');
}
function loadLastTweet ()
{
$.getJSON( "lastTweet.json", function( data ) {
 console.log('start lastTweet');
  //console.log(data.lasttweetID);
  window.lasttweetID=data.lasttweetID;
  console.log(lasttweetID);
  console.log('Success from inside getJson call to lastTweet.json');
 });
}
function mouthoff(le)
{
window.mouthy.src="images/faces/1/MOUTH-2.jpg";
}
function harvestTweets ()
{
console.log('start harvestTweets');

$.getJSON( "tweetstore2.json", function(adata) {
console.log('l = '+adata.store.length);
l=adata.store.length; // set max 'l' based on length of imported array

$.each( adata.store, function(key,val) {
	console.log('key= '+key,val.username,val.screen_name);
	usernames.push (val.username);
	screenames.push (val.screen_name);
	tweetText.push (val.tweet_text);

	
	
	
  }  );
  
  console.log(usernames);
  console.log(screenames);
	console.log('wtf')
    //console.log(adata[i].username);
//for ( var i = 0; i < l; i++ ) {
//}

console.log('inside harvestTweets call to tweetstore.json');
 /*
 $.each( data, function() {
    console.log(data.username)
	//twitems.push( username, tweet_id );
  });
  console.log('twitems'+twitems);
  */
 });
 
}
function setUp() {

/* optional checking for html5 file apis, needed to read data
if (window.File && window.FileReader && window.FileList && window.Blob) {
  console.log("Yay - The File APIs are supported by your browser.")
} else {
  console.log('The File APIs are not fully supported by your browser.');
}*/
// +++
$( document ).ready(function() {
speakTest('hello there');
console.log ('Start setUp initialisation...');

window.l= 0;// used later to store array length
window.usernames = [];
window.screenames = [];
window.tweetText =[];
loadLastTweet ();

harvestTweets ();

// +++
console.log ("Hello, Tweetenstein.js...");
try {

screenSize();

myCanvas.width=W;
myCanvas.height = H;
myCanvas2.width=W;
myCanvas2.height = H;
var ctxt=document.getElementById("myCanvas");
window.txt=ctxt.getContext("2d");
window.fontDef="20px Arial";
txt.font=fontDef;
var ctxt2=document.getElementById("myCanvas2");
window.txt2=ctxt2.getContext("2d");
window.fontDef2="30px Arial";
txt2.font=fontDef2;
console.log('setUp complete!!!');
}
catch (e) { console.log("FAIL"+e)};
}
	);
}
// -------------------------------end setup ---------------------


function plotLoop(txty){
// this is grabbing users' details and randomly writing them to the sreen
screenSize();
window.xx=Math.random(1)*W-35;//initialise random x position variable;
window.yy=Math.random(1)*H;//initialise random y position variable;
window.xx2=Math.random(1)*W-35;//initialise random x position variable;
window.yy2=Math.random(1)*H;//initialise random y position variable;
txt.fillStyle="#000033";
txt2.fillStyle="purple";
//txt.fillText(txty,xx,yy);
ran= Math.floor((Math.random()*l)+1);
console.log ('random number = '+ran)
//txt.fillText(lasttweetID,xx,yy);
// txt.fillText(screenames[ran],xx,yy); // temp disabled ########
txt.fillText(tweetText[ran],xx2,yy2+30)
txt2.fillText(screenames[ran],xx2,yy2);
//
//

}
function plotPulse() {
myCanvas.width=W;
myCanvas.height=H;
txt.font=fontDef;
window.fontDef="20px Arial";
}
function plotPulse2 () {
myCanvas2.width=W;
myCanvas2.height=H;
window.fontDef2="30px Arial";
txt2.font=fontDef2;
}
// speed of text draw
window.phi=100;
// speed of pulse
window.phi2=4000;
window.phi3=3500;
window.phi4=500;
window.txty="Hello World...";
$( document ).ready(function() {
console.log ('document ready from intervals');
setInterval(function(){plotPulse()},phi2); //redraws a backgound to make the text visible
setInterval(function(){plotPulse2()},phi3); //redraws a backgound to make the text visible
setInterval(function(){harvestTweets()}, phi4); // check for changes
setInterval(function(){plotLoop(txty)},phi); // fires out text at rate set by period: phi
//setInterval(function(){speakTest("hello")}, phi2); // check for changes


});
window.onkeyup = keyup;
function keyup()
{
console.log('inside keyup detection ');
window.g=screenames[ran];
speakTest(g);
 
}