package tasks

import (
	"fmt"
	"slices"
)

type edge struct {
	u, v string
	cost int
}

func Task2() {
	graph := getGraph()
	printDotUndirected("NonMST", graph)
	mst := kruskal(graph)
	printDotUndirected("MST", mst)

	maxDegree := map[string]int{
		"D": 3,
	}
	mstConstrained := kruskalConstrained(graph, maxDegree)
	improved := localSearch(mstConstrained, graph, maxDegree)
	printDotUndirected("ConstrainedMST", improved)

	original := 0
	for _, e := range graph {
		original += e.cost
	}
	total := 0
	for _, e := range mst {
		total += e.cost
	}
	constrained := 0
	for _, e := range improved {
		constrained += e.cost
	}

	_, optCost := bruteForce(graph, maxDegree)
	fmt.Printf("Original cost: %d, Minimum cost: %d, Constrained cost: %d, Optimal constrained: %d\n", original, total, constrained, optCost)

	testCounterExample()
}

// Algorithms

func kruskal(g []edge) []edge {
	slices.SortFunc(g, func(a, b edge) int {
		return a.cost - b.cost
	})

	set := newDisjointSet()
	for _, edge := range g {
		set.makeSet(edge.u)
		set.makeSet(edge.v)
	}

	A := []edge{}
	for _, edge := range g {
		if set.findSet(edge.u) != set.findSet(edge.v) {
			A = append(A, edge)
			set.union(edge.u, edge.v)
		}
	}
	return A
}

func kruskalConstrained(g []edge, maxDegree map[string]int) []edge {
	slices.SortFunc(g, func(a, b edge) int {
		return a.cost - b.cost
	})

	degree := make(map[string]int)
	set := newDisjointSet()
	for _, edge := range g {
		set.makeSet(edge.u)
		set.makeSet(edge.v)
	}

	A := []edge{}
	for _, edge := range g {
		if max, ok := maxDegree[edge.u]; ok && degree[edge.u] >= max {
			continue
		}
		if max, ok := maxDegree[edge.v]; ok && degree[edge.v] >= max {
			continue
		}
		if set.findSet(edge.u) != set.findSet(edge.v) {
			A = append(A, edge)
			set.union(edge.u, edge.v)
			degree[edge.u]++
			degree[edge.v]++
		}
	}
	return A
}

func localSearch(mst, all []edge, maxDeg map[string]int) []edge {
	for _, add := range all {
		for i, rem := range mst {
			if add.cost < rem.cost {
				mst[i] = add
				if isValid(mst, maxDeg) {
					return localSearch(mst, all, maxDeg)
				}
				mst[i] = rem
			}
		}
	}
	return mst
}

func isValid(edges []edge, maxDeg map[string]int) bool {
	deg := make(map[string]int)
	set := newDisjointSet()
	for _, e := range edges {
		set.makeSet(e.u)
		set.makeSet(e.v)
		deg[e.u]++
		deg[e.v]++
	}
	for v, max := range maxDeg {
		if deg[v] > max {
			return false
		}
	}
	for _, e := range edges {
		if set.findSet(e.u) == set.findSet(e.v) {
			return false
		}
		set.union(e.u, e.v)
	}
	return true
}

func bruteForce(g []edge, maxDeg map[string]int) ([]edge, int) {
	vertices := make(map[string]bool)
	for _, e := range g {
		vertices[e.u] = true
		vertices[e.v] = true
	}
	n := len(vertices) - 1
	best := []edge{}
	bestCost := 999999

	var combine func(start int, current []edge)
	combine = func(start int, current []edge) {
		if len(current) == n {
			if isValid(current, maxDeg) {
				cost := 0
				for _, e := range current {
					cost += e.cost
				}
				if cost < bestCost {
					bestCost = cost
					best = make([]edge, n)
					copy(best, current)
				}
			}
			return
		}
		for i := start; i < len(g); i++ {
			combine(i+1, append(current, g[i]))
		}
	}
	combine(0, []edge{})
	return best, bestCost
}

// Utility

func lowest(g []edge) edge {
	return slices.MinFunc(g, func(a, b edge) int {
		return a.cost - b.cost
	})
}

func removeEdge(g []edge, e edge) []edge {
	for i, edge := range g {
		if e == edge {
			return slices.Delete(g, i, i+1)
		}
	}
	return g
}
func newEdge(u, v string, c int) edge {
	if u > v {
		u, v = v, u
	}
	return edge{u, v, c}
}
func getGraph() []edge {
	return []edge{
		newEdge("A", "B", 5),
		newEdge("A", "D", 1),

		newEdge("B", "D", 4),
		newEdge("B", "H", 8),

		newEdge("C", "D", 2),
		newEdge("C", "G", 6),

		newEdge("D", "E", 2),
		newEdge("D", "F", 4),

		newEdge("E", "H", 8),

		newEdge("F", "G", 9),
		newEdge("F", "H", 7),
	}
}

func getCounterExample() []edge {
	return []edge{
		newEdge("A", "D", 1),
		newEdge("D", "C", 1),
		newEdge("B", "D", 1),
		newEdge("C", "E", 1),
		newEdge("A", "C", 5),
		newEdge("B", "E", 10),
	}
}

func testCounterExample() {
	graph := getCounterExample()
	maxDeg := map[string]int{"D": 2}

	greedy := kruskalConstrained(graph, maxDeg)
	greedyCost := 0
	for _, e := range greedy {
		greedyCost += e.cost
	}

	optimal, optCost := bruteForce(graph, maxDeg)

	printDotUndirected("CounterOriginal", graph)
	printDotUndirected("CounterGreedy", greedy)
	printDotUndirected("CounterOptimal", optimal)

	fmt.Printf("Counter-example: Greedy=%d, Optimal=%d\n", greedyCost, optCost)
}

func printDotUndirected(name string, edges []edge) {
	fmt.Printf("graph %s {\n", name)
	fmt.Println("  rankdir=LR;")
	for _, e := range edges {
		fmt.Printf("  %s -- %s [label=%d];\n", e.u, e.v, e.cost)
	}
	fmt.Println("}")
}
