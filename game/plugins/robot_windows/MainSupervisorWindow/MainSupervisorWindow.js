/*
MainSupervisorWindow.js v2

Changelog:
 - Added human loaded indicator
*/


//The total time at the start
var maxTime = 8 * 60;

var visable = false;

var robot0Name = "Robot 0";
var robot1Name = "Robot 1";

var scores = [0,0];

const stream = "21";
const version = "21.0.0 Beta-2";
const unreleased = true;

function receive (message){
	//Receive message from the python supervisor
	//Split on comma
	var parts = message.split(",");

	//If there is a message
	if (parts.length > 0){			
		switch (parts[0]){
			case "startup":
				//Call for set up the robot window
				startup();
				break;
			case "update":
				//Update the information on the robot window every frame (of game time)
				update(parts.slice(1,parts.length + 1));
				break;
			case "config":
				//Load config data from world
				updateConfig(parts.slice(1,parts.length + 1));
				break;
			case "unloaded0":
				//Robot 0's controller has been unloaded
				unloadedController(0);
				break;
			case "unloaded1":
				//Robot 1's controller has been unloaded
				unloadedController(1);
				break;
			case "ended":
				//The game is over
				endGame();
				break;
			case "humanLoaded0":
				//Robot 0's human is loaded
				humanLoadedColour(0);
				break;
			case "humanUnloaded0":
				//Robot 0's human is unloaded
				humanUnloadedColour(0);
				break;
			case "humanLoaded1":
				//Robot 1's human is loaded
				humanLoadedColour(1);
				break;
			case "humanUnloaded1":
				//Robot 1's human is unloaded
				humanUnloadedColour(1);
				break;
			case "activityLoaded0":
				activityLoadedColor(0,parts[1],parts[2],parts[3])
				break;
			case "activityUnloaded0":
				activityUnloadedColour(0)
				break;
			case "activityLoaded1":
				activityLoadedColor(1,parts[1],parts[2],parts[3])
				break;
			case "activityUnloaded1":
				activityUnloadedColour(1)
				break;
			case "historyUpdate":
				let msg = message.split(":");
				let history0 = msg[0].split(",").slice(1,msg[0].length-1)
				updateHistory(history0)
				break;
			case "robotInSimulation0":
				robotQuitColour(0);
				break;
			case "robotInSimulation1":
				robotQuitColour(1);
				break;
			case "robotNotInSimulation0":
				robotQuitUnavailableColour(0);
				break;
			case "robotNotInSimulation1":
				robotQuitUnavailableColour(1);
				break;
		}
	}
}

function robotQuitColour(id){
	// setEnableButton('quit'+id, true)
	// setEnableButton('relocate'+id, true)
	// setEnableButton('load'+id, true)
	// setEnableButton('unload'+id, true)
}
function robotQuitUnavailableColour(id){
	// setEnableButton('quit'+id, false)
	// setEnableButton('relocate'+id, false)
	// setEnableButton('load'+id, false)
	// setEnableButton('unload'+id, false)
}

function humanLoadedColour(id){
	// Changes svg human indicator to gold to indicate a human is loaded
	document.getElementById("human"+id+"a").style.stroke = "#edae39";
	document.getElementById("human"+id+"b").style.stroke = "#edae39";
}
function humanUnloadedColour(id){
	// Changes svg human indicator to black to indicate a human is unloaded
	document.getElementById("human"+id+"a").style.stroke = "black";
	document.getElementById("human"+id+"b").style.stroke = "black";
}

function activityLoadedColor(id,r,g,b){
	document.getElementById("activity"+id).style.stroke = "rgb("+(Number(r)*255).toString()+","+(Number(g)*255).toString()+", "+(Number(b)*255).toString()+")";
}
function activityUnloadedColour(id){
	document.getElementById("activity"+id).style.stroke = "black";
}
function updateHistory(history0){
	let text = ""


	let history0End = false;
	// let history1End = false;

	let i = history0.length -1;
	// let j = history1.length -1;


	while(!history0End){
		text += "<tr id='historyrow'>";
		if(history0[i] != null){
			if(history0[i].indexOf("+") != -1){
				text += "<div class='outerDiv'><div class='innerDiv'><td id='historyrowtext' style='font-size:18px;color:#2980b9;'>"+history0[i]+"</td></div></div>";
			}else if(history0[i].indexOf("-") != -1){
				text += "<div class='outerDiv'><div class='innerDiv'><td id='historyrowtext' style='font-size:18px;color:#c0392b;'>"+history0[i]+"</td></div></div>";
			}else{
				text += "<div class='outerDiv'><div class='innerDiv'><td id='historyrowtext' style='font-size:18px;color:#2c3e50;'>"+history0[i]+"</td></div></div>";
			}

			i--;
		}else{
			text += "<div class='outerDiv'><div class='innerDiv'><td id='historyrowtext'></td></div></div>"
			history0End = true;
		}
		text += "</tr>";
	}
	document.getElementById("history").innerHTML = text;
}

function loadedController(id){
	//A controller has been loaded into a robot id is 0 or 1 and name is the name of the robot
	//Set name and toggle to unload button for robot 0
	document.getElementById("load"+ id).style.display = "none";
	document.getElementById("unload"+ id).style.display = "inline-block";
}

function unloadedController(id){
	//A controller has been unloaded for robot of the given id
	//Reset name and toggle to load button for robot 0
	document.getElementById("robot"+ id +"Controller").value = "";
	document.getElementById("unload"+ id).style.display = "none";
	document.getElementById("load"+ id).style.display = "inline-block";
}

function startup (){
	//Turn on the run button and reset button when the program has loaded
	setEnableButton("runButton", true);
	setEnableButton("pauseButton", false);

	// setEnableButton('quit0', false)
	setEnableButton('relocate0', false)

	setEnableButton("load0", true);
	setEnableButton("unload0", true);
}

function update (data){
	//Update the ui each frame of the simulation
	//Sets the scores and the timer
	document.getElementById("score0").innerHTML = String(data[0]);

	scores = [data[0],0]

	maxTime = data[2]
	document.getElementById("timer").innerHTML = calculateTimeRemaining(data[1]);
}

function updateConfig (data){
	//Update the config ui
	document.getElementById("autoRemoveFiles").checked = Boolean(Number(data[0]));
	document.getElementById("autoLoP").checked = Boolean(Number(data[1]));
}

function configChanged(){
	let data = [0,0];
	data[0] = String(Number(document.getElementById("autoRemoveFiles").checked));
	data[1] = String(Number(document.getElementById("autoLoP").checked));
	window.robotWindow.send(`config,${data.join(',')}`);
}

function calculateTimeRemaining(done){
	//Create the string for the time remaining (mm:ss) given the amount of time elapsed
	//Convert to an integer
	done = Math.floor(done);
	//Calculate number of seconds remaining
	var remaining = maxTime - done;
	//Calculate seconds part of the time
	var seconds = Math.floor(remaining % 60);
	//Calculate the minutes part of the time
	var mins = Math.floor((remaining - seconds) / 60);
	//Convert parts to strings
	mins = String(mins)
	seconds = String(seconds)

	//Add leading 0s if necessary
	for (var i = 0; i < 2 - seconds.length; i++){
		seconds = "0" + seconds;
	}

	for (var i = 0; i < 2 - mins.length ; i++){
		mins = "0" + mins;
	}

	//Return the time string
	return mins + ":" + seconds;
}

function runPressed(){
	//Disable all the loading buttons (cannot change loaded controllers once simulation starts)
	setEnableButton("load0", false);
	setEnableButton("unload0", false);
	
	setEnableButton("load1", false);
	setEnableButton("unload1", false);
	//When the run button is pressed
	//Disable the run button
	setEnableButton("runButton", false);
	//Send a run command
	//Enable the pause button
	setEnableButton("pauseButton", true);
	
	// setEnableButton('quit0', true)
	setEnableButton('relocate0', true)
	window.robotWindow.send("run");
}

function pausePressed(){
	//When the pause button is pressed
	//Turn off pause button, on run button and send signal to pause
	setEnableButton("pauseButton", false);
	setEnableButton("runButton", true);
	window.robotWindow.send("pause");
}

function resetPressed(){
	//When the reset button is pressed
	//Disable all buttons
	setEnableButton("runButton", false)
	setEnableButton("pauseButton", false);
	//Send signal to reset everything
	window.robotWindow.send("reset");
}

function openLoadController(id){
	//When a load button is pressed - opens the file explorer window
	document.getElementById("robot"+id+"Controller").click();
}

function setEnableButton(name, state){
	//Set the disabled state of a button (state is if it is enabled as a boolean)
	document.getElementById(name).disabled = !state;
}

//Set the onload command for the window
window.onload = function(){
	//Connect the window
	window.robotWindow = webots.window();
	//Set the title
	window.robotWindow.setTitle('Simulation Controls');
	//Set which function handles the recieved messages
	window.robotWindow.receive = receive;
	//Set timer to inital time value
	document.getElementById("timer").innerHTML = '--:--'
	//Set version info
	document.getElementById("versionInfo").innerHTML = "Ver. " + version;
	//Check update
	checkUpdate();
};

function checkUpdate(){
	if(unreleased){
		document.getElementById("versionInfo").style.color = "#e67e22";
		document.getElementById("versionInfo").innerHTML = `Ver. ${version} (Unreleased)`;
		return;
	}
	$.ajax({
		url: 'https://gitlab.com/api/v4/projects/22054848/releases',
		dataType: 'json',
		success: function(data){
			let versions = data.filter(release => release['tag_name'].startsWith(`v${stream}`));
			if(versions.length == 0) return;
			if(versions[0]['tag_name'].replace(/_/g, ' ') === `v${version}`){
				//Latest
				document.getElementById("versionInfo").style.color = "#27ae60";
				document.getElementById("versionInfo").innerHTML = `Ver. ${version} (Latest)`;
			}else{
				document.getElementById("versionInfo").style.color = "#c0392b";
				document.getElementById("versionInfo").innerHTML = `Ver. ${version} (Outdated)`;
				document.getElementById("newVersion").innerHTML = `New version: ${versions[0]['tag_name'].replace(/_/g, ' ')} is available. Please update it!`;
			}
		}
	});
	
}

function endGame(){
	//Once the game is over turn off both the run and pause buttons
	setEnableButton("runButton", false)
	setEnableButton("pauseButton", false);
}

function unloadPressed(id){
	//Unload button pressed
	//Send the signal for an unload for the correct robot
	window.robotWindow.send("robot"+id+"Unload");
}

function fileOpened(filesId, acceptTypes, location, id){
	//When file 0 value is changed
	//Get the files
	var files = document.getElementById(filesId).files;

	//If there are files
	if (files.length > 0){
		//Get the first file only
		var file = files[0];
		//Split at the .
		var nameParts = file.name.split(".");

		//If there are parts to the name
		if (nameParts.length > 1){
			//If the last part is "py" - a python file
			if(acceptTypes.indexOf(nameParts[nameParts.length - 1]) != -1 ){
				const fd = new FormData();
				for (let i = 0; i < files.length; i++) {
					const f = files[i];
					fd.append(`file${(i+1)}`, f, f.name);
				}

				let xmlhttp = new XMLHttpRequest();
				xmlhttp.onreadystatechange = function () {
					if (xmlhttp.readyState == 4 && xmlhttp.status != 200) {
						console.log(xmlhttp.status);
						alert(xmlhttp.responseText);
					}
					if (xmlhttp.readyState == 4 && xmlhttp.status == 200) {
						loadedController(id);
					}
				};
				xmlhttp.open("POST", "http://127.0.0.1:60520/"+location+"/", true);
				xmlhttp.send(fd);

			}else{
				//Tell the user to select a program
				alert("Please select your controller program.1");
			}
		}else{
			//Tell the user to select a program
			alert("Please select your controller program.");
		}

	}
}

function openJsonFile(){
	//When file 0 value is changed
	//Get the files
	var files = document.getElementById("robot1Controller").files;
	
	//If there are files
	if (files.length > 0){
		//Get the first file only
		var file = files.item(0);
		//Split at the .
		var nameParts = file.name.split(".");
		
		//If there are parts to the name
		if (nameParts.length > 1){
			//If the last part is "json" - a json file
			if(nameParts[nameParts.length - 1] == "json"){
				//Create a file reader
				var reader = new FileReader();
				
				//Set the function of the reader when it finishes loading
				reader.onload = (function(reader){
					return function(){
						//Send the signal to the supervisor with the data from the file
						window.robotWindow.send("robotJson," + reader.result);
						loadedController(1)
					}
				})(reader);
				
				//Read the file as udf-8 text
				reader.readAsText(file);
			}else{
				//Tell the user to select a json file
				alert("Please select a json file.");
			}
		}else{
			//Tell the user to select a json file
			alert("Please select a json file.");
		}
		
	}
}

function hide_winning_screen(){
	//Disable winner screen
	document.getElementById("winning-screen").style.display = "none";
}

function calculateWinner(name0,name1){
	//if scores are the same
	if (scores[0] == scores[1]){
		//Show draw text
		document.getElementById("winning-team").innerHTML = "Draw!"
	}else {
		//Find index of highest scoring team

		if (scores[0] > scores[1]){
			//Show robot 0 win text
			document.getElementById("winning-team").innerHTML = name0 + " wins!"
		} else {
			//Show robot 1 win text
			document.getElementById("winning-team").innerHTML = name1 + " wins!"
		}
	}

}

function show_winning_screen(){
	calculateWinner(robot0Name,robot1Name);
	//Show winning screen
  	document.getElementById("winning-screen").style.display = "inline-block";
  	visable = true;
}

function relocate(id){
	window.robotWindow.send("relocate,"+id.toString());
}

function quit(id){
	unloadPressed(id);
	window.robotWindow.send("quit,"+id.toString());
}