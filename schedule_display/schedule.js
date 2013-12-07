// Initialize "global" variables
var columns, rows, canvasClickHandler, canvasW, canvasH, pad, cellW, cellH, canvas, context, schedStartTime, schedEndTime, weekdays, classes, gridText, fontHeight, pillStyle, backgroundColor;

function initializeCanvas(canvasSelector, timesStart, timesEnd, clickHandler) {
	// Initialize drawing objects
	canvas = canvasSelector; // must be the jquery selector object, i.e.: $("#schedule")
	context = canvas.get(0).getContext("2d");

	// Styling
	fontHeight = 12;
	//pillStyle = "rgba(172, 209, 233, 0.5)";
	pillStyle = "rgba(109, 146, 155, 0.5)";
	//pillStyle = "rgba(232, 208, 169, 0.5)";
	backgroundColor = "rgb(245, 250, 250)";

	// Fill with the background color
	context.fillStyle = backgroundColor;
	context.fillRect(0, 0, canvas[0].width, canvas[0].height)
	context.fillStyle = "black";

	// Initialize a bunch of crap
	columns = 1+5; // time column + days of the week
	rows = timesEnd[0] - timesStart[0] + 2;
	canvasClickHandler = clickHandler;
	canvasW = canvas[0].width;
	canvasH = canvas[0].height;
	pad = 10;
	cellW = Math.floor((canvasW - (2 * pad)) / columns);
	cellH = Math.floor((canvasH - (2 * pad)) / rows);
	schedStartTime = timesStart; // [h, m]
	schedEndTime = timesEnd;
	weekdays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"];
	classes = [];
	gridText = [];
	for (var i = 0; i < rows; i++) {
		gridText[i] = [];
		for (var j = 0; j < columns; j++) {
			gridText[i][j] = "";
		}
	}

	// Event listeners
	canvas.click(function(e) {
		xyCoords = getCursorPosition(e);
		ijCoords = [yToI(xyCoords[1]), xToJ(xyCoords[0])];
		classInfo = findClassInXY(xyCoords);

		// Send to real handler
		clickInfo = new Object();
		clickInfo.xyCoords = xyCoords; 
		clickInfo.ijCoords = ijCoords;
		clickInfo.classInfo = classInfo;
		canvasClickHandler(clickInfo);
	});

	canvas.mousemove(function(e) {
		xyCoords = getCursorPosition(e);
		classInfo = findClassInXY(xyCoords);
		document.body.style.cursor = (classInfo ? "pointer" : "default");
	});

	// Draw skeleton of schedule
	drawGrid();

	// Draw starting schedule
	addWeekdays();
	addTimes();
}

//////////////////////////////////
// Utility functions
function iToY(i) {
	return pad + i * cellH + 1;
}

function jToX(j){
	return pad + j * cellW + 1;
}

function xToJ(x){
	return Math.floor((x - pad)/cellW);
}

function yToI(y){
	return Math.floor((y - pad)/cellH);
}

function getCursorPosition(e) {
	// From: http://diveintohtml5.info/canvas.html
	var x;
	var y;
	if (e.pageX != undefined && e.pageY != undefined) {
		x = e.pageX;
		y = e.pageY;
	}
	else {
		x = e.clientX + document.body.scrollLeft +
				document.documentElement.scrollLeft;
		y = e.clientY + document.body.scrollTop +
				document.documentElement.scrollTop;
	}

	x -= canvas.offset()["left"];
	y -= canvas.offset()["top"];

	return [x, y];
}

//////////////////////////////////
// Drawing functions
function drawGrid(){
	// vert lines
	for (var x = 0.5 + pad; x <= canvasW - pad; x += cellW) {
		//colX = 0.5 + x + p;
		startY = 0.5 + pad;
		stopY = 0.5 + pad + rows * cellH;
		context.moveTo(x, startY);
		context.lineTo(x, stopY);
	}

	// horz lines
	for (var y = 0.5 + pad; y <= canvasH - pad; y += cellH) {
		rowY = 0.5 + y + pad;
		startX = 0.5 + pad;
		stopX = 0.5 + pad + columns * cellW;
		context.moveTo(startX, y);
		context.lineTo(stopX, y);
	}

	context.strokeStyle = "black";
	context.stroke();
}

function drawTextInCell(i, j, text, center){
	// http://diveintohtml5.info/canvas.html#text
	var x = jToX(j);
	var y = iToY(i);

	context.textAlign = (center ? "center":"start");
	context.textBaseline = "top";
	context.font = "bold "+fontHeight+"px Arial";

	//var metrics = context.measureText(text);
	var lines = text.split("\n");
	x += (center ? cellW/2:0);
	y += (center ? cellH/2-lines.length*fontHeight/2:0);
	for (var i = 0; i < lines.length; i++) {
		context.fillText(lines[i], x, y);
		y += fontHeight;
	}
}

function drawTextXY(x, y, text, hcenter, vcenter, shadow) {
	context.textAlign = (hcenter ? "center":"start");
	context.textBaseline = "top";
	context.font = "bold "+fontHeight+"px Arial";
	if (shadow) {
		oldShadow = context.shadowBlur;
		oldFillStyle = context.fillStyle;
		context.fillStyle = "white";
		context.shadowBlur = 5;
	}

	var lines = text.split("\n");
	y += (vcenter ? -lines.length*fontHeight/2:0)
	for (var i = 0; i < lines.length; i++) {
		context.fillText(lines[i], x, y);
		y += fontHeight;
	}

	if (shadow) {
		context.fillStyle = oldFillStyle;
		context.shadowBlur = oldShadow;
	}
}

function drawRoundRect(x, y, width, height, radius, fill, stroke) {
	if (typeof stroke == "undefined" ) {
		stroke = true;
	}
	if (typeof radius === "undefined") {
		radius = 5;
	}
	context.beginPath();
	context.moveTo(x + radius, y);
	context.lineTo(x + width - radius, y);
	context.quadraticCurveTo(x + width, y, x + width, y + radius);
	context.lineTo(x + width, y + height - radius);
	context.quadraticCurveTo(x + width, y + height, x + width - radius, y + height);
	context.lineTo(x + radius, y + height);
	context.quadraticCurveTo(x, y + height, x, y + height - radius);
	context.lineTo(x, y + radius);
	context.quadraticCurveTo(x, y, x + radius, y);
	context.closePath();
	if (stroke) {
		context.stroke();
	}
	if (fill) {
		oldFillStyle = context.fillStyle;
		context.shadowBlur = 5;
		context.shadowOffsetX = 1;
		context.shadowOffsetY = 1;
		context.shadowColor = "black";
		context.fillStyle = fill;
		context.fill();
		context.shadowOffsetX = 0;
		context.shadowOffsetY = 0;
		context.shadowBlur = 0;
		context.fillStyle = oldFillStyle;
	}     
}

function screenshot() {
	return canvas[0].toDataURL('image/png');
}

///////////////////////////////////
// Schedule drawing

// Update function -- call this to redraw all the text in gridText!
function drawGridText() {
	for (var i = 0; i < gridText.length; i++) {
		for (var j = 0; j < gridText[i].length; j++) {
			drawTextInCell(i, j, gridText[i][j], true);
		}
	}
}

function drawCellText(i, j) {
	drawTextInCell(i, j, gridText[i][j], true);
}

function timeToI(time) {
	return 1 + time[0] - schedStartTime[0];
}

function timeToY(time) {
	return iToY(timeToI(time)) + cellH * time[1]/60;
}

function timeToStr(time) {
	var hour = time[0];
	var minute = time[1];
	return (hour <= 12 ? hour:hour%12) + ":" + (minute < 10 ? "0"+minute:minute) + (hour < 12 ? "am":"pm");
}

function dayToJ(day) {
	return 1+weekdays.indexOf(day.charAt(0).toUpperCase() + day.substr(1).toLowerCase());
}

function dayToX(day) {
	return jToX(dayToJ(day));
}

function addWeekdays() {
	var i = 0; // first row
	for (var j = 1; j <= weekdays.length; j++) {
		gridText[i][j] = weekdays[j - 1];
		drawCellText(i,j);
	}
}

function addTimes() {
	var j = 0;
	for (var i = 1; i <= 1+(schedEndTime[0] - schedStartTime[0]); i++) {
		var hour = (schedStartTime[0] - 1 + i);
		var minute = 0;
		gridText[i][j] = (hour <= 12 ? hour:hour%12) + ":" + (minute < 10 ? "0"+minute:minute) + (hour < 12 ? "am":"pm");
		drawCellText(i,j);
	}
}

function addClass(classStartTime, classEndTime, day, title, uid) {
	// Draw background pill
	var pillX = dayToX(day) + 2;
	var pillY = timeToY(classStartTime);
	var pillW = cellW - 5;
	var pillH = timeToY(classEndTime)-timeToY(classStartTime);
	drawRoundRect(pillX, pillY, pillW, pillH, 5, pillStyle);
	
	// Draw text
	var text = title+"\n"+timeToStr(classStartTime)+" - "+timeToStr(classEndTime);
	var textX = pillX + pillW / 2;
	var textY = pillY + pillH / 2;
	drawTextXY(textX,textY,text,true,true,true);

	// Keep track of these guys
	classObj = new Object();
	classObj.startTime = classStartTime;
	classObj.endTime = classEndTime;
	classObj.day = day;
	classObj.title = title;
	classObj.xRange = [pillX, pillX+pillW];
	classObj.yRange = [pillY,pillY+pillH];
	classObj.uid = uid;
	classes.push(classObj);
}

function removeClass(uid) {
	// Clear canvas
	context.fillStyle = backgroundColor;
	context.fillRect(0, 0, canvas[0].width, canvas[0].height)
	context.fillStyle = "black";

	// Draw skeleton of schedule
	drawGrid();

	// Draw starting schedule
	addWeekdays();
	addTimes();

	// Remove class
	for (var i = classes.length-1; i >= 0; i--) {
		if (classes[i].uid == uid) {
			classes.splice(i, 1);
		}
	}

	for (var i = 0; i < classes.length; i++) {
		var classStartTime = classes[i].startTime;
		var classEndTime = classes[i].endTime;
		var day = classes[i].day;
		var title = classes[i].title;
		var uid = classes[i].uid;

		// Draw background pill
		var pillX = dayToX(day) + 2;
		var pillY = timeToY(classStartTime);
		var pillW = cellW - 5;
		var pillH = timeToY(classEndTime)-timeToY(classStartTime);
		drawRoundRect(pillX, pillY, pillW, pillH, 5, pillStyle);
		
		// Draw text
		var text = title+"\n"+timeToStr(classStartTime)+" - "+timeToStr(classEndTime);
		var textX = pillX + pillW / 2;
		var textY = pillY + pillH / 2;
		drawTextXY(textX,textY,text,true,true,true);
	}
}

function clearCanvas() {
	// Clear canvas
	context.fillStyle = backgroundColor;
	context.fillRect(0, 0, canvas[0].width, canvas[0].height)
	context.fillStyle = "black";

	// Draw skeleton of schedule
	drawGrid();

	// Draw starting schedule
	addWeekdays();
	addTimes();

	// Clear classes
	classes = [];
	gridText = [];
	for (var i = 0; i < rows; i++) {
		gridText[i] = [];
		for (var j = 0; j < columns; j++) {
			gridText[i][j] = "";
		}
	}
}

function findClassInXY(xyCoords) {
	x = xyCoords[0];
	y = xyCoords[1];

	for (var i = 0; i < classes.length; i++) {
		if (
			x >= classes[i].xRange[0] &&
			x <= classes[i].xRange[1] &&
			y >= classes[i].yRange[0] &&
			y <= classes[i].yRange[1]
			) {
			return classes[i];
		}
	}
	return null;
}

