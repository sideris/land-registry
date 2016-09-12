let plentific = {};
plentific.svg = {};
plentific.svg.viewBox = function (x0, y0, x1, y1) {
	return [x0, y0, x1, y1].join(' ');
};


class PlentificView {

	constructor(container, data) {
		this.container = container;
		this.data = data;
		this.svg = null;
		this.datum = null;
		this.graph = null;
	}

	/**
	 * Creates the graph
	 */
	makeGraph() {
		let height = 1024 * 1.5, width = 768;
		this.svg = d3.select(this.container)
						.append("svg:svg")
							.attr("width", "100%")
							.attr("height", "100%")
							.attr("preserveAspectRatio", "xMidYMid meet")
							.attr("viewBox", plentific.svg.viewBox(0, 0, width, height))
							.classed("svg-content", true);
		this.graph = this.svg
							.append('g')
								.attr({'width':'100%', 'height': '100%'})
								.classed(this.container + '-view', true)
	}

	updateGraph() {

	}

	parseData() {

	}

	updateDataset(ds) {
		this.data = ds;
		this.parseData();
		this.updateGraph();
	}

	/**
	 * Initializes the graph, data and sets up the scene
	 */
	call() {
		this.makeGraph();
		this.parseData();
		this.updateGraph();
	}
}
