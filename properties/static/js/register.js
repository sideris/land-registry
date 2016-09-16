let register = {
	svg: {},
	ajax: {},
	date: {},
	view: {},
	utils: {}
};

register.date.format = 'YYYY-MM-DD';
register.svg.viewBox = function (x0, y0, x1, y1) {
	return [x0, y0, x1, y1].join(' ');
};
register.svg.translate = function(x, y) {
	return 'translate(' + x +','+ y + ')';
};

register.ajax.get = function(url, callback) {
	d3.json(url)
		.header("X-REQUESTED-WITH", "XMLHttpRequest")
		.on("beforesend",	function()		{;})
		.on("load",			function(json)	{callback(null, json)})
		.on("error",		function(error)	{callback(error, null)})
		.get();
};

register.view.showMessage = function(msg='', cl='error', duration=2000) {
	$('#message').html(msg).addClass(cl).fadeIn(duration, function () {
		$(this).fadeOut(duration/3)
	});
};

/**
 * Removes all outliers that are 3 std from the mean
 * @param arr The sorted value array
 */
register.utils.removeOutliers = function(arr) {
	let sum=0,
		sumsq = 0; // stores sum of squares
	let l = arr.length;
	for(var i=0;i<l;++i) {
		sum		+=arr[i];
		sumsq	+=arr[i] * arr[i];
	}
	let mean 		= sum / l;
	let variance 	= sumsq / l - mean * mean;
	let sd 			= Math.sqrt(variance);

	let data3 = [];
	for(let i=0;i<l;++i) {
		if(arr[i] > mean - 3 *sd && arr[i] < mean + 3 * sd)
			data3.push(arr[i]);
	}
	return data3;
};

/**
 * Gets all outliers that are 3 std from the mean
 * @param arr The sorted value array
 */
register.utils.getOutliers = function(arr, sigma=3) {
	let sum=0,
		sumsq = 0; // stores sum of squares
	let l = arr.length;
	for(var i=0;i<l;++i) {
		sum		+=arr[i];
		sumsq	+=arr[i] * arr[i];
	}
	let mean 		= sum / l;
	let variance 	= sumsq / l - mean * mean;
	let sd 			= Math.sqrt(variance);

	let outliers = [];
	for(let i=0;i<l;++i) {
		if(arr[i] <= mean - sigma *sd || arr[i] >= mean + sigma * sd)
			outliers.push(arr[i]);
	}
	return outliers;
};
