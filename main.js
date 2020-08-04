var canvas = document.getElementById('myCanvas');
var modeButtons = document.getElementsByName('mode');
var normalisationButtons = document.getElementsByName('normalisation');
var colourmapButtons = document.getElementsByName('colourmap');
var context = canvas.getContext('2d');

var minimap = document.getElementById('minimap');
var minimapContext = minimap.getContext('2d');

var selectRectCoords = [0,0,0,0];
var mousedown = false;
var shiftFrom= 0;
var isSeriesBrushed = [];

var seriesCount = 100;
var seriesLength = 100;
var labels = [];
let allData = [] // stores data in single flat array, rather than in an array of arrays
var data = new Array(seriesCount);
var dataImage = new Image;
var dataImageStale = true;

var normalise = percentile; // points to the current normalisation function being used
var colourmap = viridisColorString; // current colour map being used

// attributes is an association array of association arrays (dict-of-dicts)
// attributes[i]['attName'] is the attName attribute of the 'i'th series
var attributes = new Array(seriesCount);
var attributesLoaded = false;

var dataMin = Number.MAX_VALUE;
var dataMax = Number.MIN_VALUE;

Array.prototype.unique = function() {
    var o = {}, i, l = this.length, r = [];
    for(i=0; i<l;i+=1) o[this[i]] = this[i];
    for(i in o) r.push(o[i]);
    return r;
};

// prepare startup dataset
for(var i=0;i<data.length;i++)
{
	data[i] = new Array(seriesLength);
	attributes[i] = {};
	attributes[i]['even'] = (i%2)==0;
	//attributes[i]['odd'] = (i%2)!=0;

	labels[i] = i;
	isSeriesBrushed[i] = false;
	for(var j=0; j<data[i].length; j++)
	{
		data[i][j] = Math.round((Math.random()*Math.abs(Math.sin(i/5)*Math.sin(j/5)))*100)/100;

		if(data[i][j]<dataMin) dataMin = data[i][j];
		if(data[i][j]>dataMax) dataMax = data[i][j];
	}
}

// load viridis perceptual colourmap
var viridis = [];
loadJSON('viridis.json', function(response) {
  // Parse JSON string into object
    viridis = JSON.parse(response);
    dataImageStale = true;
    drawData();
 });

attributesLoaded = true;

// need to force numeric sort
allSortedData = (data.reduce(function(a, b) {return a.concat(b);}, [])).sort(function(a, b){return a-b});
allPercentiles = [];
for(let i=allSortedData.length-1; i>=0; i--) allPercentiles[allSortedData[i]] = i/allSortedData.length

var zoomSelector = document.getElementById('zoomSelector');
zoomSelector.addEventListener("change", function() {setDatumSize(zoomSelector.value)});

datumWidth = zoomSelector.value;
datumHeight = datumWidth;
canvas.width = datumWidth*seriesLength;
canvas.height = datumHeight*seriesCount;
drawData();

// scroll event handler
document.addEventListener('scroll', function(evt)
{
    	const canvasOffset   = canvas.getBoundingClientRect().top - document.body.getBoundingClientRect().top

	//if(document.body.scrollTop > canvasOffset-40) //document.body.scrollTop is deprecated
	if(document.documentElement.scrollTop > canvasOffset-40) 
	{	// main canvas about to touch top of window
		document.getElementById('tools').style.position = 'fixed';
		document.getElementById('tools').style.top = '0.5em';

		document.getElementById('minimapContainer').style.position = 'fixed';
		document.getElementById('minimapContainer').style.top = '4em';
		document.getElementById('myCanvas').style.marginLeft='7.5em'
	}
	else
	{
		// main canvas far below top of window
		document.getElementById('tools').style.position = '';
		document.getElementById('tools').style.top = '';

		document.getElementById('minimapContainer').style.position = 'relative';
		document.getElementById('minimapContainer').style.top = '0px';
		document.getElementById('myCanvas').style.marginLeft='0em'
	}

	var topmostVisiblePixel = document.documentElement.scrollTop - canvasOffset;
	var bottomVisiblePixel = Math.min(topmostVisiblePixel+window.innerHeight,canvas.height);
	if(topmostVisiblePixel<0) topmostVisiblePixel = 0;

  // draw minimap scroll thumb
	minimapContext.clearRect(0,0,minimap.width,minimap.height);
	drawMinimap();
	minimapContext.beginPath();
	minimapContext.rect(0,
					Math.round((topmostVisiblePixel/canvas.height)*minimap.height),
					minimap.width,
					// in the expression below, all the extra parenthesis is necessary. Think about it.
					Math.round(((bottomVisiblePixel-topmostVisiblePixel)/canvas.height)*minimap.height));
	minimapContext.closePath();
	minimapContext.fillStyle = 'rgba(0,0,0,0.5)';
	minimapContext.fill();
	minimapContext.lineWidth = 1;
	minimapContext.strokeStyle = 'rgba(0,0,0,1)';
	minimapContext.stroke();

}, false);

//drag event handler for minimap
minimap.addEventListener('mousedown', function(mousedownEvent){

	const canvasOffset   = canvas.getBoundingClientRect().top - document.body.getBoundingClientRect().top
	var mousedownPos = getMousePos(minimap, mousedownEvent);
	var topmostVisiblePixel = document.documentElement.scrollTop - canvasOffset;
	var bottomVisiblePixel = Math.min(topmostVisiblePixel+window.innerHeight,canvas.height);

	// if the drag originates from within the minimap scroll 'thumb'
	if(mousedownPos.y>Math.round((topmostVisiblePixel/canvas.height)*minimap.height)
	 &&mousedownPos.y<Math.round((bottomVisiblePixel/canvas.height)*minimap.height))
	{
		minimap.onmousemove = function(mousemoveEvent){
			var mousemovePos = getMousePos(minimap, mousemoveEvent);
			var yOffset = mousemovePos.y - mousedownPos.y;
			var pixelsFromThumbTop = mousedownPos.y - Math.round((topmostVisiblePixel/canvas.height)*minimap.height);
			//console.log(yOffset);
			window.scrollTo(0,
				Math.round(canvasOffset+(mousemovePos.y/minimap.height)*canvas.height)
				-Math.round((pixelsFromThumbTop/minimap.height)*canvas.height));
		};
	}

}, false);

minimap.addEventListener('mouseup', function(mousedownEvent){
	minimap.onmousemove = function(mousemoveEvent){
		// Do nothing
	};
}, false);

minimap.addEventListener('mouseout', function(mousedownEvent){
	minimap.onmousemove = function(mousemoveEvent){
		// Do nothing
	};
}, false);

// MAIN CANVAS EVENT HANDLERS
// mousemove event handler
canvas.addEventListener('mousemove', function(evt) {
	var mousePos = getMousePos(canvas, evt);

	// note! the select mode has been retired, in favour of the new brushing options
	if(currentMode()==='select' && mousedown)
	{
		context.clearRect(0, 0, canvas.width, canvas.height);
		//context.drawImage(imageObj, 0, 0);
		drawData();

		/* // Old way -- just a freeform rectangle
		context.rect(selectRectCoords[0],
					selectRectCoords[1],
					mousePos.x-selectRectCoords[0],
					mousePos.y-selectRectCoords[1]);
		*/

		var leftest = Math.min(selectRectCoords[0],mousePos.x);
		var rightest = Math.max(selectRectCoords[0],mousePos.x);
		var toppest = Math.min(selectRectCoords[1],mousePos.y);
		var bottomest = Math.max(selectRectCoords[1],mousePos.y);

		var firstSelectedTimeCode = Math.round(leftest/datumWidth);
		var firstSelectedSeries = Math.floor(toppest/datumHeight);
		var lastSelectedTimeCode = Math.round(rightest/datumWidth);
		var lastSelectedSeries = Math.floor(bottomest/datumHeight);

		context.beginPath();
		//context.rect(upperLeftX,upperLeftY,width,height)
		context.rect(0,
					firstSelectedSeries*datumHeight,
					seriesLength*datumWidth,
					(lastSelectedSeries-firstSelectedSeries+1)*datumHeight);

		// do I need a context.endPath() here?
		context.fillStyle = 'rgba(0,0,255,0.3)';
		context.fill();
		context.lineWidth = 1;
		context.strokeStyle = 'rgba(0,0,255,1)';
		context.stroke();
	}
	else if(currentMode()==='selectBrush' && mousedown)
	{
		var hoverSeries = Math.floor(mousePos.y/datumHeight);
		if(!isSeriesBrushed[hoverSeries])
		{
			isSeriesBrushed[hoverSeries] = true; // brush row
			context.fillStyle = "rgba(255,255,255,0.8)";
			context.fillRect(0,hoverSeries*datumHeight,datumWidth*seriesLength,datumHeight); // highlight row
		}
		dataImageStale = true;
	}
	else if(currentMode()==='deselectBrush' && mousedown)
	{
		var hoverSeries = Math.floor(mousePos.y/datumHeight);
		if(isSeriesBrushed[hoverSeries])
		{
			isSeriesBrushed[hoverSeries] = false; // unbrush my row... say you'll love me again
			for(var j=0; j<seriesLength; j++)
			{
				var datum = data[hoverSeries][j];
				context.fillStyle = colourmap(normalise(datum));
				context.fillRect(j*datumWidth,hoverSeries*datumHeight,datumWidth,datumHeight);
			}
		}
		dataImageStale = true;
	}
	else if(currentMode()==='shift' && mousedown)
	{
		var shiftTo = Math.floor(mousePos.y/datumHeight);
		if(shiftTo!=shiftFrom)
		{
			shiftSeries(shiftFrom - shiftTo);
			shiftFrom = shiftTo;
			dataImageStale = true;
			drawData();
		}
	}
	else if(currentMode()==='scan')
	{
		var hoverSeries = Math.floor(mousePos.y/datumHeight);
		// console.log(mousePos.y);
		/*
			There is potential for a small bug here that I have chosen not to fix at this moment.
			The bug is that if datumHeight is 1, then hoverSeries stops being a value from 0 to
			seriesCount-1, and instead becomes a value from 1 to seriesCount. Now this causes javascript
			to throw an exception when you hover over the *last* time series because that index
			is too large, i.e. data[hoverSeries] does not exist when hoverSeries = data.length.

			Hmmm... there seems to be a related bug where no matter what datumHeight is, if you hover over
			the *last few pixels* of the last time series you get a similar TypeError.

			This boils down to the fact that you can get a mousePos.y which is canvas height+1 for some reason.
			Of course doing floor((canvas.height+1)/datumHeight) results in an index larger than the last hoverSeries.

			As this does not impact the working of the software, I have suppressed the errors by returning early.
		*/
		var hoverElement = Math.floor(mousePos.x/datumWidth);

		// skip when bullshit comes out of mousePos resulting in bad hoverSeries
		if(data[hoverSeries]===undefined) return;


		context.clearRect(0, 0, canvas.width, canvas.height);
		context.fillStyle = "rgba(255,255,255,0.8)";
		drawData();
		drawScanChart(hoverSeries, hoverElement);
		context.fillRect(0,hoverSeries*datumHeight,datumWidth*seriesLength,datumHeight); // highlight row
		context.fillRect(hoverElement*datumWidth,0,datumWidth,seriesCount*datumHeight); // highlight column

		// to get sharp lines in canvas, offset by 0.5
		// see: http://diveintohtml5.info/canvas.html (section on 'ask professor markup')

		var scanDisplay = document.createElement('div');
		scanDisplay.id = 'scanDisplay';

		// this is one of the lines that will get messed up if you start only rearranging labels and not the actual data series
		scanDisplay.innerHTML="Series "+labels[hoverSeries]+" | Element "+hoverElement+" | Value: "+data[hoverSeries][hoverElement];

		scanDisplay.innerHTML+=HTMLTableFromObject(attributes[labels[hoverSeries]]);
							 //+JSON.stringify(attributes[labels[hoverSeries]]);
		document.getElementById('scanChartContainer').appendChild(scanDisplay);
	}
}, false);

// mousedown event handler
canvas.addEventListener('mousedown', function(evt)
{
	mousedown = true;
	var mousePos = getMousePos(canvas, evt);
	if(currentMode()==='select')
	{
		selectRectCoords[0] = mousePos.x;
		selectRectCoords[1] = mousePos.y;
	}
	else if(currentMode()==='shift')
	{
		/*
			shiftFrom contains the index of the row of data where the user
			starts dragging from in shift mode. It ignores the fact that the data might have been
			rearranged. So if shiftFrom is 5, it just means the user literally started dragging
			the 5th row. It doesn't mean this was the 5th series in the original dataset.
		*/
		shiftFrom = Math.floor(mousePos.y/datumHeight);
	}
	else if(currentMode()==='selectBrush')
	{
		var hoverSeries = Math.floor(mousePos.y/datumHeight);
		if(!isSeriesBrushed[hoverSeries])
		{
			isSeriesBrushed[hoverSeries] = true; // brush row
			context.fillStyle = "rgba(255,255,255,0.8)";
			context.fillRect(0,hoverSeries*datumHeight,datumWidth*seriesLength,datumHeight); // highlight row
		}
		dataImageStale = true;
	}
	else if(currentMode()==='deselectBrush')
	{
		var hoverSeries = Math.floor(mousePos.y/datumHeight);
		if(isSeriesBrushed[hoverSeries])
		{
			isSeriesBrushed[hoverSeries] = false; // unbrush my row... say you'll love me again
			for(var j=0; j<seriesLength; j++)
			{
				var datum = data[hoverSeries][j];
				context.fillStyle = colourmap(normalise(datum));
				context.fillRect(j*datumWidth,hoverSeries*datumHeight,datumWidth,datumHeight);
			}
		}
	}
}, false);

// mouseup event handler
canvas.addEventListener('mouseup', function(evt)
{
	mousedown = false;
	var mousePos = getMousePos(canvas, evt);
	if(currentMode()==='select')
	{
		selectRectCoords[2] = mousePos.x;
		selectRectCoords[3] = mousePos.y;
	}
	else if(currentMode()==='scan')
	{
		// TODO: create a persistent line graph of the series the user has clicked on
		// in a separate div for more detailed inspection
	}
	else if(currentMode()=='shift')
	{
		dataImage.src = canvas.toDataURL();
		dataImageStale = false;
		drawMinimap();
	}
}, false);

// mouseout event handler
canvas.addEventListener('mouseout', function(evt)
{
	if(currentMode()==='scan')
	{
		var container = document.getElementById('scanChartContainer');
		//while(container.firstChild) container.removeChild(container.firstChild);
		container.style.display='none';
		drawData();
	}
}, false);

// mouseover event handler
canvas.addEventListener('mouseover', function(evt)
{
	if(currentMode()==='scan')
	{
		var container = document.getElementById('scanChartContainer');
		//while(container.firstChild) container.removeChild(container.firstChild);
		container.style.display='initial';
	}
}, false);

canvas.style.cursor = 'default'; // stop annoying selection cursor when brushing
// radio button change event handlers
// primarily to change the cursor on the canvas
for(var i=0;i<modeButtons.length;i++)
{
	modeButtons[i].onclick = function(evt)
	{
		if(currentMode()==='shift')
			canvas.style.cursor = 'row-resize'; // all-scroll also ok
		else
			canvas.style.cursor = 'default';
	};
}

var normalisationSelector = document.getElementById('normalisationSelector');
normalisationSelector.addEventListener("change", function() {
	currentNormalisation = normalisationSelector.value;

	if (currentNormalisation === 'percentile')
			normalise = percentile;
		else
			normalise = rangeNormalise;

	dataImageStale = true;
	drawData();
});

var colourmapSelector = document.getElementById('colourmapSelector');
colourmapSelector.addEventListener("change", function() {
	currentColourMap = colourmapSelector.value;

	if (currentColourMap === 'grayscale')
			colourmap = getGrayscaleColorString;
		else if (currentColourMap === 'redyellowgreen')
			colourmap = getRedYellowGreenColorString;
		else if (currentColourMap === 'viridis')
			colourmap = viridisColorString;
		else
			colourmap = rainbowColorString;

		dataImageStale = true;
		colourCache = []
		drawData();
});

var gatheringStrategySelector = document.getElementById('gatheringStrategySelector');

// sets up explain tabs
window.onload = function() {
	const tabs = document.querySelectorAll('.tabs .tab-links a')
	for(let i=0; i<tabs.length; i++) {
		tabs[i].onclick = function(e)  {
			var currentAttrValue = event.target.getAttribute("href")
			console.log(currentAttrValue)

			// Show/Hide Tabs
			document.querySelectorAll('.tab').forEach(function(t) {t.style.display = "none"})
			document.querySelector('.tabs ' + currentAttrValue).style.display = "block"	

			// Change/remove current tab to active
			document.querySelectorAll('.tab-links li').forEach(function(t) {t.classList.remove('active')})
			event.target.parentNode.classList.add('active')

			e.preventDefault();
		}
	}
}

// START FUNCTION DEFINITIONS
function writeMessage(canvas, message)
{
	var context = canvas.getContext('2d');
	context.clearRect(0, 0, canvas.width, canvas.height);
	context.font = '1em Helvetica';
	context.fillStyle = 'black';
	context.fillText(message, 10, 25);
}

function getMousePos(canvas, evt)
{
	var rect = canvas.getBoundingClientRect();
	return {
		x: evt.clientX - rect.left,
		y: evt.clientY - rect.top
	};
}

function getRedGreenColorString(value)
{
	var red;
	var green;
	var blue;

	// Straightforward scaling -- creates a muddy green colour
	red = value*255;
	green = (1-value)*255;
	blue = 0;

	red = Math.round(red);
	green = Math.round(green);
	blue = Math.round(blue);

	return "rgb("+red+","+green+","+blue+")";
}

// http://stackoverflow.com/questions/5137831/map-a-range-of-values-e-g-0-255-to-a-range-of-colours-e-g-rainbow-red-b
function rainbowColorString(value) {
    // value = value * 240; // for red-blue
    // final hue value needs to be between 0 and 240 for red-blue. Goes all the way to 360 but that takes you back to red.
    value = value * 300; // red-pinkish?
    return 'hsl(' + value + ',100%,50%)';
}

function viridisColorString(value) {
	const index = Math.ceil(value*(viridis.length-1));

	var red;
	var green;
	var blue;

	try {
		red = Math.round(viridis[index][0]*255);
		green = Math.round(viridis[index][1]*255);
		blue = Math.round(viridis[index][2]*255);
	}
	catch(e) {
  			// currently do nothing. Was getting a bunch of 0 and -1, should fix that at some point
  			//console.log('rogue index is '+index);
		}

  	return "rgb("+red+","+green+","+blue+")";
}

function percentile(value)
{
	if (allPercentiles[value] === undefined)
	{
		allPercentiles[value] = (allSortedData.indexOf(value)/allSortedData.length);
	}

	return allPercentiles[value];
}

function rangeNormalise(value)
{
	// mean & range normalisation
	// doesn't do so well with negative numbers in range
	return (value-dataMin)/Math.abs(dataMax-dataMin);
}

function getRedYellowGreenColorString(value)
{
	var red;
	var green;
	var blue;

	blue = 0;
	// Goes through green-red hue transition in HSV space
	if(value<0.5)
	{
		green = 255;
		red = 2*value*255;
	}
	else
	{
		red = 255;
		// green = 255 when norm = 0.5, green = 0 when norm = 1.
		// Solve the equation of that line and you end up with the following expression.
		green = 2*((-255*value)+255);
	}

	red = Math.round(red);
	green = Math.round(green);
	blue = Math.round(blue);

	//console.log(value+" --> "+normalised+" --> "+ "rgb("+red+","+green+","+blue+")")
	return "rgb("+red+","+green+","+blue+")";
}

function getSpecialColorString(value)
{
	// doesn't do so well with negative numbers in range
	//var normalised = (value-dataMin)/Math.abs(dataMax-dataMin);

	// special normalisation for Gatherminer paper panic time
	var normalised = 0;
	if(value>0) normalised = 0.4;
	if(value>1) normalised = 0.6;
	if(value>5) normalised = 0.8;
	if(value>10) normalised = 0.9;
	if(value>20) normalised = 1.0;

	var red;
	var green;
	var blue;

	blue = 0;
	// Goes through green-red hue transition in HSV space
	if(normalised<0.5)
	{
		green = 255;
		red = 2*normalised*255;
	}
	else
	{
		red = 255;
		// green = 255 when norm = 0.5, green = 0 when norm = 1.
		// Solve the equation of that line and you end up with the following expression.
		green = 2*((-255*normalised)+255);
	}

	red = Math.round(red);
	green = Math.round(green);
	blue = Math.round(blue);

	if (normalised===0) red = 255, green = 255, blue = 255;

	//console.log(value+" --> "+normalised+" --> "+ "rgb("+red+","+green+","+blue+")")
	return "rgb("+red+","+green+","+blue+")";
}


function getGrayscaleColorString(value)
{
	var red;
	var green;
	var blue;

	red = value*255;
	green = value*255;
	blue = value*255;

	red = Math.round(red);
	green = Math.round(green);
	blue = Math.round(blue);

	return "rgb("+red+","+green+","+blue+")";
}

function getReverseGrayscaleColorString(value)
{
	var normalised = (value-dataMin)/Math.abs(dataMax-dataMin);

	normalised = 1-normalised;


	var red;
	var green;
	var blue;

	red = normalised*255;
	green = normalised*255;
	blue = normalised*255;

	red = Math.round(red);
	green = Math.round(green);
	blue = Math.round(blue);

	return "rgb("+red+","+green+","+blue+")";
}

function loadData()
{
	var selected_file = document.getElementById('input').files[0];
	if(!selected_file)
	{
		alert("No file chosen!");
		return;
	}
	var reader = new FileReader();  // Create a FileReader object
	reader.readAsText(selected_file);           // Read the file

	reader.onload = function(){    // Define an event handler
		var text = reader.result;   // This is the file contents

		dataMin = Number.MAX_VALUE;
		dataMax = Number.MIN_VALUE;

		var allTextLines = text.split(/\r\n|\n/);
		var lines = [];
		for (var i=0; i<allTextLines.length; i++) {
			if (allTextLines[i].length===0) continue
			var elems = allTextLines[i].split(',');
			var tarr = [];
			for (var j=0; j<elems.length; j++) {
				var floatDatum = parseFloat(elems[j]);
				tarr.push(floatDatum);
				allData.push(floatDatum)
			  	// need to parse before comparing because otherwise it does a fucking string comparison
			  	// silently, which creates a fucking mess
			  	if(floatDatum<=dataMin) dataMin = floatDatum;
			  	if(floatDatum>=dataMax) dataMax = floatDatum;
			}
			lines.push(tarr);
		}
		data = lines;
		console.log("Series loaded: "+lines.length);
		console.log("Min: "+dataMin+", max: "+dataMax);

		// need to force numeric sort
		console.log("Sorting")
		allSortedData = allData.sort(function(a, b){return a-b});
		allPercentiles = [];
		console.log("Precomputing percentiles")
		for(let i=allSortedData.length-1; i>=0; i--) allPercentiles[allSortedData[i]] = i/allSortedData.length

		seriesCount = data.length;
		seriesLength = data[0].length;

		canvas.height = datumHeight * seriesCount;
		canvas.width  = datumWidth  * seriesLength;

		labels = [];
		isSeriesBrushed = [];
		for(var i=0;i<seriesCount;i++)
		{
			labels[i] = i;
			isSeriesBrushed[i] = false;
		}

		console.log('Drawing gatherplot')
		context.clearRect(0, 0, canvas.width, canvas.height);
		dataImageStale = true;
		drawData();

		// refresh data image
		dataImage.src = canvas.toDataURL();
		dataImageStale = false;

		drawMinimap();
		// drawHist([]); // empty argument because no selected series
		attributesLoaded = false;
	}
}

function loadAttributes()
{
	var selected_file = document.getElementById('inputAttributes').files[0];
	if(!selected_file)
	{
		alert("No file chosen!");
		return;
	}
	var reader = new FileReader();  // Create a FileReader object
	reader.readAsText(selected_file);           // Read the file

	reader.onload = function(){    // Define an event handler
		var text = reader.result;   // This is the file contents
		attArray = CSVToArray(text);
		var headers = attArray[0];

		if((seriesCount+1)!=attArray.length)
		{
			alert('Size of attribute file does not match data. Please ensure attribute file has a header line and as many entries as there are series in your dataset.');
			return;
		}

		// this is a complicated loop
		// it sets each attribute of each time series
		// since a header line is assumed, you get attArray[i+1]
		attributes = [];
		for(var i=0;i<seriesCount;i++)
		{
			attributes[labels[i]] = {};
			for(var j=0;j<headers.length;j++)
			{
				attributes[labels[i]][headers[j]] = attArray[i+1][j];
			}
		}

		attributesLoaded = true;
		console.log('Attributes loaded successfully');
	}
}

function gather()
{
	var gatherWorker = new Worker("gatherer.js");
	var progressDisplay = document.getElementById('gatherProgress');
	progressDisplay.style.display="inline-block";

	gatherWorker.postMessage({"lists":data,
							  "strategy":gatheringStrategySelector.value,
							  "labels":labels,
							  "precomputeDistances": document.getElementById("precomputeDistancesCheckbox").checked
							});

	gatherWorker.addEventListener('message', function(e) {
		if(e.data.type==='distanceProgress')
		{
			progressDisplay.innerHTML = 'Computing distances: '+ Math.round((e.data.value*100)/seriesCount)+'%';
		}
		else if(e.data.type==='recomposeProgress')
		{
			if(e.data.value==='none')
				progressDisplay.innerHTML = 'Recomposing...';
			else
				progressDisplay.innerHTML = 'Recomposing: '+ Math.round(e.data.value*100)+'%';
		}
		else if(e.data.type==='labels')
		{
			labels = e.data.value
			console.log("Received labels. Reordering data...")
			let reorderedData = []
			for(let i=0; i<data.length; i++) reorderedData[i] = data[labels[i]]
			data = reorderedData
		}
		else if(e.data.type==='finished')
		{
			progressDisplay.innerHTML = "Done";
			progressDisplay.style.display="none";
			dataImageStale = true;
			drawData();
		}

	}, false);
}

function clearBrush()
{
	for(var i=0;i<isSeriesBrushed.length;i++) isSeriesBrushed[i] = false;

	dataImageStale = true;
	drawData();
}

function drawData()
{
	if(dataImageStale)
	{
		for(var i=0;i<seriesCount;i++)
		{
			for(var j=0; j<seriesLength; j++)
			{
				var datum = data[i][j];
				context.fillStyle = colourmap(normalise(datum));
				context.fillRect(j*datumWidth,i*datumHeight,datumWidth,datumHeight);
			}

			if(isSeriesBrushed[i])
			{
				context.fillStyle = "rgba(255,255,255,0.8)";
				context.fillRect(0,i*datumHeight,datumWidth*seriesLength,datumHeight); // highlight row
			}
		}

		if(currentMode()!=='shift')
		{
			// OLD METHOD: dataImage = context.getImageData(0,0,canvas.width,canvas.height);
			// shifting creates too many images, so we just wait until user
			// is no longer shifting to redraw.
			dataImage.src = canvas.toDataURL();
			dataImageStale = false;
			drawMinimap();
		}
	}
	else
	{
		//context.putImageData(imgData,x,y,dirtyX,dirtyY,dirtyWidth,dirtyHeight);
		//context.putImageData(dataImage,0,0);

		context.drawImage(dataImage,0,0);
		drawMinimap();
	}
}

function drawMinimap()
{
	minimapContext.drawImage(dataImage,0,0,minimap.width,minimap.height);
}

// currently unused function
function zoomMainCanvas(scaleFactor)
{
	if(Math.round(datumWidth * scaleFactor) < 1) return;
	//else, it's not going to get too small
	datumWidth = Math.round(datumWidth * scaleFactor);
	datumHeight = Math.round(datumHeight * scaleFactor);

	canvas.width = datumWidth*seriesLength;
	canvas.height = datumHeight*seriesCount;

	dataImageStale = true;
	drawData();
}

function setDatumSize(size)
{
	if(Math.round(size) < 1) return;
	//else, it's not going to get too small
	datumWidth = Math.round(size);
	datumHeight = Math.round(size);

	canvas.width = datumWidth*seriesLength;
	canvas.height = datumHeight*seriesCount;

	dataImageStale = true;
	drawData();
}

function drawScanChart(hoverSeries, hoverElement)
{
	var series = data[hoverSeries];
	var label = labels[hoverSeries];

	var labelsForChart = new Array(series.length);
	for(var i=0; i<labelsForChart.length; i++) labelsForChart[i] = i+1;
	var scanChartData = {
		labels: labelsForChart,
		datasets: [
			{
				label: label,
				fillColor: "rgba(0,0,0,0.2)",
				strokeColor: "rgba(0,0,0,1)",
				//pointColor: "rgba(151,187,205,1)",
				//pointStrokeColor: "#fff",
				//pointHighlightFill: "#fff",
				//pointHighlightStroke: "rgba(151,187,205,1)",
				data: series
			}
		]
	};

	//$('#scanChart').remove(); // removes node with id 'scanChart'
	var container = document.getElementById('scanChartContainer');
	while(container.firstChild) container.removeChild(container.firstChild);

	var node = document.createElement('canvas');
	node.id = 'scanChart';
	var container = document.getElementById('scanChartContainer');
	container.appendChild(node);
	container.style.top = (hoverSeries*datumHeight)-160+'px';
	container.style.left = (hoverElement*datumWidth)+50+'px';
	/*
	 	This complicated expression sets the width for the scan chart to:
	 	The larger of, either:
			1000 pixels, or
	 		The smaller of, either:
				15*serieslength (i.e. giving 15 pixels per element of the time series), or
				window.innerWidth

		var chartWidth = Math.max(1000,Math.min(window.innerWidth-70,series.length*15));
	*/

	var chartWidth = 600;//datumWidth*seriesLength;
	document.getElementById('scanChart').width=''+chartWidth;

	var ctx = document.getElementById('scanChart').getContext('2d');
	var myLineChart = new Chart(ctx).Line(scanChartData,
		{
			animation:false,
			bezierCurve:false,
			//pointDotRadius:2,
			//pointDotStrokeWidth:1,
			pointDot: false,
			showTooltips: false,
			scaleShowGridLines: false,
			scaleShowXLabels: false // my own addition to the Chart.js library
			//showScale: false
		}
	);
}

function drawLineChart(series, label, canvasID)
{
	var labelsForChart = new Array(series.length);
	for(var i=0; i<labelsForChart.length; i++) labelsForChart[i] = i+1;
	var scanChartData = {
		labels: labelsForChart,
		datasets: [
			{
				label: label,
				fillColor: "rgba(151,187,205,0.2)",
				strokeColor: "rgba(151,187,205,1)",
				pointColor: "rgba(151,187,205,1)",
				pointStrokeColor: "#fff",
				pointHighlightFill: "#fff",
				pointHighlightStroke: "rgba(151,187,205,1)",
				data: series
			}
		]
	};

	var oldParentNode = document.getElementById(canvasID).parentNode;
	//delete all children nodes
	while(oldParentNode.firstChild){oldParentNode.removeChild(oldParentNode.firstChild);}

	var node = document.createElement('canvas');
	node.id = canvasID;
	oldParentNode.appendChild(node);

	/*
	 	This complicated expression sets the width for the scan chart to:
	 	The larger of, either:
			1000 pixels, or
	 		The smaller of, either:
				15*seriesLength (i.e. giving 15 pixels per element of the time series), or
				window.innerwidth
	*/
	var chartWidth = Math.max(1000,Math.min(window.innerWidth-150,series.length*15))
	document.getElementById(canvasID).width=''+chartWidth;
	document.getElementById(canvasID).height='200';

	var ctx = document.getElementById(canvasID).getContext('2d');
	var myLineChart = new Chart(ctx).Line(scanChartData,
		{
			animation:false,
			bezierCurve:false,
			pointDotRadius:2,
			pointDotStrokeWidth:1,
			pointHitDetectionRadius:1 // lord almighty, this is what I was looking for!
			//tooltipEvents:["touchstart,touchmove"]
		}
	);
}

function shiftSeries(amount)
{
	amount = amount % seriesCount;
	if(amount > 0) // upwards shift
	{
		for(var i=0; i<amount; i++)
		{
			// for an upwards shift, need to remove from the top and place at bottom
			data.push(data.shift());
			labels.push(labels.shift());
		}
	}
	else
	{
		for(var i=0; i<(-amount); i++)
		{
			// for a downwards shift, need to remove from bottom and place at top
			data.unshift(data.pop());
			labels.unshift(labels.pop());
		}
	}
	dataImageStale = true;
}

function drawHist(selectedSeries)
{
	var overallData =
	{
		name: 'Overall (%)',
		x: allData,
		opacity: 0.75,
		type: 'histogram',
		histnorm: 'percent'
	};

	var selectedData =
	{
		name: 'Selected (%)',
		x: selectedSeries.reduce(function(a, b) {return a.concat(b);}, []),
		opacity: 0.75,
		type: 'histogram',
		histnorm: 'percent'
	};

	var dataHist = [overallData, selectedData];
	var layout = {barmode: 'overlay'};
	Plotly.newPlot('tab5', dataHist, layout);
}

function explain()
{
	if(!attributesLoaded)
	{
		alert('Attributes not loaded yet!');
		return;
	}

	var oDiv = document.getElementById('seriesList');
	oDiv.innerHTML = "The selection contains the following time series: <br>";

	var leftest = Math.min(selectRectCoords[0],selectRectCoords[2]);
	var rightest = Math.max(selectRectCoords[0],selectRectCoords[2]);
	var toppest = Math.min(selectRectCoords[1],selectRectCoords[3]);
	var bottomest = Math.max(selectRectCoords[1],selectRectCoords[3]);

	var firstSelectedTimeCode = Math.round(leftest/datumWidth);
	var firstSelectedSeries = Math.floor(toppest/datumHeight);
	var lastSelectedTimeCode = Math.round(rightest/datumWidth);
	var lastSelectedSeries = Math.floor(bottomest/datumHeight);

	var features = getKeysExcept(attributes[0],'interesting');
	var attValCounts = {};
	var attValCountsSelected = {};

	var selectedSeriesSum = new Array(seriesLength);
	var selectedSeriesCount = 0;
	for(var i=0;i<seriesLength;i++) selectedSeriesSum[i] = 0;

	/*
		augment attributes list objects with interesting field
		based on selection -- for use in the id3 decision tree

		also collect sum of selected series for aggregate chart
	*/

	var selectedSeries = [];
	for(var i=0;i<seriesCount;i++)
	{
		var seriesAttributes = attributes[labels[i]];
		//console.log(seriesAttributes);
		/* populates the attValCounts dictionary
			which is really a dictionary of dictionaries,
			indexed first by attribute names,
			and then by their values (so currently assumes categorical attributes).
			Keeps a count of how many have been seen.

			The attValCountsSelected dictionary is identical,
			except it is only incremented for rows within the bounds
			of the user selection.
		*/
		for(var j=0; j<features.length; j++)
		{
			var f = features[j];
			//console.log(f);
			if(attValCounts[f]===undefined)
			{
				attValCounts[f] = {};
				attValCountsSelected[f] = {};
			}

			if(attValCounts[f][seriesAttributes[f]]===undefined)
			{
				attValCounts[f][seriesAttributes[f]] = 0;
				attValCountsSelected[f][seriesAttributes[f]] = 0;
			}

			attValCounts[f][seriesAttributes[f]]++;
		}

		// rows within the selection
		//if(i>=firstSelectedSeries && i<=lastSelectedSeries) // old -- used the selection box
		if(isSeriesBrushed[i])
		{
			selectedSeriesCount++;
			oDiv.innerHTML += labels[i] + " ";
			attributes[labels[i]]['interesting'] = 'interesting';

			for(var j=0; j<features.length; j++)
			{
				var f = features[j];
				attValCountsSelected[f][seriesAttributes[f]]++;
			}

			for(var j=0; j<seriesLength; j++) selectedSeriesSum[j] += data[i][j];

			selectedSeries.push(data[i]);
		}
		else
		{
			attributes[labels[i]]['interesting'] = 'not interesting';
		}
	}
	//console.log(selectedSeriesSum);
	var selectedSeriesAvg = selectedSeriesSum.map(function(x){return x/selectedSeriesCount;});
	drawLineChart(selectedSeriesSum,"Sum","sumChart");
	drawLineChart(selectedSeriesAvg,"Average","avgChart");

	//var testModel = id3(examples,'play',features);
	//console.log(attValCounts);
	//console.log(attValCountsSelected);

	try
	{
		underscore_attributes = _(attributes); //endows this with special abilities
		var treeModel = id3(underscore_attributes,'interesting',features);
		//drawGraph(treeModel,'treeCanvas'); // old tree using google charts that came with id3.js
		//printInterestingRules(treeModel);

		//console.log(treeModel);
		var treeAsJSON = simpleTreeJSON(treeModel);
		//console.log(treeAsJSON);
		drawTreeFromJSON(treeAsJSON)


		var treeMapAsJSON = {attributeName: '', name:'', value:data.length, children: simpleTreeMapJSON(treeModel)};
		//var treeMapAsJSON = simpleTreeMapJSON(treeModel);

		var scatterpoints = treeAsScatterPoints(treeMapAsJSON,0,[[],[],[]]);
		//console.log(treeMapAsJSON);
		//console.log(scatterpoints);
		drawScatterTree(scatterpoints);

		// draw treemap
		// putting this after the scatterpoints generation because Bostock's treemap
		// completely mangles this JSON object
		drawTreeMap(treeMapAsJSON);
	}
	catch(err)
	{
		/*
		console.log("Unable to create tree. P.S. Sometimes this happens"
				   +" when you've selected the entire dataset and so none"
				   +" of the series gets marked as 'uninteresting', so it"
				   +" complains about not being able to do a binary classification.");
		*/
		console.log(err);
		document.getElementById('treeCanvas').innerHTML = 'Unable to generate tree. Sorry!';
	}

	var dataForCharts = {};

	// create necessary canvas elements and prepare dataForCharts

	// removes all existing nodes with class 'chart'
	// http://stackoverflow.com/questions/10842471/remove-all-elements-of-a-certain-class-with-javascript
	let chartElements = document.getElementsByClassName('chart');
	while(chartElements[0]) chartElements[0].parentNode.removeChild(chartElements[0])

	for(var i=0; i<features.length; i++)
	{
		var f = features[i];
		var newNode = document.createElement('div');
		newNode.className = 'chart';
		//newNode.innerHTML=f+'<br><canvas id=\''+f+'\' width="600" height="400"></canvas>';
		newNode.innerHTML=f+'<br><canvas id=\''+f+'\'></canvas>';
		document.getElementById('barChartView').appendChild(newNode);

		var featureValues = getAllKeys(attValCounts[f]);
		var countsOverall = [];
		var countsSelected = [];
		for(var j=0; j<featureValues.length; j++)
		{
			countsOverall[j] = attValCounts[f][featureValues[j]];
			countsSelected[j] = attValCountsSelected[f][featureValues[j]];
		}

		dataForCharts[f] = {
			labels: featureValues,
			datasets: [
				{
					label: "Overall",
					fillColor: "rgba(220,220,220,0.5)",
					strokeColor: "rgba(220,220,220,0.8)",
					highlightFill: "rgba(220,220,220,0.75)",
					highlightStroke: "rgba(220,220,220,1)",
					data: countsToProbabilities(countsOverall).map(function(e){return e*100;})
				},
				{
					label: "Selection",
					fillColor: "rgba(151,187,205,0.5)",
					strokeColor: "rgba(151,187,205,0.8)",
					highlightFill: "rgba(151,187,205,0.75)",
					highlightStroke: "rgba(151,187,205,1)",
					data: countsToProbabilities(countsSelected).map(function(e){return e*100;})
				}
			]
		}
	}

	// draw all charts using chart.js
	for(var i=0; i<features.length; i++)
	{
		var ctx = document.getElementById(features[i]).getContext('2d');
		var myBarChart = new Chart(ctx).Bar(dataForCharts[features[i]],
			{animation:false,
			 legendTemplate : "<ul class=\"<%=name.toLowerCase()%>-legend\">"
							 +"<% for (var i=0; i<datasets.length; i++){%>"
							 +"<li><span style=\"background-color:<%=datasets[i].fillColor%>\">"
							 +"<%if(datasets[i].label){%><%=datasets[i].label%><%}%> (%)</span>"
							 +"</li><%}%></ul>"
			}
		);
		//currently keeps writing this legend, could be more efficient
		document.getElementById("legend").innerHTML = myBarChart.generateLegend();
	}

   	// show explain tabs div
   	document.getElementById('explainTabs').style.display="block";
   	document.getElementById('explainToggle').innerHTML = "Hide explanation";

   	drawHist(selectedSeries);
}

function drawScatterTree(points)
{
	var trace1 = {
	  x: points[0],
	  y: points[1],
	  z: points[2],
	  mode: 'markers',
	  marker: {
	    size: 10,//points[2].map(x=>x*10),
	    symbol: 'circle', //points[2],
	    line: {
	      color: 'rgba(217, 217, 217, 0.14)',
	      width: 0.5
	    },
	    opacity: 0.8
	  },
	  type: 'scatter3d'
	};

	var data = [trace1];
	var layout = {
		margin: {
		    l: 0,
		    r: 0,
		    b: 0,
		    t: 0
	  	},
	  	xaxis: {
		    title: 'Coverage',
		    titlefont: {
		      family: 'Courier New, monospace',
		      size: 18,
		      color: '#7f7f7f'
		    }
	  	},
	 	yaxis: {
		    title: 'Entropy',
		    titlefont: {
		      family: 'Courier New, monospace',
		      size: 18,
		      color: '#7f7f7f'
		    }
	  	}
	 };
	Plotly.newPlot('scatterTree', data, layout);
}

function toggleDisplayExplanation()
{
	var explainTabs = document.getElementById('explainTabs');
	if(explainTabs.style.display==='none')
	{
		explainTabs.style.display='block';
		document.getElementById('explainToggle').innerHTML = "Hide explanation";
	}
	else
	{
		explainTabs.style.display='none';
		document.getElementById('explainToggle').innerHTML = "Show explanation";
	}
}

function currentMode()
{
	for(var i=0;i<modeButtons.length;i++)
		if(modeButtons[i].checked) return modeButtons[i].value;
}

function CSVToArray(csv)
{
	var allTextLines = csv.split(/\r\n|\n/);
  	var lines = [];
  	for (var i=0; i<allTextLines.length; i++) {
  		if (allTextLines[i].length===0) continue
		var elems = allTextLines[i].split(',');
		var tarr = [];
		for (var j=0; j<elems.length; j++) {
			tarr.push(elems[j]);
		}
		lines.push(tarr);
  	}
  	return lines;
}

function getKeysExcept(obj,except)
{
	var r = [];
	for (var k in obj)
		if (obj.hasOwnProperty(k))
			if(k!=except)
				r.push(k);

	return r;
}

function getAllKeys(obj)
{
	var r = [];
	for (var k in obj)
		if (obj.hasOwnProperty(k))
				r.push(k);

	return r;
}

function countsToProbabilities(counts)
{
	var sum = counts.reduce(function(a,b){return a+b;});
	//console.log(sum);
	var probabilities = counts.map(function(e){return e/sum;});
	return probabilities;
}

function HTMLTableFromObject(obj)
{
	var keys = getKeysExcept(obj,'interesting');
	var table = "<table>";
	for(var i=0;i<keys.length;i++)
	{
		table+="<tr>";
		table+="<td>"+keys[i]+"</td>";
		table+="<td>"+obj[keys[i]]+"</td>";
		table+="</tr>";
	}
	table += "</table>";
	return table;
}

// http://codepen.io/KryptoniteDove/post/load-json-file-locally-using-pure-javascript
function loadJSON(filePath, callback) {

    var xobj = new XMLHttpRequest();
        xobj.overrideMimeType("application/json");
    xobj.open('GET', filePath, true);
    xobj.onreadystatechange = function () {
          if (xobj.readyState == 4 && xobj.status == "200") {
            // Required use of an anonymous callback as .open will NOT return a value but simply returns undefined in asynchronous mode
            callback(xobj.responseText);
          }
    };
    xobj.send(null);
 }
