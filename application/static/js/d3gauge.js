// d3Gauge and xtend get pulled in via browserify-cdn standalone
// see script tags
var gauges = [];
var small = {
  size: 100,
  min: 0,
  max: 50,
  transitionDuration: 500

  ,
  label: 'label.text',
  minorTicks: 4,
  majorTicks: 5,
  needleWidthRatio: 0.6,
  needleContainerRadiusRatio: 0.7

  ,
  zones: [{
    clazz: 'yellow-zone',
    from: 0.73,
    to: 0.9
  }, {
    clazz: 'red-zone',
    from: 0.9,
    to: 1.0
  }]
};

function createGauge(opts, target) {
  var el = document.createElement('div');
  el.setAttribute('class', 'gauge-container');
  target.append(el);
  var g = d3Gauge(el, opts);
  g.currentValue = g._range / 2;
  gauges.push(g);
}

function getRandomNextValue(gauge) {
  gauge.currentValue += (Math.random() - 0.5) * gauge._range / 10;
  if (gauge.currentValue < gauge._min) gauge.currentValue = gauge._min;
  if (gauge.currentValue > gauge._max) gauge.currentValue = gauge._max;
  return gauge.currentValue;
}

function updateGauges() {
  gauges.forEach(function(gauge) {
    gauge.write(getRandomNextValue(gauge));
  });
}

createGauge({
  clazz: 'simple',
  label: '',
  max: 20000,
  size: 220,
  zones: [{
    clazz: 'yellow-zone',
    from: 0,
    to: 0
  }, {
    clazz: 'red-zone',
    from: 0,
    to: 0
  }]
}, $('#altitude'));

createGauge({
  clazz: 'simple',
  label: '',
  min: -60,
  max: 30,
  size: 220,
  zones: [{
    clazz: 'blue-zone',
    from: 0,
    to: .15
  }, {
    clazz: 'lightblue-zone',
    from: .15,
    to: .25
  }]
}, $('#temperature'));

createGauge({
  clazz: 'simple',
  label: '',
  max: 1050,
  size: 220,
  zones: [{
    clazz: 'yellow-zone',
    from: 0,
    to: 0
  }, {
    clazz: 'red-zone',
    from: 0,
    to: 0
  }]
}, $('#pressure'));
