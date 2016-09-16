let PropertyTypesView = function(container, data) {
	let svg;
	let datum;
	let graph;
	const width 	= 1024 * 2,
		height	= 768;
	const margin = {top: 20, right: 20, bottom: 40, left: 100};

	let startDate	= new Date("2200"),
		endDate 	= new Date("1900");

	let x = d3.time.scale.utc().range([0, width]),
		y = d3.scale.linear().range([height, 0]),
		col = d3.scale.category10()
	let xAxis = d3.svg.axis().scale(x).orient("bottom").ticks(10).tickFormat(d3.time.format("%d/%b/%Y")),
		yAxis = d3.svg.axis().scale(y).orient("left").ticks(5).tickFormat(d3.format("d"));
	let noData = false;

	const line = d3.svg.line()
		.interpolate("basis")
		.x( d => x(d.date) )
		.y(d => y(d.price));
	const typeMap = {	D: 'Detached', S: 'Semi detached', T: 'Terraced', F: 'Flats  / Maisonnetes', O: 'Other' }; //should come from API
	/**
	 * Makes the scaffolding for the graph
	 */
	function makeGraph() {
		svg = d3.select(container)
						.append("svg")
							.attr({'width':'100%', 'height': '100%'})
							.attr("preserveAspectRatio", "xMidYMid meet")
							.attr("viewBox", register.svg.viewBox(	0, 0,
																	width + margin.left * 4, height + margin.top * 2))
							.classed("svg-content", true)
						.append('g')
							.attr({'width':'100%', 'height': '100%'});
		graph = d3.select(container).select('svg.svg-content').select('g');
		graph.classed(container.replace('#','') + '-graph', true);
		graph.attr('transform', register.svg.translate(margin.left, margin.top));
		graph.append("g").classed("background", true)
			.append("rect")
			.attr({width: width, height: height});
	}

	/**
	 * Updates the graph should any change occur
	 */
	function updateGraph() {
		if ( noData === false ) {

			let ptypes = graph
				.selectAll(".property-type")
				.data(datum)
				.enter().append("g")
					.attr("class", "property-type");
			ptypes.append('path')
					.attr('class', 'line')
					.attr('d', d =>  line(d.fixed))
					.style("stroke", (d, i) => col(i) );
			ptypes.append("text")
				  .datum(function(d) { return {label: d.label, value: d.fixed[d.fixed.length - 1]}; })
				  .attr("transform", function(d) { if(d.value) return "translate(" + x(d.value.date) + "," + y(d.value.price) + ")"; })
				  .attr("x", 3)
				  .attr("dy", ".35em")
				  .text(function(d) {
					  if(d.value)
						  return d.label;
					  return '';
				  });

			graph.append("g")
				.attr("class", "x axis")
				.attr("transform", register.svg.translate(0, height))
				.call(xAxis);
			graph.append("g")
				.attr("class", "y axis")
				.attr("transform", register.svg.translate(0, 0))
				.call(yAxis);
		}
	}

	/**
	 * Parses the data to create appropriate dataset for this graph
	 */
	function parseData() {
		startDate	= new Date("2200");
		endDate 	= new Date("1900");
		let byType = {};
		let minY = 10000000000, maxY = 0;
		datum = [];
		let outliers;
		for(let key of Object.keys(typeMap)) {
			byType[key] = []
							.concat.apply([], data
											.filter(x => x.property_type === key).map(x => x.transactions))
											.map(x => {
												minY = x.price < minY ? x.price : minY;
												maxY = x.price > maxY ? x.price : maxY;
												return { price: x.price, date: moment(x.transfer_date).toDate()};})
											.sort((a, b) => +(a.date) - +(b.date));
			let l = byType[key].length;
			// find the mean
			let avg;
			if(l > 0) {
				let prices = [].concat.apply([], byType[key].map(x=> x.price)).sort((a,b) => a-b);
				outliers = register.utils.getOutliers(prices, 2);
				let nextMonth = moment(byType[key][0].date).add(1, 'months').set('date', 1).toDate();
				startDate = +(byType[key][0].date) < +startDate ? byType[key][0].date : startDate;
				endDate = +(byType[key][l - 1].date) > +endDate ? byType[key][l - 1].date : endDate;
				let sum = 0;
				let c = 0;
				for(let i=0; i < l; i++) {
					if(outliers.indexOf(byType[key].price) > -1) continue;
					if( +byType[key][i].date >  +nextMonth) {
						sum = 0;
						nextMonth = moment(nextMonth).add(1, 'months').toDate();
						c =0;
					}
					c++;
					sum += byType[key][i].price
				}
				avg = sum / c;
			}
			datum.push( {label: typeMap[key], values: byType[key].filter(x=> outliers.indexOf(x.price) === -1), mean: avg} )
		}
		// make datum
		datum.forEach(function(d){
			d.fixed = [];
			for(let i=0; i<d.values.length;i++) {
				let price = outliers.indexOf(d.values[i].price) > - 1 ? 0 : 100 * d.values[i].price / d.mean;
				d.fixed.push({date: d.values[i].date, price:  price});
			}
		});
		var normalizedYMax = Math.max.apply( Math, [].concat.apply([], datum.map(x=> x.fixed.map(y=>y.price))));

		y.domain([0, normalizedYMax]);
		x.domain([startDate, endDate]);
		graph.select('.x.axis').transition().duration(1500).ease("sin-in-out").call(xAxis);
		graph.select('.y.axis').transition().duration(1500).ease("sin-in-out").call(yAxis);
	}

	/**
	 * Updates the dataset and the graph
	 * @param dataset The new dataset
	 */
	this.updateDataset = function(dataset) {
		data = dataset;
		graph.selectAll('.axis').remove();
		d3.selectAll('.property-type').remove();
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