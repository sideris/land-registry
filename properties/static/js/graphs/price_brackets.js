// class PriceBracketsView extends PlentificView {
//
// }


let PriceBracketsView = function(container, data) {
	let svg;
	let datum;
	let graph;

	let width 	= 1024 * 1.5,
		height	= 768;
	let bracketSize = 8;
	let margins = {left: 20, top: 30, bottom: 100, right: 0};

	let x = d3.scale.linear().range([0, width - margins.left * 2]).domain([0, 7]),
		y = d3.scale.linear().range([height, 0]);
	let xAxis = d3.svg.axis()
					.scale(x)
					.orient("bottom")
					.ticks(bracketSize);
	let yAxis = d3.svg.axis()
					.scale(y)
					.orient("left")
					.ticks(0);
	let brackets;
	let noData = false;

	/**
	 * Makes the scaffolding for the graph
	 */
	function makeGraph() {
		svg = d3.select(container)
						.append("svg")
							.attr("width", "100%")
							.attr("height", "100%")
							.attr("preserveAspectRatio", "xMidYMid meet")
							.attr("viewBox", plentific.svg.viewBox(0, 0, width, height - margins.bottom))
							.attr('preserveAspectRatio', 'xMidYMin')
							.classed("svg-content", true)
						.append('g')
							.attr({'width':'100%', 'height': '100%'});
		graph = d3.select(container).select('svg.svg-content').select('g');
		graph.classed(container.replace('#','') + '-graph', true)
	}

	/**
	 * Updates the graph should any change occur
	 */
	function updateGraph() {
		if ( noData )
			alert('No data. Pick other range or postcode')
		else {
			graph.selectAll("bar")
				.data(datum)
				.enter().append("rect")
				.style("fill", "blue")
				.attr("x", d => x(d.x) + margins.left)
				.attr("width", (width - margins.left * 2) / bracketSize)
				.attr("y", d => height - y(d.y) )
				.attr("height", d => y(d.y) );
			graph.append("g")
				.attr("class", "x axis")
				.attr("transform", plentific.svg.translate(margins.left, height - margins.bottom - 3))
				.call(xAxis);
		}
	}

	/**
	 * Parses the data to create appropriate dataset for this graph
	 */
	function parseData() {
		let tmpData = [].concat.apply([], data.map(x =>
												x.transactions.map(y => y.price)
											)).sort();

		if (tmpData.length > 0 ) {
			brackets = d3.scale.linear().range([tmpData[0], tmpData[tmpData.length-1]]).domain([0, bracketSize - 1]);
			noData = false;
			datum = [];
			let i = 0;
			datum.push({x: i, y: tmpData.filter(x => x <= brackets(i)).length});
			for(let i=1; i < bracketSize; i++)
				datum.push({x: i, y: tmpData.filter(x => x <= brackets(i) && x > brackets(i - 1)).length})

			y.domain([ 0, Math.max.apply(Math, datum.map(x => x.y)) ]);
			console.log(datum)
		} else {
			noData = true;
		}
		// console.log(tmpData)
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