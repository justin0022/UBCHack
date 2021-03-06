$( document ).ready(function() {
    var margin = {top: 20, right: 120, bottom: 20, left: 120},
    width = 1920 - margin.right - margin.left,
    height = 900 - margin.top - margin.bottom;

    var i = 0,
        duration = 750,
        root;

    var tree = d3.layout.tree()
        .size([height, width]);

    var diagonal = d3.svg.diagonal()
        .projection(function(d) { return [d.y, d.x]; });

    var svg = d3.select("tree1").append("svg")
        .attr("width", width + margin.right + margin.left)
        .attr("height", height + margin.top + margin.bottom)
        .append("g")
        .attr("transform", "translate(" + margin.left + "," + margin.top + ")");
    
    //initialize the tip for on hover
    var tip = d3.tip()
        .attr('class', 'd3-tip')
        .html(function(d) { 
            return "<strong>Events:</strong> <span style='color: white;'>" + d.hit + "</span>"; 
        });
    svg.call(tip);

    d3.json("data_with_vertical_hits_multilevel.json", function(error, flare) {
    if (error) throw error;

    root = flare;
    root.x0 = height / 2;
    root.y0 = 0;

    function collapse(d) {
        if (d.children) {
        d._children = d.children;
        d._children.forEach(collapse);
        d.children = null;
        }
    }

    root.children.forEach(collapse);
    update(root);
    });

    d3.select(self.frameElement).style("height", "800px");

    function update(source) {

    // Compute the new tree layout.
    var nodes = tree.nodes(root).reverse(),
        links = tree.links(nodes);

    // Normalize for fixed-depth.
    nodes.forEach(function(d) { d.y = d.depth * 360; });

    // Update the nodes…
    var node = svg.selectAll("g.node")
        .data(nodes, function(d) { 
            return d.id || (d.id = ++i); 
        });

    // Enter any new nodes at the parent's previous position.
    var nodeEnter = node.enter().append("g")
        .attr("class", "node")
        .attr("transform", function(d) { return "translate(" + source.y0 + "," + source.x0 + ")"; })
        .on("click", click);

    nodeEnter.append("circle")
        .attr("r", 1e-6)
        .style("fill", function(d) { return d._children ? "#186175" : "#fff"; })
        .on('mouseover', tip.show)
        .on('mouseout', tip.hide);

    nodeEnter.append("text")
        .attr("x", function(d) { return d.children || d._children ? -10 : 10; })
        .attr("dy", ".35em")
        .attr("text-anchor", function(d) { return d.children || d._children ? "end" : "start"; })
        .text(function(d) { return d.name; })
        .style("fill-opacity", 1e-6);

    // Transition nodes to their new position.
    var nodeUpdate = node.transition()
        .duration(duration)
        .attr("transform", function(d) { return "translate(" + d.y + "," + d.x + ")"; });

    nodeUpdate.select("circle")
        .attr("r", function(d) { 
            if (d.hit && d.category === "vertical") {
                return d.hit/2000;
            } 
            if (d.hit && d.category === "sequential") {
                return d.hit/2000;
            }
            if (d.hit && d.category === "chapter") {
                return d.hit/6000;
            }
            if (d.category === "vertical" || d.category === "sequential" || d.category === "chapter") {
                return 1e-6;
            }
            else return 4.5;
        })
        .style("fill", function(d) 
            { 
                if (!d.hit && d.category === "vertical") {
                    return "#c61b00";
                } 
                else 
                return d._children ? "#186175" : "#fff"; 
            });
    
    nodeUpdate.select("text")
        .style("fill-opacity", 1);
    
        
    // Transition exiting nodes to the parent's new position.
    var nodeExit = node.exit().transition()
        .duration(duration)
        .attr("transform", function(d) { return "translate(" + source.y + "," + source.x + ")"; })
        .remove();

    nodeExit.select("circle")
        .attr("r", 1e-6);

    nodeExit.select("text")
        .style("fill-opacity", 1e-6);

    // Update the links…
    var link = svg.selectAll("path.link")
        .data(links, function(d) { return d.target.id; });

    // Enter any new links at the parent's previous position.
    link.enter().insert("path", "g")
        .attr("class", "link")
        .attr("d", function(d) {
            var o = {x: source.x0, y: source.y0};
            return diagonal({source: o, target: o});
        });

    // Transition links to their new position.
    link.transition()
        .duration(duration)
        .attr("d", diagonal);

    // Transition exiting nodes to the parent's new position.
    link.exit().transition()
        .duration(duration)
        .attr("d", function(d) {
            var o = {x: source.x, y: source.y};
            return diagonal({source: o, target: o});
        })
        .remove();

    // Stash the old positions for transition.
    nodes.forEach(function(d) {
            d.x0 = d.x;
            d.y0 = d.y;
        });
    }
   
    // Toggle children on click.
    function click(d) {
        if (d.children) {
            d._children = d.children;
            d.children = null;
        } else {
            d.children = d._children;
            d._children = null;
        }
        update(d);
    }
    
    
});