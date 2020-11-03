var distances
var precomputeDistances
var lists = []

function visualDistance(list1, list2)
{	
	if (list1.length!=list2.length)
	{
		//console.log("List1: "+list1);
		//console.log("List2: "+list2);
		return -1;
	}

	var distance = 0;
	for (var i=0; i<list1.length; i++)
		for (var j=0; j<list2.length; j++)
			distance += Math.exp(-Math.abs(i-j)) * Math.abs(list1[i]-list2[j]);
	
	return distance;
}

function boundedDistance(list1, list2, bound)
{
	// this version only compares each element of list1 with a sliding window 
	// 'bound' of elements in list2, so hopefully a little faster
	if(list1.length!=list2.length) return -1;
	if(bound>=list1.length) return visualDistance(list1,list2);

	var distance = 0;
	for (var i=0; i<list1.length; i++)
		for (var j=Math.max(0,i-bound); j<Math.min(list2.length,i+bound); j++)
			distance += Math.exp(-Math.abs(i-j)) * Math.abs(list1[i]-list2[j]);
	
	return distance;
}

function boundedDistance2(list1, list2, bound)
{
	// this version only compares each element of list1 with a sliding window 
	// 'bound' of elements in list2, so hopefully a little faster
	// also uses 1/(position diff+1) as decay function instead of e^-(position diff)
	// -- gives higher weighting to neighbours. Also, what about 2^-(position diff), could be efficient.

	var distance = 0;
	for (var i=0; i<list1.length; i++)
		for (var j=Math.max(0,i-bound); j<Math.min(list2.length,i+bound); j++)
			distance += (1/(Math.abs(i-j)+1) * Math.abs(list1[i]-list2[j]));
	
	return distance;
}

function absolutePairwiseDistance(list1, list2)
{
	// this version only compares each element of list1 with its corresponding
	// element in list2 so as fast as it gets with this strategy
	// if(list1.length!=list2.length) return -1;
	// assumes they are of same length or list1 is longer

	var distance = 0;
	for (var i=0; i<list1.length; i++)
	{
		//var diff = list1[i]-list2[i];
		distance += Math.abs(list1[i]-list2[i]);
		//distance += (diff + (diff >> 31))^(diff>>31);
	}
	
	return distance;
}

function highPassBoundedDistance(list1, list2, bound)
{
	// like a high pass filter, only "let through" (penalise) big differences. Small differences are rounded down to 1. Other differences are reduced by threshold.
	var threshold = 3; // arbitrarily set from Martin's data
	var distance = 0;
	for (var i=0; i<list1.length; i++)
		for (var j=Math.max(0,i-bound); j<Math.min(list2.length,i+bound); j++)
			distance += (1/(Math.abs(i-j)+1) * Math.max(1, Math.abs(list1[i]-list2[j])-threshold));
	
	return distance;
}

function allDistances(lists)
{
	let distanceMatrix = [];

	for(let i=0; i<lists.length; i++) {
		distanceMatrix[i] = []
		for(let j=0; j<lists.length; j++) {
			distanceMatrix[i][j] = 0
		}
	}

	for(let i=0; i<lists.length; i++) {
		postMessage({"type":"distanceProgress","value":i});

		for(let j=i+1; j<lists.length; j++) {
			const d = boundedDistance2(lists[i], lists[j],8)
			distanceMatrix[i][j] = d
			distanceMatrix[j][i] = d
		}
	}
	return distanceMatrix
}

// can make a really inefficient double-ended queue using javascript Array
// functions: push = add to tail, unshift = add to head, 
// pop = pop from tail, shift = pop from head

function recompose(lists)
{	
	console.log("Recomposing...")
	var BIG_NUMBER = Number.MAX_VALUE;
	var originalSize = lists.length;
	var totalDistance = 0;
	
	//var recomposed = [];
	var labels = [];
	
	unallottedLabels = [];
	for(let i=0; i<lists.length;i++) unallottedLabels[i] = i

	postMessage({"type":"recomposeProgress","value":0});
	// gets key with minimum value
	let seedL, seedR
	let currentMin = BIG_NUMBER;
	for(let i=0; i<unallottedLabels.length; i++) {
		for(let j=i+1; j<unallottedLabels.length; j++) {
			const d = distanceLookup(i,j)
			if(d<currentMin) {
				seedL = i
				seedR = j
				currentMin = d
			}
		}
	}

	totalDistance += currentMin;

	currentLeft = seedL;
	currentRight = seedR;
	
	//recomposed.push(lists[seedR]);
	//recomposed.unshift(lists[seedL]);
	
	labels.push(seedR);
	labels.unshift(seedL);
	
	unallottedLabels.splice(unallottedLabels.indexOf(seedL),1);
	unallottedLabels.splice(unallottedLabels.indexOf(seedR),1);
	
	//console.table(lists);
	while(unallottedLabels.length>0)
	{
		//console.log("Size of list: "+lists.length)
		var fractionRecomposeProgress = 1-(unallottedLabels.length/originalSize);
		postMessage({"type":"recomposeProgress","value":fractionRecomposeProgress}); // will use the value field when this becomes complicated

		var minKeyL = "NIL";
		var minKeyR = "NIL";
		
		var minDistanceL = BIG_NUMBER; 
		var minDistanceR = BIG_NUMBER;
		
		for(let i=0; i<unallottedLabels.length; i++) {
			const l = unallottedLabels[i]

			if(l!==currentLeft) {
				const dL = distanceLookup(currentLeft,l)
					if (dL < minDistanceL) {
					minKeyL = l
					minDistanceL = dL
				}
			}

			if(l!==currentRight) {
				const dR = distanceLookup(currentRight,l)
				if (dR < minDistanceR) {
					minKeyR = l
					minDistanceR = dR
				}
			}
		}

		if(minDistanceL < minDistanceR)
		{
			labels.unshift(minKeyL);
			currentLeft = minKeyL;
			unallottedLabels.splice(unallottedLabels.indexOf(minKeyL), 1);
			totalDistance += minDistanceL;
		}
		else
		{
			labels.push(minKeyR);
			currentRight = minKeyR;
			unallottedLabels.splice(unallottedLabels.indexOf(minKeyR),1);
			totalDistance += minDistanceR;
		}
		//console.log(minKeyL+ " "+minKeyR)
	}
	console.log("Finished gathering. Total distance was: "+totalDistance);
	postMessage({"type":"labels","value":labels});
	postMessage({"type":"finished"});
}

function recomposeImperfectSeed(lists)
{	
	console.log("Recomposing...")
	var BIG_NUMBER = Number.MAX_VALUE;
	var originalSize = lists.length;
	var totalDistance = 0;
	
	//var recomposed = [];
	var labels = [];
	
	unallottedLabels = [];
	for(let i=0; i<lists.length;i++) unallottedLabels[i] = i

	postMessage({"type":"recomposeProgress","value":0});
	// gets key with minimum value
	let seedL = 0
	let seedR
	let currentMin = BIG_NUMBER;
	for(let i=0; i<unallottedLabels.length; i++) {
			const l = unallottedLabels[i]
			if(l!==seedL) {
				const dL = distanceLookup(seedL,l)
					if (dL < currentMin) {
					seedR = l
					currentMin = dL
				}
			}
		}

	totalDistance += currentMin;

	currentLeft = seedL;
	currentRight = seedR;
	
	//recomposed.push(lists[seedR]);
	//recomposed.unshift(lists[seedL]);
	
	labels.push(seedR);
	labels.unshift(seedL);
	
	unallottedLabels.splice(unallottedLabels.indexOf(seedL),1);
	unallottedLabels.splice(unallottedLabels.indexOf(seedR),1);
	
	//console.table(lists);
	while(unallottedLabels.length>0)
	{
		//console.log("Size of list: "+lists.length)
		var fractionRecomposeProgress = 1-(unallottedLabels.length/originalSize);
		postMessage({"type":"recomposeProgress","value":fractionRecomposeProgress}); // will use the value field when this becomes complicated

		var minKeyL = "NIL";
		var minKeyR = "NIL";
		
		var minDistanceL = BIG_NUMBER; 
		var minDistanceR = BIG_NUMBER;
		
		for(let i=0; i<unallottedLabels.length; i++) {
			const l = unallottedLabels[i]

			if(l!==currentLeft) {
				const dL = distanceLookup(currentLeft,l)
					if (dL < minDistanceL) {
					minKeyL = l
					minDistanceL = dL
				}
			}

			if(l!==currentRight) {
				const dR = distanceLookup(currentRight,l)
				if (dR < minDistanceR) {
					minKeyR = l
					minDistanceR = dR
				}
			}
		}

		if(minDistanceL < minDistanceR)
		{
			labels.unshift(minKeyL);
			currentLeft = minKeyL;
			unallottedLabels.splice(unallottedLabels.indexOf(minKeyL), 1);
			totalDistance += minDistanceL;
		}
		else
		{
			labels.push(minKeyR);
			currentRight = minKeyR;
			unallottedLabels.splice(unallottedLabels.indexOf(minKeyR),1);
			totalDistance += minDistanceR;
		}
		//console.log(minKeyL+ " "+minKeyR)
	}
	console.log("Finished gathering. Total distance was: "+totalDistance);
	postMessage({"type":"labels","value":labels});
	postMessage({"type":"finished"});
}


Object.size = function(obj) {
    var size = 0, key;
    for (key in obj) {
        if (obj.hasOwnProperty(key)) size++;
    }
    return size;
};

/* ENTRYPOINT EVENT LISTENER THAT GETS MESSAGES FROM MAIN THREAD */
self.addEventListener('message',function(e) {
	var listsAsOrdered = e.data.lists;
	var strategy = e.data.strategy;
	var labelOrder = e.data.labels;
	precomputeDistances = e.data.precomputeDistances

	/* there's a bug where gathering the same dataset more than once returns complete garbage orderings */
	/* I have a feeling the answer is somewhere here but I cba to fix it for now */
	console.log("Sanity check same number of labels as lists: "+(labelOrder.length===listsAsOrdered.length));
	for(var i=0;i<labelOrder.length;i++) 
		lists[labelOrder[i]] = listsAsOrdered[i]; 

	// labelOrder's Nth element points to which of the original data series as loaded currently occupies position N
	// thus, the for loop above reconstructs the original data series as loaded
	// this allows us to reuse the distance matrix, because the keys always stay the same
	// a bit convoluted but that's how it turned out, sorry
	
	if (precomputeDistances) {
		console.log("Computing distances...");
		distances = allDistances(lists);
	}
	
	if(strategy==="genetic")
		recomposeGeneticTSP(lists);
	else if(strategy==="greedyImperfectSeed")
		recomposeImperfectSeed(lists)
	else if(strategy==="greedy")
		recompose(lists);
	else
		console.log("Error: invalid strategy type: "+strategy);
},false);


/* BEGIN GREEDY MULTI-'SEED' TSP */
function recomposeTSPGreedyN(lists)
{
	// TODO when bothered
	// Algorithm given by http://lcm.csa.iisc.ernet.in/dsa/node186.html

	/*
	Based on Kruskal's algorithm. It only gives a suboptimal solution in general.
	Works for complete graphs. May not work for a graph that is not complete.
	
	As in Kruskal's algorithm, first sort the edges in the increasing order of weights.
	
	Starting with the least cost edge, look at the edges one by one 
	and select an edge only if the edge, together with already selected edges,
	1. does not cause a vertex to have degree three or more
	2. does not form a cycle, unless the number of selected edges equals the number of vertices in the graph.
	*/	
}

/* BEGIN GENETIC ALGORITHM  STUFF */
// adapted from https://github.com/parano/GeneticAlgorithm-TSP

var running;
var doPreciseMutate;

var POPULATION_SIZE;
var ELITE_RATE;
var CROSSOVER_PROBABILITY;
var MUTATION_PROBABILITY;
var OX_CROSSOVER_RATE;
var UNCHANGED_GENS;

var mutationTimes;
var bestValue, best;
var currentGeneration;
var currentBest;
var population;
var values;
var fitnessValues;
var roulette;

function recomposeGeneticTSP(lists)
{
	// initialise parameters for the genetic algorithm
	POPULATION_SIZE = 30; // how many candidate solutions we are keeping
	var NUM_GENERATIONS = 100;
	running = false;
	ELITE_RATE = 0.3;
	CROSSOVER_PROBABILITY = 0.9;
	MUTATION_PROBABILITY  = 0.01;
	//OX_CROSSOVER_RATE = 0.05;
	UNCHANGED_GENS = 0;
	mutationTimes = 0;
	doPreciseMutate = true;

	bestValue = undefined; // cost of the best individual ordering/cycle/tour
	best = []; // best individual ordering/cycle/tour
	currentGeneration = 0;
	currentBest; // object pointing to which of the current population is our current best
	population = []; //new Array(POPULATION_SIZE);
	values = new Array(POPULATION_SIZE);
	fitnessValues = new Array(POPULATION_SIZE);
	roulette = new Array(POPULATION_SIZE);

	for(var i=0; i<POPULATION_SIZE; i++)
    	population.push(randomIndividual(lists.length)); // assumes keys are integers from 0 to n

    setBestValue();

	for(var i=0; i<NUM_GENERATIONS; i++)
	{
		var fractionRecomposeProgress = (i+1)/NUM_GENERATIONS;
		postMessage({"type":"recomposeProgress","value":fractionRecomposeProgress});
		nextGeneration();
		// console.log('Finished gen '+(i+1));
		if(i%10===0) console.log('Cost at gen '+i+': '+bestValue);
	}

	//console.log("bestValue: "+bestValue);
	//console.log("currentBest: "+currentBest);
	//console.log("best: "+best);

	// bestValue should give you the same result as evaluate(best)

	//var recomposed = [];
	var labels = [];

	console.log("Sanity check to see if we've retained all series: "+(best.length===lists.length));
	for(var i=0; i<best.length; i++) 
	{
		//recomposed.push(lists[best[i]]);
		labels.push(best[i]);
	}

	console.log("Finished gathering. Total distance was: "+bestValue+", acyclic: "+(bestValue-distanceLookup(best[0],best[best.length-1])));
	//postMessage({"type":"result","value":[recomposed,labels]});
	postMessage({"type":"labels","value":labels});
	postMessage({"type":"finished"});
}

function distanceLookup(key1, key2) 
{
	if (precomputeDistances)
		return distances[key1][key2]
	else
		return absolutePairwiseDistance(lists[key1],lists[key2])
}

function setBestValue() {
  for(var i=0; i<population.length; i++) {
    values[i] = evaluate(population[i]);
    //values[i] = evaluateWindowed(population[i],2);
  }
  currentBest = getCurrentBest();
  if(bestValue === undefined || bestValue > currentBest.bestValue) {
    best = population[currentBest.bestPosition].clone();
    bestValue = currentBest.bestValue;
    UNCHANGED_GENS = 0;
  } else {
    UNCHANGED_GENS += 1;
  }
}

function getCurrentBest() {
  var bestP = 0,
  currentBestValue = values[0];

  for(var i=1; i<population.length; i++) {
    if(values[i] < currentBestValue) {
      currentBestValue = values[i];
      bestP = i;
    }
  }

  return {
    bestPosition: bestP, 
    bestValue: currentBestValue
  }
}

function evaluate(individual) {
  var sum = distanceLookup(individual[0], individual[individual.length-1]); // start by adding tail -> head distance
  //var sum = 0; // find paths not cycles, omg

  for(var i=1; i<individual.length; i++) {
    sum += distanceLookup(individual[i], individual[i-1]);
  }

  return sum;
}

function evaluateWindowed(individual,window)
{
	var sum = 0;
	for(var i=0; i<individual.length; i++) {
		for(var j=Math.max(0,i-window); j<Math.min(individual.length,i+window); j++) {
			if(j===i) continue;
			sum += distanceLookup(individual[i], individual[j])*(1/Math.abs(i-j));
		}
  	}
  	return sum;
}

// returns a random path through the graph
// e.g. [0,1,5,3,2,4] represents the cycle 0 -> 1 -> 5 -> 3 -> 2 -> 4 -> 0
function randomIndividual(n) 
{
  var a = [];
  for(var i=0; i<n; i++)
    a.push(i);

  return a.shuffle();
}

function nextGeneration() {
  currentGeneration++;
  selection();
  crossover();
  mutation();

  setBestValue();
}

// selection
function selection() {
  var parents = new Array();
  var initnum = 4;
  parents.push(population[currentBest.bestPosition]);
  parents.push(doMutate(best.clone()));
  parents.push(pushMutate(best.clone()));
  parents.push(best.clone());

  setRoulette();
  for(var i=initnum; i<POPULATION_SIZE; i++) {
    parents.push(population[wheelOut(Math.random())]);
  }
  population = parents;
}

// appears to pick an interval from n to m, within the sequence, and reverse the first half of that interval (subsequence)
function doMutate(seq) {
  mutationTimes++;
  // m and n refers to the actual index in the array
  // m range from 0 to length-2, n range from 2...length-m
  do {
    m = randomNumber(seq.length - 2);
    n = randomNumber(seq.length);
  } while (m>=n)

    for(var i=0, j=(n-m+1)>>1; i<j; i++) {
      seq.swap(m+i, n-i);
    }
    return seq;
}

// picks 2 points, m (somewhere in the first half of the sequence) and n, such that m<n
// then returns the concatenation of subsequences from m to n, then 0 to m, then n to the end
function pushMutate(seq) {
  mutationTimes++;
  var m,n;
  do {
    m = randomNumber(seq.length>>1);
    n = randomNumber(seq.length);
  } while (m>=n)

  var s1 = seq.slice(0,m);
  var s2 = seq.slice(m,n)
  var s3 = seq.slice(n,seq.length);
  return s2.concat(s1).concat(s3).clone();
}

function fitnessFromDistance(d)
{
	return 1.0/d;
}

function setRoulette() {
  //calculate all the fitness
  for(var i=0; i<values.length; i++) { fitnessValues[i] = fitnessFromDistance(values[i]); } 
  // fitness of a sequence is inversely proportional to total distance

  //set the roulette
  var sum = 0;
  for(var i=0; i<fitnessValues.length; i++) { sum += fitnessValues[i]; }
  for(var i=0; i<roulette.length; i++) { roulette[i] = fitnessValues[i]/sum; }
  for(var i=1; i<roulette.length; i++) { roulette[i] += roulette[i-1]; }
}

function wheelOut(rand) {
  var i;
  for(i=0; i<roulette.length; i++) {
    if( rand <= roulette[i] ) {
      return i;
    }
  }
}

//crossover
function crossover() {
  var queue = new Array();
  for(var i=0; i<POPULATION_SIZE; i++) {
    if(Math.random() < CROSSOVER_PROBABILITY ) {
      queue.push(i);
    }
  } 
  queue.shuffle();
  for(var i=0, j=queue.length-1; i<j; i+=2) {
    doCrossover(queue[i], queue[i+1]);
    //oxCrossover(queue[i], queue[i+1]);
  }
}

function doCrossover(x, y) {
  child1 = getChild('next', x, y);
  child2 = getChild('previous', x, y);
  population[x] = child1;
  population[y] = child2;
}

function getChild(fun, x, y) {
  solution = new Array();
  var px = population[x].clone();
  var py = population[y].clone();
  var dx,dy;
  var c = px[randomNumber(px.length)];
  solution.push(c);
  while(px.length > 1) {
    dx = px[fun](px.indexOf(c));
    dy = py[fun](py.indexOf(c));
    px.deleteByValue(c);
    py.deleteByValue(c);
    c = distanceLookup(c,dx) < distanceLookup(c,dy) ? dx : dy;
    solution.push(c);
  }
  return solution;
}

// mutation
function mutation() {
  for(var i=0; i<POPULATION_SIZE; i++) {
    if(Math.random() < MUTATION_PROBABILITY) {
      if(Math.random() > 0.5) {
        population[i] = pushMutate(population[i]);
      } else {
        population[i] = doMutate(population[i]);
      }
      i--;
    }
  }
}

function pushMutate(seq) {
  mutationTimes++;
  var m,n;
  do {
    m = randomNumber(seq.length>>1);
    n = randomNumber(seq.length);
  } while (m>=n)

  var s1 = seq.slice(0,m);
  var s2 = seq.slice(m,n)
  var s3 = seq.slice(n,seq.length);
  return s2.concat(s1).concat(s3).clone();
}

// some utilities
Array.prototype.clone = function() { return this.slice(0); }


Array.prototype.swap = function (x, y) {
  if(x>this.length || y>this.length || x === y) {return}
  var tem = this[x];
  this[x] = this[y];
  this[y] = tem;
}

Array.prototype.shuffle = function() {
  for(var j, x, i = this.length-1; i; j = randomNumber(i), x = this[--i], this[i] = this[j], this[j] = x);
  return this;
};

Array.prototype.next = function (index) {
  if(index === this.length-1) {
    return this[0];
  } else {
    return this[index+1];
  }
}

Array.prototype.previous = function (index) {
  if(index === 0) {
    return this[this.length-1];
  } else {
    return this[index-1];
  }
}

Array.prototype.deleteByValue = function (value) {
  var pos = this.indexOf(value);
  this.splice(pos, 1);
}

function randomNumber(boundary) {
  return parseInt(Math.random() * boundary);
  //return Math.floor(Math.random() * boundary);
}

/* END GENETIC ALGORITHM  STUFF */