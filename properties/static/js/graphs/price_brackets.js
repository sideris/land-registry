// class PriceBracketsView extends PlentificView {
//
// }

let PriceBracketsView = function(container, data) {
	let svg;
	let datum;
	let graph;

	let height 	= 1024 * 1.5,
		width	= 768;

	let x = d3.scale.linear().range([0, width]),
		y = d3.scale.linear().range([height, 0])
	let xAxis = d3.svg.axis()
					.scale(x)
					.orient("bottom")
					.ticks(0);
	let yAxis = d3.svg.axis()
					.scale(y)
					.orient("left")
					.ticks(0);

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
		d3.select(container)
			.select('svg.svg-content')
				.select('g')
					.classed(container.replace('#','') + '-graph', true)
	}

	/**
	 * Updates the graph should any change occur
	 */
	function updateGraph() {

	}

	/**
	 * Parses the data to create appropriate dataset for this graph
	 */
	function parseData() {

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