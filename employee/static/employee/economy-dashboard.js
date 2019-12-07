$(function() {
	var yearCounter = 0;
	var countryColor = {"Media" : "#6dbceb", "Publicity" : "#c8b631", "Events" : "#369ead", "Projects" : "#a2d1cf", "Finance" : "#f79647", "Membership" : "#7f6084", "Sessions" : "#4f81bc",
											"Website" : "#369ead", "Opensource" : "#86b402", "Core" : "#52514e", "Ecell" : "#a064a1", "Startups" : "#c24642", "Zimbabwe" : "#c24642"};
	var countryCode = {"Membership":"M","Projects":"P","Startups":"S"};
	var yearSlider = document.getElementById('year-slider');
	var orderedDataPoints = JSON.parse(JSON.stringify(getDataPoint(yearArr[0])));
	var DepartmentSizeBubbleChart;
	var merchandiseImportsExportsColumnChart;

//On click of the play button the bubble chart animation starts. Following callback function performs 6 transition between the actual dataPoints of the year(example from 1961 to 1962) to produce the animation effect
	var animationIteration = 0;
	var pauseAnimation = true;
	var numberOfTransitions = 5;
	$('#startGraphAnimation').click(function () {
		$('#pauseGraphAnimation').show();
		$('#startGraphAnimation').hide();
		var dynamicDataPoints = [];
		yearCounter++;
		if (yearCounter >= yearArr.length) {
			yearCounter = 0;
			DepartmentSizeBubbleChart = createDepartmentSizeChart(getDataPoint(yearArr[yearCounter]));
			yearSlider.noUiSlider.set(yearArr[yearCounter]);
		}
		var nextDataPoints = getDataPoint(yearArr[yearCounter]);
		pauseAnimation = false;
		var animationInterval = setInterval(function(){
			if (animationIteration === 6) {
				orderedDataPoints = JSON.parse(JSON.stringify(dynamicDataPoints));
				animationIteration = 0;
				yearSlider.noUiSlider.set(yearArr[yearCounter]);
				yearCounter++;
				nextDataPoints = getDataPoint(yearArr[yearCounter]);
				if (yearCounter >= yearArr.length) {
					yearSlider.noUiSlider.set(yearArr[yearCounter]);
					orderedDataPoints = getDataPoint(yearArr[0]);
					clearInterval(animationInterval);
					pauseAnimation = true;
					$('#startGraphAnimation').show();
					$('#pauseGraphAnimation').hide();
				}
				if (pauseAnimation === true) {
					if (yearCounter !== yearArr.length - 1) {
						yearCounter--;
					}
					clearInterval(animationInterval);
				}
			}
			else{
				dynamicDataPoints = [];
					for (var j = 0; j < nextDataPoints.length; j++) {
						if (nextDataPoints[j].name !== orderedDataPoints[j].name) {
							orderedDataPoints.splice( j, 0, { x: 0.01, y : 0, z : 0, name: nextDataPoints[j].name } );
						}
						if (nextDataPoints[j].name === "Membership" || nextDataPoints[j].name === "Projects" || nextDataPoints[j].name === "Startups") {
							dynamicDataPoints.push({
								x: orderedDataPoints[j].x + (nextDataPoints[j].x - orderedDataPoints[j].x) * animationIteration / numberOfTransitions,
								y: orderedDataPoints[j].y + (nextDataPoints[j].y - orderedDataPoints[j].y) * animationIteration / numberOfTransitions,
								z: nextDataPoints[j].z,
								name: nextDataPoints[j].name,
								color: countryColor[nextDataPoints[j].name],
								cursor: "pointer",
								indexLabel: countryCode[nextDataPoints[j].name],
								indexLabelFontColor: "#fbf3de"
							 });
						} else {
							dynamicDataPoints.push({
								x: orderedDataPoints[j].x + (nextDataPoints[j].x - orderedDataPoints[j].x) * animationIteration / numberOfTransitions,
								y: orderedDataPoints[j].y + (nextDataPoints[j].y - orderedDataPoints[j].y) * animationIteration / numberOfTransitions,
								z: nextDataPoints[j].z,
								name: nextDataPoints[j].name,
								color: countryColor[nextDataPoints[j].name],
								cursor: "pointer"
							});
						}
					}
					DepartmentSizeBubbleChart.options.data[0].dataPoints = JSON.parse(JSON.stringify(dynamicDataPoints));
					DepartmentSizeBubbleChart.options.subtitles[0].text = yearArr[yearCounter];
					animationIteration++;
			}
			DepartmentSizeBubbleChart.render();
			}, 35);
	});

//pause the bubble chart animation and display the play button
	$('#pauseGraphAnimation').click(function () {
		$('#startGraphAnimation').show();
		$('#pauseGraphAnimation').hide();
		pauseAnimation=true;
	});

//Get the dataPoints for all the countries for the specific year
	function getDataPoint(year) {
		var dataPoints=[];
			$.each(economyData,function (countryName,categoryData) {
				if (typeof(categoryData["DepartmentSize"][year]) !== "undefined" && typeof(categoryData["Efficiency"][year]) !== "undefined" && typeof(categoryData["population"][year]) !== "undefined") {
					if (countryName === "Membership" || countryName === "Projects" || countryName === "Startups") {
						dataPoints.push({x: categoryData["DepartmentSize"][year], y: categoryData["Efficiency"][year], z: categoryData["population"][year], name: countryName, color: countryColor[countryName], cursor: "pointer",
														 indexLabel: countryCode[countryName], indexLabelFontColor:"#fbf3de"});
					} else {
						dataPoints.push({x: categoryData["DepartmentSize"][year], y: categoryData["Efficiency"][year], z: categoryData["population"][year], name: countryName, color: countryColor[countryName], cursor: "pointer"});
					}
				}
			});
		return JSON.parse(JSON.stringify(dataPoints));
	}

//Department Size vs Efficiency bubble chart
	function createDepartmentSizeChart(dataPoints) {
		var DepartmentSizeBubbleChart = new CanvasJS.Chart("GDP-per-capita-bubble-chart",
			{
				backgroundColor: "transparent",
				axisX: {
					labelFontWeight: 'lighter',
					lineThickness: 1,
					logarithmic: true,
					minimum: 10,
					maximum: 70000,
					tickLength: 10,
					tickThickness: 1,
					title: "Department Size",
					titleFontColor: "#065f66",
					valueFormatString: "#,###"
				},
				axisY: {
					gridThickness: 1,
					labelFontWeight: 'lighter',
					lineThickness: 1,
					minimum: 30,
					maximum: 100,
					tickThickness: 1,
					tickLength: 10,
					title: "Efficiency",
					titleFontColor: "#065f66",
					valueFormatString: "#,###"
				},
				toolTip: {
					contentFormatter: function(e) {
						var content = "";
						for (var i = 0; i < e.entries.length; i++) {
							content += "<strong>" + e.entries[i].dataPoint.name + "</strong> <br/> Department Size: " + CanvasJS.formatNumber(e.entries[i].dataPoint.x,"#,###.##") + " <br/> Efficiency: " +
							CanvasJS.formatNumber(e.entries[i].dataPoint.y,"#,###.##") + " \%<br/> Volume: "+formatTooltipNumber(e.entries[i].dataPoint.z);
						}
						return content;
					}
				},
				data: [
					{
						indexLabelPlacement: "outside",
						legendMarkerType: "circle",
						name: "Size of Bubble Represents Complaints volume (click on any bubble to see more details)",
						showInLegend: true,
						type: "bubble",
						click: showChartForSelectedCountry,
						dataPoints: dataPoints
					}
				],
				subtitles: [
				{
					dockInsidePlotArea: true,
					fontColor: "rgba(50,30,150,0.1)",
					fontSize: 126,
					text: yearArr[yearCounter],
					verticalAlign: "center"
				}
				],
			});

		DepartmentSizeBubbleChart.render();
		return DepartmentSizeBubbleChart;
	}

//On click of the bubble in the bubble chart it scrolls down to the chart of population, working population, and Merchandise import and export chart
	function showChartForSelectedCountry(e) {
		$('div #selected-country').each(function(){
			$(this).html(' - '+e.dataPoint.name);
		});
		createPopulationChart(e.dataPoint.name);
		createWorkingPopulationChart(e.dataPoint.name);
		merchandiseImportsExportsColumnChart = createMerchandiseImportsExportsChart(e.dataPoint.name);
		setMerchandiseImportsExportsColumnChartAxisYTitleFontSize();
		$('html,body').animate({scrollTop: $("#population-charts").offset().top},400);
	}

//Set the subtitle of the bubble chart to display the year during the animation of the chart
	function setBubbleChartSubtitlesFontSize() {
		if ($('#GDP-per-capita-bubble-chart').height() === 400) {
			DepartmentSizeBubbleChart.options.subtitles[0].fontSize = 113;
		}
		if ($('#GDP-per-capita-bubble-chart').height() === 300) {
			DepartmentSizeBubbleChart.options.subtitles[0].fontSize = 60;
		}
		DepartmentSizeBubbleChart.render();
	}

//Initiate the slider
	function createSlider(startingYear) {
		noUiSlider.create(yearSlider, {
			start: startingYear,
			connect: "lower",
			step: 1,
			animate: false,
			range: {
				'min': yearArr[0],
				'max': yearArr[yearArr.length-1]
			},
			pips: {
				mode: 'values',
				stepped: true,
				values: getYearArrForSlider(),
				density: 2
			}
		});
	}

//Get the number of jumps to be taken for the year array as per the width of the slider
	function getYearJump(){
		var yearJumps = 0;
		if($(window).outerWidth() > 1800){
			yearJumps = 0;
		}
		if($(window).outerWidth() < 1800 && $(window).outerWidth() > 1000){
			yearJumps = 1;
		}
		if($(window).outerWidth() < 1000 && $(window).outerWidth() > 600){
			yearJumps = 2;
		}
		if($(window).outerWidth() < 600 && $(window).outerWidth() > 450){
			yearJumps = 3;
		}
		if($(window).outerWidth() < 450 && $(window).outerWidth() > 400){
			yearJumps = 4;
		}
		if($(window).outerWidth() < 400 && $(window).outerWidth() > 350){
			yearJumps = 5;
		}
		if($(window).outerWidth()<350){
			yearJumps = 6;
		}
		return yearJumps;
	}

//Get the year array to be displayed on the slider scale
	function getYearArrForSlider() {
		var modifiedYearArr = [];
		for (var i = 0; i < yearArr.length; i++) {
			modifiedYearArr.push(yearArr[i]);
			i = i + getYearJump();
		}
		return modifiedYearArr;
	}

//Bind click event on year slider
	function bindClickEventToSliderScale() {
	$(".noUi-value").click( function() {
		yearSlider.noUiSlider.updateOptions({
			range: {
				'min': yearArr[0],
				'max': yearArr[yearArr.length-1]
			},
			animate: true
		});
		yearSlider.noUiSlider.set($(this).html());
		yearSlider.noUiSlider.updateOptions({
			range: {
				'min': yearArr[0],
				'max': yearArr[yearArr.length-1]
			},
			animate: false
		});
	});
	}

//Bind slider update event
	function bindYearSliderUpdateEvent() {
		yearSlider.noUiSlider.on('update', function (values, handle) {
			$(".noUi-value").each( function () {
				if (parseInt($(this).html()) === parseInt(values[handle])) {
					$(this).addClass('noUi-value-large');
					$(this).removeClass('noUi-value-sub');
					$(this).prev().addClass('noUi-marker-large');
					$(this).prev().removeClass('noUi-marker-sub');
				} else {
					$(this).addClass('noUi-value-sub');
					$(this).removeClass('noUi-value-large');
					$(this).prev().addClass('noUi-marker-sub');
					$(this).prev().removeClass('noUi-marker-large');
				}
			});
			yearCounter = yearArr.indexOf(parseInt(values[handle]));
			if (pauseAnimation === true) {
				orderedDataPoints = getDataPoint(parseInt(values[handle]));
				DepartmentSizeBubbleChart = createDepartmentSizeChart(getDataPoint(parseInt(values[handle])));
			}
		});
	}

//Population chart
	function createPopulationChart(selectedCountry) {
		var populationDataPoints = [];
		$.each(economyData[selectedCountry]["population"], function (year, population) {
			populationDataPoints.push({x: parseInt(year), y: population});
		});
		var populationAreaChart = new CanvasJS.Chart("population-line-chart",
		{
			animationEnabled: true,
			backgroundColor: "transparent",
			axisX: {
				labelFontWeight: 'lighter',
				lineThickness: 1,
				tickThickness: 1,
				valueFormatString: "####",
				viewportMinimum: yearArr[0],
				viewportMaximum: yearArr[yearArr.length-1],
			},
			axisY: {
				gridThickness: 1,
				includeZero: false,
				labelFontWeight: 'lighter',
				lineThickness: 1,
				labelFormatter: addSymbols,
				tickThickness: 1,
				title: "On-Time",
				titleFontColor: "#065f66"
			},
			toolTip: {
				content: populationChartTooltipContent
			},
			data: [
			{
				markerSize: 0,
				name: "Population",
				type: "splineArea",
				xValueFormatString: "####",
				dataPoints: populationDataPoints
			}
			]
		});

		populationAreaChart.render();
	}

// working population chart
	function createWorkingPopulationChart(selectedCountry) {
		var workingPopulationDataPoints = [];
		$.each(economyData[selectedCountry]["workingPopulation"], function (year, population) {
			workingPopulationDataPoints.push({x: parseInt(year), y: population});
		});
		var workingPopulationAreaChart = new CanvasJS.Chart("working-population-line-chart",
		{
			animationEnabled: true,
			backgroundColor: "transparent",
			axisX: {
				labelFontWeight: 'lighter',
				lineThickness: 1,
				tickThickness: 1,
				valueFormatString: "####",
				viewportMinimum: yearArr[0],
				viewportMaximum: yearArr[yearArr.length-1],
			},
			axisY: {
				gridThickness: 1,
				includeZero: false,
				labelFontWeight: 'lighter',
				lineThickness: 1,
				suffix: "%",
				tickThickness: 1,
				title: "Deadlines Missed",
				titleFontColor: "#065f66"
			},
			legend: {
				verticalAlign: "top"
			},
			toolTip: {
				content: "<strong>{x}</strong> <br/> {name}: {y}"
			},
			data: [
			{
				color: "#c24642",
				markerSize: 0,
				name: "Deadlines Missed",
				type: "splineArea",
				xValueFormatString: "####",
				yValueFormatString: "##.##'%'",
				dataPoints: workingPopulationDataPoints
			}
			]
		});
		workingPopulationAreaChart.render();
	}

//Complaints Alloted and exports chart
	function createMerchandiseImportsExportsChart(selectedCountry) {
		var merchandiseImportsDataPoints = [];
		var merchandiseExportsDataPoints = [];
		$.each(economyData[selectedCountry]["merchandiseImports"], function (year, population) {
			merchandiseImportsDataPoints.push({x: parseInt(year), y: population});
		});
		$.each(economyData[selectedCountry]["merchandiseExports"], function (year, population) {
			merchandiseExportsDataPoints.push({x: parseInt(year), y: population});
		});
		var merchandiseImportsExportsColumnChart = new CanvasJS.Chart("merchandise-imports-exports-column-chart",
		{
			animationEnabled: true,
			backgroundColor: "transparent",
			axisX: {
				labelFontWeight: 'lighter',
				lineThickness: 1,
				tickThickness: 1,
				valueFormatString: "####",
			},
			axisY: {
				gridThickness: 1,
				includeZero: false,
				labelFontWeight: 'lighter',
				labelFormatter: addSymbols,
				lineThickness: 1,
				tickThickness: 1,
				title: "Complaints Alloted & Passed",
				titleFontColor: "#065f66",
				titleFontSize: 30
			},
			legend: {
				cursor: "pointer",
				verticalAlign: "top",
				itemclick: function (e) {
					if (typeof (e.dataSeries.visible) === "undefined" || e.dataSeries.visible) {
							e.dataSeries.visible = false;
							setMerchandiseImportExportAxisYTitle(e);
					} else {
							e.dataSeries.visible = true;
							setMerchandiseImportExportAxisYTitle(e);
					}
					e.chart.render();
				}
			},
			toolTip: {
				shared: true,
				contentFormatter: merchandiseImportsExportsChartTooltipContent
			},
			data: [
			{
				name: "Complaints Alloted",
				showInLegend: true,
				type: "column",
				visible: true,
				dataPoints: merchandiseImportsDataPoints
			},
			{
				name: "Complaints Passed-On",
				showInLegend: true,
				type: "column",
				visible: true,
				dataPoints: merchandiseExportsDataPoints
			}
			]
		});
		merchandiseImportsExportsColumnChart.render();
		return merchandiseImportsExportsColumnChart;
	}

	function setMerchandiseImportsExportsColumnChartAxisYTitleFontSize() {
		if ($('#merchandise-imports-exports-column-chart').height() === 500) {
			merchandiseImportsExportsColumnChart.options.axisY.titleFontSize = 30;
		}
		if ($('#merchandise-imports-exports-column-chart').height() === 400) {
			merchandiseImportsExportsColumnChart.options.axisY.titleFontSize = 25;
		}
		if ($('#merchandise-imports-exports-column-chart').height() === 300) {
			merchandiseImportsExportsColumnChart.options.axisY.titleFontSize = 16;
		}
		merchandiseImportsExportsColumnChart.render();
	}

	function addSymbols(e) {
		var suffixes = ["", "K", "", "", "K"];
		var order = Math.max(Math.floor(Math.log(e.value) / Math.log(1000)), 0);
		if (order > suffixes.length - 1)
			order = suffixes.length - 1;
		var suffix = suffixes[order];
		if (e.chart.options.data[0].name === "Complaints Alloted") {
			return "" + CanvasJS.formatNumber(e.value / Math.pow(1000, order)) + suffix;
		} else {
			return CanvasJS.formatNumber(e.value / Math.pow(1000, order)) + suffix;
		}
	}

	function setMerchandiseImportExportAxisYTitle(e) {
		if (e.chart.options.data[0].visible === true ) {
			if (e.chart.options.data[1].visible === false) {
				e.chart.options.axisY.title = e.chart.options.data[0].name;
			} else {
				e.chart.options.axisY.title = 'Complaints Alloted & Passed';
			}
		} else {
			if (e.chart.options.data[1].visible === false) {
				e.chart.options.axisY.title = '';
			} else {
				e.chart.options.axisY.title = e.chart.options.data[1].name;
			}
		}
	}

	function populationChartTooltipContent(e) {
		var content;
		content = "<strong>" + e.entries[0].dataPoint.x + "</strong> <br/>" + e.chart.options.data[0].name + ': ' + formatTooltipNumber(e.entries[0].dataPoint.y);
		return content;
	}

	function merchandiseImportsExportsChartTooltipContent(e) {
		var content;
		if (e.chart.options.data[0].visible === true) {
			if (e.chart.options.data[1].visible === false) {
				content = "<strong>" + e.entries[0].dataPoint.x + "</strong> <br/>" + "<span style= 'color:" + e.entries[0].dataSeries.color + "'> " +  "Complaints Alloted:</span> " + formatTooltipNumber(e.entries[0].dataPoint.y);
			} else {
				content = "<strong>" + e.entries[0].dataPoint.x + "</strong> <br/>" + "<span style= 'color:" + e.entries[0].dataSeries.color + "'> " +  "Complaints Alloted:</span> " + formatTooltipNumber(e.entries[0].dataPoint.y)
				+ "<br/><span style= 'color:" + e.entries[1].dataSeries.color + "'> " + "Complaints Passed-On:</span> "+ formatTooltipNumber(e.entries[1].dataPoint.y);
			}
		} else {
			if (e.chart.options.data[1].visible === false) {
				content = '';
			} else {
				content = "<strong>" + e.entries[0].dataPoint.x + "</strong>" + "<br/><span style= 'color:" + e.entries[1].dataSeries.color + "'> "+ "Complaints Passed-On:</span> " + formatTooltipNumber(e.entries[1].dataPoint.y);
			}
		}
		return content;
	}

	function formatTooltipNumber(number) {
		var suffixes = ["", "", "", "", "Thousand"];
		var order = Math.max(Math.floor(Math.log(number) / Math.log(1000)), 0);
		if (order > suffixes.length - 1)
			order = suffixes.length - 1;
		var suffix = suffixes[order];
		return CanvasJS.formatNumber(number / Math.pow(1000, order)) + ' ' + suffix;
	}

	$(window).resize(function() {
		setBubbleChartSubtitlesFontSize();
		setMerchandiseImportsExportsColumnChartAxisYTitleFontSize();
		yearSlider.noUiSlider.destroy();
		createSlider(yearArr[yearCounter]);
		bindClickEventToSliderScale();
		bindYearSliderUpdateEvent();
	});

	(function init() {
		createSlider(yearArr[0]);
		bindClickEventToSliderScale();
		bindYearSliderUpdateEvent();
		DepartmentSizeBubbleChart = createDepartmentSizeChart(getDataPoint(yearArr[0]));
		createPopulationChart("Startups");
		createWorkingPopulationChart("Startups");
		merchandiseImportsExportsColumnChart = createMerchandiseImportsExportsChart("Startups");
		setBubbleChartSubtitlesFontSize();
		setMerchandiseImportsExportsColumnChartAxisYTitleFontSize();
	})();

});
