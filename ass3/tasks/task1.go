package tasks

import (
	"fmt"
	"maps"
	"slices"
)

func Task1() {
	g := getRelationMatrix()
	nodes := makeNodeMap(g.RelationMap())
	dfs(nodes, nil)

	fmt.Println("=== Not DAG ===")
	printRelationList(g.RelationMap())

	nodesT := makeNodeMap(g.Transposed().RelationMap())
	keys := slices.SortedFunc(maps.Keys(nodes), func(a, b string) int {
		return nodes[b].f - nodes[a].f
	})
	dfs(nodesT, keys)

	for id, node := range nodesT {
		nodes[id].scc = node.scc
	}

	dag := g.ToDAG(nodes)
	fmt.Println("=== DAG ===")
	printRelationList(dag.RelationMap())

	fmt.Println()
	printDot("Original", g.RelationMap())
	fmt.Println()
	printDot("DAG", dag.RelationMap())
}

// Types and constants

type Node struct {
	id         string
	color      color
	neighbours []*Node
	d          int
	f          int
	scc        int
}
type graph [][]int
type color string

const (
	WHITE color = "White"
	GRAY  color = "Gray"
	BLACK color = "Black"
)

// Algorithms

func dfs(nodes map[string]*Node, keys []string) {
	if keys == nil {
		keys = slices.Sorted(maps.Keys(nodes))
	}
	time := 0
	sccID := 0
	for _, key := range keys {
		if nodes[key].color == WHITE {
			dfsVisit(nodes[key], &time, sccID)
			sccID++
		}
	}
}

func dfsVisit(node *Node, time *int, sccID int) {
	*time += 1
	node.color = GRAY
	node.d = *time
	node.scc = sccID
	for _, neighbour := range slices.Backward(node.neighbours) {
		if neighbour.color == WHITE {
			dfsVisit(neighbour, time, sccID)
		}
	}
	node.color = BLACK
	*time += 1
	node.f = *time
}

func (g graph) ToDAG(nodes map[string]*Node) graph {
	keys := slices.Sorted(maps.Keys(nodes))
	n := len(g)
	dag := make(graph, n)
	for i := range dag {
		dag[i] = make([]int, n)
	}

	for i, row := range g {
		for j, val := range row {
			if val != 1 {
				continue
			}
			u, v := nodes[keys[i]], nodes[keys[j]]
			if u.scc != v.scc || u.f > v.f {
				dag[i][j] = 1
			}
		}
	}
	return dag
}

// Utility

func printRelationList(rel map[string][]string) {
	for _, k := range slices.Sorted(maps.Keys(rel)) {
		fmt.Printf("%s → %v\n", k, rel[k])
	}
}

// Used to generate graph using graphwiz
func printDot(name string, rel map[string][]string) {
	fmt.Printf("digraph %s {\n", name)
	fmt.Println("  rankdir=LR;")
	for _, u := range slices.Sorted(maps.Keys(rel)) {
		for _, v := range rel[u] {
			fmt.Printf("  %s -> %s;\n", u, v)
		}
	}
	fmt.Println("}")
}

func printMap(nodes map[string]*Node) {
	for _, id := range slices.Sorted(maps.Keys(nodes)) {
		node := nodes[id]
		fmt.Printf("Node %s (color: %s, time: %d, %d) -> Neighbors: ", id, node.color, node.d, node.f)
		for _, n := range node.neighbours {
			fmt.Printf("%s ", n.id)
		}
		fmt.Println()
	}
}
func printSCCs(nodes map[string]*Node) {
	sccs := make(map[int][]string)
	for id, node := range nodes {
		sccs[node.scc] = append(sccs[node.scc], id)
	}
	for _, id := range slices.Sorted(maps.Keys(sccs)) {
		slices.Sort(sccs[id])
		fmt.Printf("SCC %d: %v\n", id, sccs[id])
	}
}

// Matrix and list stuff

func getRelationMatrix() graph {
	// I -> C and C -> A added
	return [][]int{
		//  B  C  D  E  F  G  H  I  J
		{0, 1, 0, 0, 0, 0, 0, 0, 0, 0}, // A
		{0, 0, 1, 1, 0, 0, 0, 0, 0, 0}, // B
		{1, 0, 0, 0, 1, 1, 0, 0, 0, 0}, // C
		{0, 0, 0, 0, 1, 1, 0, 0, 0, 0}, // D
		{0, 0, 0, 0, 0, 1, 1, 0, 0, 1}, // E
		{0, 1, 0, 0, 0, 0, 1, 1, 0, 1}, // F
		{0, 0, 0, 0, 0, 0, 0, 0, 0, 0}, // G
		{0, 0, 0, 0, 0, 0, 0, 0, 1, 0}, // H
		{0, 0, 1, 0, 0, 0, 0, 0, 0, 0}, // I
		{0, 0, 0, 0, 0, 0, 0, 0, 1, 0}, // J
	}
}

func (g graph) RelationMap() map[string][]string {
	labels := []string{"A", "B", "C", "D", "E", "F", "G", "H", "I", "J"}
	rel := make(map[string][]string)
	for i, row := range g {
		rel[labels[i]] = []string{}
		for j, val := range row {
			if val == 1 {
				rel[labels[i]] = append(rel[labels[i]], labels[j])
			}
		}
	}
	return rel
}

func (g graph) Transposed() graph {
	n := len(g)
	t := make(graph, n)
	for i := range t {
		t[i] = make([]int, n)
	}
	for i, row := range g {
		for j, val := range row {
			t[j][i] = val
		}
	}
	return t
}

func makeNodeMap(relList map[string][]string) map[string]*Node {
	nodes := make(map[string]*Node)
	for id := range relList {
		nodes[id] = &Node{id: id, color: WHITE}
	}
	for id, neighbours := range relList {
		for _, neighbour := range neighbours {
			nodes[id].neighbours = append(nodes[id].neighbours, nodes[neighbour])
		}
	}
	return nodes
}
