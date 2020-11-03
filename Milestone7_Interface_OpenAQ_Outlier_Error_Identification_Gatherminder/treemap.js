// code adapted from http://codepen.io/boars/pen/JjILy
/* doesn't look any different from Bostock's orginal treemap */
/* now enough tweaking that code has significant differences from both versions */

var margin = {
    top: 25,
    right: 0,
    bottom: 0,
    left: 0
  },
  width = 960,
  height = 500 - margin.top - margin.bottom,
  formatNumber = d3.format(",d"),
  transitioning;

var xScale = d3.scale.linear()
  .domain([0, width])
  .range([0, width]);

var yScale = d3.scale.linear()
  .domain([0, height])
  .range([0, height]);

var treemap = d3.layout.treemap()
  .children(function(d, depth) { return depth ? null : d._children;})
  .sort(function(a, b) {return a.value - b.value;})
  //.ratio(height / width * 0.5 * (1 + Math.sqrt(5)))
  .round(false);

var svg = d3.select("#treeMapChart").append("svg")
  .attr("width", width + margin.left + margin.right)
  .attr("height", height + margin.bottom + margin.top)
  .style("margin-left", -margin.left + "px")
  .style("margin.right", -margin.right + "px")
  .append("g")
  .attr("transform", "translate(" + margin.left + "," + margin.top + ")")
  .style("shape-rendering", "crispEdges");

var grandparent = svg.append("g")
  .attr("class", "grandparent");

grandparent.append("rect")
  .attr("y",-margin.top)
  .attr("width", width)
  .attr("height", margin.top);

grandparent.append("text")
  .attr("x", 6)
  .attr("y", 6 - margin.top)
  .attr("dy", ".75em");

var div = d3.select("body").append("div")   
  .attr("class", "tooltip")               
  .style("opacity", 0);

function drawTreeMap(inputJSON) {

  //"testdata.js"
  //  var root = JSON.parse(inputJSON);
  var root = inputJSON;
  //d3.json(inputJSON, function(root) {
    initialize(root);
    accumulate(root);
    layout(root);
    display(root);


    //console.log(root);
    //console.log(root.classDistribution);
    console.log("root height: "+root.height);

    function initialize(root) {
      root.x = root.y = 0;
      root.dx = width;
      root.dy = height;
      root.depth = 0;
    }

    // Aggregate the values for internal nodes. This is normally done by the
    // treemap layout, but not here because of our custom implementation.
    // We also take a snapshot of the original children (_children) to avoid
    // the children being overwritten when when layout is computed.

    /* Bostock's original function
      function accumulate(d) {
        return (d._children = d.children)
          ? d.value = d.children.reduce(function(p, v) { return p + accumulate(v); }, 0)
          : d.value;
      }
    */
    function accumulate(d) {

      // does depth first traversal on tree 4 times, could be a lot more efficient
      if(d._children=d.children)
      {
        d.value = d.children.reduce(function(p, v) {
          return p + accumulate(v).value;
        }, 0);

        d.height = d.children.reduce(function(p, v) {
          return Math.max(p, 1+accumulate(v).height);
        }, 1);

        d.topTargetCount = d.children.reduce(function(p, v) {
          return p + accumulate(v).topTargetCount;
        }, 0);

        d.classDistribution = d.children.reduce(function(p, v) {
          return joinAddDictionaries(p, accumulate(v).classDistribution);
        }, {});
      }

      //console.log(d.classDistribution);
      return {'value': d.value, 
              'topTargetCount': d.topTargetCount,
              'height': d.height,
              'classDistribution': d.classDistribution};
    }

    // merge two dictionaries (values must be numeric), adding any common keys they have
    function joinAddDictionaries(d1, d2)
    {
      var joined = {};
      for (var key in d1) {
        if (d1.hasOwnProperty(key)) {
          if(!joined.hasOwnProperty(key)) joined[key] = 0;
          joined[key] +=  d1[key];
        }
      }

      for (var key in d2) {
        if (d2.hasOwnProperty(key)) {
          if(!joined.hasOwnProperty(key)) joined[key] = 0;
          joined[key] +=  d2[key];
        }
      }

      return joined;
    }
    // Compute the treemap layout recursively such that each group of siblings
    // uses the same size (1×1) rather than the dimensions of the parent cell.
    // This optimizes the layout for the current zoom state. Note that a wrapper
    // object is created for the parent node for each group of siblings so that
    // the parent’s dimensions are not discarded as we recurse. Since each group
    // of sibling was laid out in 1×1, we must rescale to fit using absolute
    // coordinates. This lets us use a viewport to zoom.
    function layout(d) {
      if (d._children) {
        treemap.nodes({_children: d._children});
        d._children.forEach(function(c) {
          c.x = d.x + c.x * d.dx;
          c.y = d.y + c.y * d.dy;
          c.dx *= d.dx;
          c.dy *= d.dy;
          c.parent = d;
          layout(c);
        });
      }
    }

    function display(d) {
      grandparent
        .datum(d.parent)
        .on("click", transition)
        .select("text")
        .text(decisionTreeNodeToTextRule(d) + (d._children[0].attributeName ? " / " + d._children[0].attributeName : ""));

      //console.log(d);

      var g1 = svg.insert("g", ".grandparent")
        .datum(d)
        .attr("class", "depth");

      var g = g1.selectAll("g")
        .data(d._children)
        .enter().append("g");

      g.filter(function(d) {return d._children;})
        .classed("children", true)
        .on("click", transition);

      var childRects = g.selectAll(".child")
        .data(function(d) {return d._children || [d];})
        .enter().append("rect")
        .attr("class", "child")
        .call(rect);

      g.append("rect")
        .attr("class", "parent")
        .call(rect)
        .append("title")
        .text(function(d) {return formatNumber(d.value);});

      g.append("text")
        .attr("dy", ".75em")
        .text(function(d) {
          //console.log(d.classDistribution);
          return d.name + ' (' + d.value + ')';
        })
        .call(text);

      //drawDots(d, g1);

      // tooltip code from http://www.d3noob.org/2013/01/adding-tooltips-to-d3js-graph.html
      // positioning code from http://stackoverflow.com/questions/16770763/mouse-position-in-d3
      // and http://jsfiddle.net/WLYUY/7/

      function transition(d) {
        if (transitioning || !d) return;
        transitioning = true;

        var g2 = display(d),
          t1 = g1.transition().duration(500),
          t2 = g2.transition().duration(500);

        // Update the domain only after entering new elements.
        xScale.domain([d.x, d.x + d.dx]);
        yScale.domain([d.y, d.y + d.dy]);

        // Enable anti-aliasing during the transition.
        svg.style("shape-rendering", null);

        // Draw child nodes on top of parent nodes.
        svg.selectAll(".depth").sort(function(a, b) {
          return a.depth - b.depth;
        });

        // Fade-in entering text.
        g2.selectAll("text").style("fill-opacity", 0);

        drawDots(d, g2);

        // Transition to the new view.
        t1.selectAll("text").call(text).style("fill-opacity", 0);
        t2.selectAll("text").call(text).style("fill-opacity", 1);
        t1.selectAll("rect").call(rect);
        t2.selectAll("rect").call(rect);

        // Remove the old node when the transition is finished.
        t1.remove().each("end", function() {
          svg.style("shape-rendering", "crispEdges");
          transitioning = false;
        });

        d3.selectAll("rect")
        .on("mouseover", function(d) {      
          div.transition()   
              .duration(200)      
              .style("opacity", .9);

          // the "grandparent" (path to node) bar on top doesn't have a value
          if(d.value!==undefined)
            div.html(d.attributeName+" = " + d.name + "<br />" + d.value +" data points.<br/>")  
                .style("left", (parseInt(d3.select(this).attr("x")) + document.getElementById("treeMapChart").offsetLeft + 60) + "px")
                .style("top", (parseInt(d3.select(this).attr("y")) + document.getElementById("treeMapChart").offsetTop + 60) + "px");
        })                
        .on("mouseout", function(d) {       
            div.transition()        
                .duration(500)      
                .style("opacity", 0);   
        });

      }

      return g;
    }

    function text(text) {
      text.attr("x", function(d) {
          return xScale(d.x) + 6;
        })
        .attr("y", function(d) {
          return yScale(d.y) + 6;
        });
    }

    function rect(rect) {
      rect.attr("x", function(d) {return xScale(d.x);})
        .attr("y", function(d) {return yScale(d.y);})
        .attr("width", function(d) {return xScale(d.x + d.dx) - xScale(d.x);})
        .attr("height", function(d){return yScale(d.y + d.dy) - yScale(d.y);})
        .attr("fill", function(d){return purityColour(d.classDistribution);})
    }

    function drawDots(d, g2)
    {
      //console.log(d);
      var dChildren = d._children;
      if(dChildren!==undefined) 
      {
        for(var i=0;i<dChildren.length; i++)
        {
          var dGrandchildren = dChildren[i]._children;
          if(dGrandchildren!==undefined) 
          {
            for(var j=0;j<dGrandchildren.length;j++)
            {
              //console.log(dGrandchildren[j].value);
              for(var k=0;k<dGrandchildren[j].value;k++)
              {
                //console.log(dGrandchildren[j]);

                xWidth = xScale(dGrandchildren[j].x + dGrandchildren[j].dx) - xScale(dGrandchildren[j].x);
                yHeight = yScale(dGrandchildren[j].y + dGrandchildren[j].dy) - yScale(dGrandchildren[j].y);
                //console.log('xEnd is '+xEnd);
                //console.log('yEnd is '+yEnd);

                xPos = xScale(dGrandchildren[j].x)+((k+1)*15)%xWidth;
                //yPos = yScale(dGrandchildren[j].y)+(Math.random()*10)+(Math.ceil(((k+1)*15)/xWidth)*20)%yHeight;
                yPos = yScale(dGrandchildren[j].y)+(Math.ceil(((k+1)*15)/xWidth)*20)%yHeight; // no noise version

                g2.append("circle")
                  .attr("class", "dot")
                  .attr("r", ((((root.height-dGrandchildren[j].height)-0)*6)/root.height)+0.5) // simple range conversion: NewValue = (((OldValue - OldMin) * NewRange) / OldRange) + NewMin
                  .attr("cx", xPos)
                  .attr("cy", yPos)
                  .style("fill", function(d) {return darkerPurityColour(dGrandchildren[j].classDistribution);})
              }
            }
          }
        }
      }
    }

    function randInterval(min,max)
    {
      return Math.round((Math.random()*max)+min);
    }
    function purityColour(distribution)
    {
      // got help from http://hslpicker.com/#fff

      if(distribution['interesting']===undefined || distribution['interesting']===0)
      {
        return 'hsl(200, 100%, 100%)';
      }
      else if(distribution['not interesting']===undefined || distribution['not interesting']===0)
      {
        return 'hsl(200, 100%, 40%)';
      }
      else
      {
        var notInterestingProportion = distribution['not interesting']/(distribution['interesting']+distribution['not interesting']);
        var lightness = 40+Math.round(notInterestingProportion*60);
        return 'hsl(200, 100%, '+lightness+'%)';
      }
    }

    // same as purityColour but reduces lightness by 10% and transparency added
    function darkerPurityColour(distribution)
    {
      // got help from http://hslpicker.com/#fff

      if(distribution['interesting']===undefined || distribution['interesting']===0)
      {
        return 'hsla(200, 100%, 90%, 0.5)';
      }
      else if(distribution['not interesting']===undefined || distribution['not interesting']===0)
      {
        return 'hsla(200, 100%, 30%, 0.5)';
      }
      else
      {
        var notInterestingProportion = distribution['not interesting']/(distribution['interesting']+distribution['not interesting']);
        var lightness = 30+Math.round(notInterestingProportion*60);
        return 'hsla(200, 100%, '+lightness+'%, 0.5)';
      }
    }

    function decisionTreeNodeToTextRule(d) {

      if(d.parent === undefined)
        return d.attributeName + "=" + d.name;
      else
        return decisionTreeNodeToTextRule(d.parent) + " / " + d.attributeName + "=" + d.name;
      
      //return d.parent ?
      //  name(d.parent) + " / " + d.name :
      //  d.name;
    }
  //});
}