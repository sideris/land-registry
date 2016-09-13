let plentific = {};
plentific.svg = {};
plentific.svg.viewBox = function (x0, y0, x1, y1) {
	return [x0, y0, x1, y1].join(' ');
};


// class PlentificView {
//
// 	constructor(container, data) {
// 		this.container = container;
// 		this.data = data;
// 		this.height = 1024 * 1.5;
// 		this.width = 768;
// 		this.x = d3.scale.linear().range([0, this.width]);
// 		this.y = d3.scale.linear().range([this.height, 0]);
// 		this.xAxis = d3.svg.axis().scale(d3.scale.linear().range([0, width])).orient("bottom").ticks(0);
// 		this.yAxis = d3.svg.axis().scale(this.y).orient("left").ticks(0);
// 		this.svg = null;
// 		this.datum = null;
// 		this.graph = null;
// 	}
//
// 	/**
// 	 * Creates the graph
// 	 */
// 	makeGraph() {
// 		this.svg = d3.select(this.container)
// 						.append("svg")
// 							.attr("width", "100%")
// 							.attr("height", "100%")
// 							.attr("preserveAspectRatio", "xMidYMid meet")
// 							.attr("viewBox", plentific.svg.viewBox(0, 0, this.width, this.height))
// 							.classed("svg-content", true)
// 						.append('g')
// 							.attr({'width':'100%', 'height': '100%'});
// 		let name = this.container.replace('#','');
// 		d3.select(this.container).select('svg.svg-content').select('g').classed(name + '-graph', true)
//
// 	}
//
// 	updateGraph() {
//
// 	}
//
// 	parseData() {
//
// 	}
//
// 	updateDataset(ds) {
// 		this.data = ds;
// 		this.parseData();
// 		this.updateGraph();
// 	}
//
// 	/**
// 	 * Initializes the graph, data and sets up the scene
// 	 */
// 	call() {
// 		this.makeGraph();
// 		this.parseData();
// 		this.updateGraph();
// 	}
// }
