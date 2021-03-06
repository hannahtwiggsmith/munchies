// Vars for node highlighting
var toggle = 0;
var minRadius = 4;
var linkedByIndex = {};
var spread = false;
var show = false;

var w = window,
  d = document,
  e = d.documentElement,
  g = d.getElementsByTagName('body')[0],
  width = (w.innerWidth || e.clientWidth || g.clientWidth) - 100,
  height = (w.innerHeight || e.clientHeight || g.clientHeight) - 100;


var svg = d3.select("body").append("svg");

svg.attr("width", width)
  .attr("height", height);

var color = d3.scaleOrdinal(d3.schemeCategory20);

var simulation = d3.forceSimulation()
  .force("link", d3.forceLink().id(function (d) {
    return d.id;
  }).distance(function (d) {
    return 1 / (d.value) * 200;
  }).strength(1))
  .force("charge", d3.forceManyBody())
  .force("collide", d3.forceCollide(10))
  .force("center", d3.forceCenter(width / 2, height / 2));

// Define the div for the tooltip
var div = d3.select("body").append("div")
  .attr("class", "tooltip")
  .style("opacity", 0);


// Load data and make the visualization
d3.json("data/ingredients_italian.json", function (error, graph) {
  if (error) throw error;

  var link = svg.append("g")
    .attr("class", "links")
    .selectAll("line")
    .data(graph.links)
    .enter().append("line")
    .attr("stroke-width", function (d) {
      return Math.sqrt(d.value);
    });

  var node = svg.append("g")
    .attr("class", "nodes")
    .selectAll("circle")
    .data(graph.nodes)
    .enter().append("circle")
    .attr("r", chooseRadius)
    .attr("fill", function (d) {
      return color(d.group);
    })
    .on("mouseover", mouseover)
    .on("mouseout", mouseout)
    .on('dblclick', connectedNodes)
    .call(d3.drag()
      .on("start", dragstarted)
      .on("drag", dragged)
      .on("end", dragended));

  // d3.selectAll("input[name=spread]")
  //   .on("change", function () {
  //     console.log(spread);
  //     if (spread == true) {
  //       simulation.force("collide", d3.forceCollide(5));
  //       spread = false;
  //     } else {
  //       simulation.force("collide", d3.forceCollide(50));
  //       spread = true;
  //     }
  //   });
  //
  // d3.selectAll("input[name=show]")
  //   .on("change", function () {
  //     if (show == true) {
  //       yo = d3.selectAll("circle");
  //       console.log(yo);
  //       div.transition()
  //         .duration(200)
  //         .style("opacity", .9);
  //
  //       // Attach the node id to tooltip
  //       div.html(" " + node.id + " ")
  //         .style("left", (d3.event.pageX) + "px")
  //         .style("top", (d3.event.pageY - 28) + "px");
  //       show = false;
  //     } else {
  //       d3.selectAll("circle")
  //       show = true;
  //     }
  //   });


  simulation
    .nodes(graph.nodes)
    .on("tick", ticked);

  simulation.force("link")
    .links(graph.links);


  /** FORCE LAYOUT EVENT FUNCTIONS */

  function ticked() {
    link
      .attr("x1", function (d) {
        return d.source.x;
      })
      .attr("y1", function (d) {
        return d.source.y;
      })
      .attr("x2", function (d) {
        return d.target.x;
      })
      .attr("y2", function (d) {
        return d.target.y;
      });

    node
      .attr("cx", function (d) {
        return d.x;
      })
      .attr("cy", function (d) {
        return d.y;
      });
  }

  function dragstarted(d) {
    if (!d3.event.active) simulation.alphaTarget(0.3).restart();
    d.fx = d.x;
    d.fy = d.y;
  }

  function dragged(d) {
    d.fx = d3.event.x;
    d.fy = d3.event.y;
  }

  function dragended(d) {
    if (!d3.event.active) simulation.alphaTarget(0);
    d.fx = null;
    d.fy = null;
  }

  function mouseover(node) {
    // Show tooltip
    div.transition()
      .duration(200)
      .style("opacity", .9);

    // Attach the node id to tooltip
    div.html(" " + node.id + " ")
      .style("left", (d3.event.pageX) + "px")
      .style("top", (d3.event.pageY - 28) + "px");

    // Increase this node's radius by 10 pixels
    // d3.select(this).transition()
    //   .duration(0)
    //   .attr("r", this.r.animVal.value + 10);
  }

  function mouseout() {
    div.transition()
      .duration(500)
      .style("opacity", 0);
    // d3.select(this).transition()
    //   .duration(0)
    //   .attr("r", this.r.animVal.value - 10);
  }


  /* HELPER FUNCTIONS */

  for (i = 0; i < graph.nodes.length; i++) {
    linkedByIndex[i + "," + i] = 1;
  };

  graph.links.forEach(function (d) {
    linkedByIndex[d.source.index + "," + d.target.index] = 1;
  });

  function neighboring(a, b) {
    return linkedByIndex[a.index + "," + b.index];
  }

  function connectedNodes() {

    if (toggle == 0) {
      d = d3.select(this).node().__data__;
      node.style("opacity", function (o) {
        return neighboring(d, o) | neighboring(o, d) ? 1 : 0.3;
      });
      toggle = 1;
    } else {
      node.style("opacity", 1);;
      toggle = 0;
    }

  }

  function chooseRadius(d) {
    return (d.appearances / 100 > 5) ? (d.appearances / 100) : minRadius;
  }

});
