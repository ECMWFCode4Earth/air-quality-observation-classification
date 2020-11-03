//ID3 Decision Tree Algorithm


//main algorithm and prediction functions

var id3 = function(_s,target,features){

    // unique values of target attribute seen in _s
    var targets = _.unique(_s.pluck(target));

    // neat trick to create dictionary of occurrences from http://stackoverflow.com/questions/5667888/counting-the-occurrences-of-javascript-array-elements
    // if exactly one value, i.e. _s is now a pure single-class dataset
    if (targets.length == 1){
	   //console.log("end node! "+targets[0]);
       //console.log(_s.size());
       //console.log(_s);
       //console.log(_.countBy(_s.pluck(target), _.identity));
	   return { 
            type:"result",
            val: targets[0],
            name: targets[0],
            topTargetCount: _s.size(),
            totalCount: _s.size(),
            classDistribution: _.countBy(_s.pluck(target), _.identity),
            alias:targets[0]+randomTag() 
        }; 
    }

    // if no more features remain to be split on
    if(features.length == 0){
	   //console.log("returning the most dominant feature");
       //console.log(_.size(_s));
       //console.log(_s);
	   var topTarget = mostCommon(_s.pluck(target));
       console.log('Top Target '+topTarget);
	   return {
            type:"result", 
            val: topTarget, 
            name: topTarget,
            // count how many instances of topTarget in _s.pluck(target)
            topTargetCount: _s.pluck(target).reduce(function(a,b){(b===topTarget)?a+1:a},0),
            classDistribution: _.countBy(_s.pluck(target), _.identity),
            totalCount: _s.size(),
            alias: topTarget+randomTag()
        };
    }

    var bestFeature = maxGain(_s,target,features);
    var remainingFeatures = _.without(features,bestFeature);
    var possibleValues = _.unique(_s.pluck(bestFeature));
    
    //console.log("node for "+bestFeature);
    var node = {name: bestFeature, alias: bestFeature+randomTag()};
    node.type = "feature";
    node.vals = _.map(possibleValues,function(v){
    	//console.log("creating a branch for "+v);
    	var _newS = _(_s.filter(function(x) {return x[bestFeature] == v}));
    	
        var child_node = {
            name: v, 
            alias: v+randomTag(), 
            type: "feature_value"
        };
    	
        child_node.child =  id3(_newS,target,remainingFeatures);

        //child_node.topTargetCount = 0;
        //child_node.totalCount = 0;
        //console.log(child_node.child);

        //_.each(child_node.child.vals, function(v){
        //    if(v.topTargetCount===undefined) console.log(v);
        //    child_node.topTargetCount += v.topTargetCount; 
        //    child_node.totalCount += v.totalCount;
        //});

    	return child_node;
    });

    /*
        node.topTargetCount = 0;
        node.totalCount = 0;
        _.each(node.vals, function(v){
            //if(v.topTargetCount===undefined) console.log(v);
            node.topTargetCount += v.topTargetCount; 
            node.totalCount += v.totalCount;
        });
    */

    return node;
}

var predict = function(id3Model,sample) {
    var root = id3Model;
    while(root.type != "result"){
    	var attr = root.name;
    	var sampleVal = sample[attr];
    	var childNode = _.detect(root.vals,function(x){return x.name == sampleVal});
    	root = childNode.child;
    }
    return root.val;
}



//necessary math functions

var entropy = function(vals){
    var uniqueVals = _.unique(vals);
    var probs = uniqueVals.map(function(x){return prob(x,vals)});
    var logVals = probs.map(function(p){return -p*log2(p) });
    return logVals.reduce(function(a,b){return a+b},0);
}

var gain = function(_s,target,feature){
    var attrVals = _.unique(_s.pluck(feature));
    var setEntropy = entropy(_s.pluck(target));
    var setSize = _s.size();
    var entropies = attrVals.map(function(n){
	var subset = _s.filter(function(x){return x[feature] === n});
	return (subset.length/setSize)*entropy(_.pluck(subset,target));
    });
    var sumOfEntropies =  entropies.reduce(function(a,b){return a+b},0);
    return setEntropy - sumOfEntropies;
}

var maxGain = function(_s,target,features){
    return _.max(features,function(e){return gain(_s,target,e)});
}

var prob = function(val,vals){
    var instances = _.filter(vals,function(x) {return x === val}).length;
    var total = vals.length;
    return instances/total;
}

var log2 = function(n){
    return Math.log(n)/Math.log(2);
}


var mostCommon = function(l){
   return  _.sortBy(l,function(a){
	return count(a,l);
    }).reverse()[0];
}

var count = function(a,l){
    return _.filter(l,function(b) { return b === a}).length
}

var randomTag = function(){
    return "_r"+Math.round(Math.random()*1000000).toString();
}

/* END ID3 ALGORITHM */


//Display logic

/* old method using google charts
    var drawGraph = function(id3Model,divId){
        var g = new Array();
        g = addEdges(id3Model,g).reverse();
        window.g = g;
        var data = google.visualization.arrayToDataTable(g.concat(g));
        var chart = new google.visualization.OrgChart(document.getElementById(divId));
        google.visualization.events.addListener(chart, 'ready',function(){
        _.each($('.google-visualization-orgchart-node'),function(x){
    	var oldVal = $(x).html();
    	if(oldVal){
    	    var cleanVal = oldVal.replace(/_r[0-9]+/,'');
    	    $(x).html(cleanVal);
    	}
    }); 
        });
        chart.draw(data, {allowHtml: true});

    }
*/

var allLeavesNotInteresting = function(node)
{
    if(node.type=='feature')
    {
        var truthAccumulator = true;
        _.each(node.vals,function(m){
            truthAccumulator = truthAccumulator && allLeavesNotInteresting(m);
        });
        return truthAccumulator;
    }
    if(node.type=='feature_value')
    {
        if(node.child.name==='not interesting') return true;
        else return false;
    }
}

// returns simplified version of tree to feed into D3 tree visualisation
var simpleTreeJSON = function(node)
{
    //console.log(node);
    if(node.type=='feature')
    {
        var simple = {'name':node.name,
                      'children': new Array(),
                      'value':1
                     };
        _.each(node.vals,function(m){
            simple.children.push(simpleTreeJSON(m));
        });

        return simple;
    }
    if(node.type=='feature_value')
    {

        var simple = {'name':node.name,
                      'children': [simpleTreeJSON(node.child)],
                      'value':1
                     };
        return simple;
    }
    if(node.type=='result')
    {
        var simple = {'name':node.name, 'value':1};
        return simple;
    }
}

var simpleTreeMapJSON = function(node)
{
    //console.log(node);
    if(node.type=='feature')
    {
        var simple = {'name':node.name,
                      'children': new Array(),
                      'value':0,
                      'topTargetCount': node.topTargetCount,
                     };
        _.each(node.vals,function(m){
            simple.children.push(simpleTreeMapJSON(m));
        });

        var kids = new Array();
        _.each(node.vals,function(m){
            kids.push(simpleTreeMapJSON(m));
        });

        _.each(kids, function(k) {
            k.attributeName = node.name;
            //k.name = node.name+'='+k.name;
        });

        //console.log(kids);
        //return simple;

        // we create simple but throw it away and use kids
        // this flattens down the useless 'feature' nodes
        return kids;
    }
    if(node.type=='feature_value')
    {
        var tempTree = simpleTreeMapJSON(node.child);
        var tempTreeIsArray = Object.prototype.toString.call(tempTree)==='[object Array]';

        var simple = {'name':node.name,
                      'children': tempTreeIsArray ? tempTree:[tempTree],
                      'value':0,
                      'height':0,
                      'topTargetCount': node.topTargetCount,
                     };

        return simple;
    }
    if(node.type=='result')
    {
        var simple = {
            'name':node.name, 
            'value':node.totalCount,
            'height':0,
            'topTargetCount':node.topTargetCount,
            'classDistribution':node.classDistribution
        };
        return simple;
    }
}

// takes as its input a tree in the format of the OUTPUT of simpleTreeMapJSON
// AFTER it has been put through the accumulate function
var treeAsScatterPoints = function(node,depth,xyz)
{
    //console.log(node);
    //console.log(xyz);
    nodeAcc = accumulate(node);
    if(node.children===undefined)
    {
        //console.log('leaf');
        xyz[0].push(nodeAcc.value);
        xyz[1].push(entropyFromDistribution(nodeAcc.classDistribution));
        xyz[2].push(depth);
    }
    else
    {
        xyz[0].push(nodeAcc.value);
        xyz[1].push(entropyFromDistribution(nodeAcc.classDistribution));
        xyz[2].push(depth);

        _.each(node.children, function(c) {
            treeAsScatterPoints(c,depth+1,xyz);
        });
    }
    
    return xyz;
}

function entropyFromDistribution(distribution) {
    var repeatedSamples = [];
    for(var key in distribution) {
        if(distribution.hasOwnProperty(key))
        {
            // Array(n).fill(value) creates an array of length n with each element = value
            //console.log(key);
            //console.log(distribution[key]);
            //console.log(Array(distribution[key]).fill(key));
            repeatedSamples = repeatedSamples.concat(Array(distribution[key]).fill(key));
        }
    }

    var ent = entropy(repeatedSamples);

    //console.log('Entropy was '+ent);
    //console.log(distribution);
    //console.log(repeatedSamples)
    return ent;
}

function accumulate(d) {
    // does depth first traversal on tree 3 times, could be a lot more efficient
    if(d._children=d.children)
    {
    d.value = d.children.reduce(function(p, v) {
      return p + accumulate(v).value;
    }, 0);

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
          'classDistribution': d.classDistribution};
}

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

// currently eddEdges shows only 'interesting' part of the tree.
// can comment out the conditionals containing allLeavesNotInteresting invocation to 
// resume displaying the entire tree
var addEdges = function(node,g){
    //console.log(node);
    //console.log(allLeavesNotInteresting(node));
    if(allLeavesNotInteresting(node)) return g;
    if(node.type == 'feature')
    {
        _.each(node.vals,function(m){
            if(!allLeavesNotInteresting(m)) // i.e. atleast one leaf is interesting
            {
                g.push([m.alias,node.alias,'']);
                g = addEdges(m,g);
            }
        });
        return g;
    }

    if(node.type == 'feature_value')
    {
        g.push([node.child.alias,node.alias,'']);
        if(node.child.type != 'result')
        {
            g = addEdges(node.child,g);
        }
        return g;
    }
    return g;
}


var renderSamples = function(samples,$el,model,target,features){
    _.each(samples,function(s){
	var features_for_sample = _.map(features,function(x){return s[x]});
	$el.append("<tr><td>"+features_for_sample.join('</td><td>')+"</td><td><b>"+predict(model,s)+"</b></td><td>actual: "+s[target]+"</td></tr>");
    })
}

var renderTrainingData = function(_training,$el,target,features){
    _training.each(function(s){
	$el.append("<tr><td>"+_.map(features,function(x){return s[x]}).join('</td><td>')+"</td><td>"+s[target]+"</td></tr>");
    })
}

var calcError = function(samples,model,target){
    var total = 0;
    var correct = 0;
    _.each(samples,function(s){
	total++;
	var pred = predict(model,s);
	var actual = s[target];
	if(pred == actual){
	    correct++;
	}
    });
    return correct/total;
}
