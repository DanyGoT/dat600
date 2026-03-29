package tasks

import (
	"fmt"
	"maps"
	"slices"
)

func Task3() {
	// Task 3A: Find champions using reachability matrix
	mat := getMatrixTask3()
	printMatrix(mat)
	mat = reachabilityMatrix(mat)
	fmt.Println()
	printMatrix(mat)
	fmt.Println()
	champs := champions(mat)
	fmt.Printf("Champions: ")
	for _, i := range champs {
		fmt.Printf("%s ", label(i))
	}
	fmt.Println()

	// Task 3B: Find SCCs using Kosaraju
	g := getMatrixTask3()
	nodes := makeNodeMap(g.RelationMap())
	dfs(nodes, nil)

	nodesT := makeNodeMap(g.Transposed().RelationMap())
	keys := slices.SortedFunc(maps.Keys(nodes), func(a, b string) int {
		return nodes[b].f - nodes[a].f
	})
	dfs(nodesT, keys)

	printSCCs(nodesT)
}

func champions(g graph) []int {
	champs := []int{}
	for i, row := range g {
		isChampion := true
		for j, val := range row {
			if i != j && val != 1 {
				isChampion = false
				break
			}
		}
		if isChampion {
			champs = append(champs, i)
		}
	}
	return champs
}

func reachabilityMatrix(g graph) graph {
	for {
		converged := true
		for i, row := range g {
			for j, val := range row {
				if val == 0 {
					continue
				}
				for k, val2 := range g[j] {
					if val2 != 0 && row[k] != 1 {
						row[k] = 1
						converged = false
					}
				}
			}
			g[i] = row
		}
		if converged {
			break
		}
	}
	return g
}

func label(i int) string {
	return string('A' + i)
}

func getMatrixTask3() graph {
	//   A  B  C  D  E  F  G
	return graph{
		{0, 1, 0, 1, 0, 0, 0}, // A
		{1, 0, 1, 0, 0, 0, 0}, // B
		{0, 0, 0, 0, 1, 1, 0}, // C
		{0, 1, 1, 0, 0, 0, 0}, // D
		{0, 0, 0, 0, 0, 0, 1}, // E
		{0, 0, 0, 0, 1, 0, 0}, // F
		{0, 0, 0, 0, 0, 1, 0}, // G
	}
}

func printMatrix(g graph) {
	for _, row := range g {
		fmt.Printf("%v\n", row)
	}
}
