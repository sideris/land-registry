// class PriceBracketsView extends PlentificView {
//
// }


let PriceBracketsView = function(container, data) {
	let svg;
	let datum;
	let graph;

	let width 	= 1024 * 2,
		height	= 768;
	let nBrackets = 8;
	let margin = {top: 20, right: 20, bottom: 40, left: 100};

	let x = d3.scale.linear().range([0, width]).domain([0, nBrackets - 1]),
		y2 = d3.scale.linear().range([height, 0]),
		y = d3.scale.linear().range([0, height]);
	let xAxis = d3.svg.axis()
					.scale(x)
					.orient("bottom")
					.ticks(nBrackets)
					.tickFormat(function(i){
						let p1 = i === 0 ? '0' : Math.round(Math.ceil(bracketScale(i-1)));
						let p2 = i === nBrackets - 1 ? ' and over' :  ' - ' + Math.round(Math.ceil(bracketScale(i)));
						return p1 + p2;});
	let yAxis = d3.svg.axis().scale(y2)
					.orient("left")
					.ticks(5).tickFormat(d3.format("d"));
	let bracketScale;
	let noData = false;

	/**
	 * Makes the scaffolding for the graph
	 */
	function makeGraph() {
		svg = d3.select(container)
						.append("svg")
							.attr({'width':'100%', 'height': '100%'})
							.attr("preserveAspectRatio", "xMidYMid meet")
							.attr("viewBox", plentific.svg.viewBox(	0, 0,
																	width + margin.left * 4, height + margin.top * 2))
							.classed("svg-content", true)
						.append('g')
							.attr({'width':'100%', 'height': '100%'});
		graph = d3.select(container).select('svg.svg-content').select('g');
		graph.classed(container.replace('#','') + '-graph', true);
		graph.attr('transform', plentific.svg.translate(margin.left, margin.top));
		graph.append("g").classed("background", true)
			.append("rect")
			.attr({width: width, height: height});
	}

	/**
	 * Updates the graph should any change occur
	 */
	function updateGraph() {
		if ( noData )
			alert('No data. Pick other range or postcode');
		else {
			let barW =  x(1) - x(0) - 1;
			graph.selectAll("bar")
				.data(datum)
				.enter().append("rect")
				.style("fill", "#99badd")
				.attr("x", (d, i) => x(d.x) - barW)
				.attr("width", barW)
				.attr("y", d => height - y(d.y) )
				.attr("height", d => y(d.y) );
			graph.append("g")
				.attr("class", "x axis")
				.attr("transform", plentific.svg.translate(0, height))
				.call(xAxis);
			graph.append("g")
				.attr("class", "y axis")
				.attr("transform", plentific.svg.translate(0, 0))
				.call(yAxis);

			graph.select('.x.axis')
				.selectAll('.tick')
				.attr('transform', i => plentific.svg.translate(barW * (i - 0.5), 0))
		}
	}

	/**
	 * Parses the data to create appropriate dataset for this graph
	 */
	function parseData() {
		let salePrices = [].concat.apply([], data.map(x =>
												x.transactions.map(y => y.price)));
		salePrices = salePrices.sort((a,b) => a - b);
		console.log(salePrices)
		console.log(data)
		if (salePrices.length > 0 ) {
			bracketScale = d3.scale.linear().range([0, salePrices[salePrices.length-1]]).domain([0, nBrackets]);
			noData = false;
			datum = [];
			let i = 0;
			datum.push({x: i, y: salePrices.filter(x => x < bracketScale(i)).length})

			for(i=1; i < nBrackets - 1; i++){
				datum.push({x: i, y: salePrices.filter(x => x >= bracketScale(i-1) && x < bracketScale(i)).length})
			}
			datum.push({x: i, y: salePrices.filter(x => x >= bracketScale(i-1)).length})
			y.domain([0, Math.max.apply(Math, datum.map(x => x.y))]);
			y2.domain([0, Math.max.apply(Math, datum.map(x => x.y))]);
		} else {
			noData = true;
		}
	}

	/**
	 * Updates the dataset and the graph
	 * @param dataset The new dataset
	 */
	this.updateDataset = function(dataset) {
		data = dataset;
		parseData();
		updateGraph();
	};

	/**
	 * Creates the view
	 */
	this.call = function() {
		makeGraph();
		parseData();
		updateGraph();
	}

};