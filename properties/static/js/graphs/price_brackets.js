// class PriceBracketsView extends PlentificView {
//
// }


let PriceBracketsView = function(container, data) {
	let svg;
	let datum;
	let graph;

	let height 	= 1024 * 1.5,
		width	= 768;
	let bracketSize = 8;

	let x = d3.scale.linear().range([0, width]).domain([0, 7]),
		y = d3.scale.linear().range([height, 0]);
	let xAxis = d3.svg.axis()
					.scale(x)
					.orient("bottom")
					.ticks(0);
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
							.attr("viewBox", plentific.svg.viewBox(0, 0, width, height))
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
			y.domain([0, tmpData[tmpData.length-1]]);
			noData = false;
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