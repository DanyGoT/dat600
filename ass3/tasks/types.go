package tasks

type edge struct {
	u, v string
	cost int
}

type graph [][]int

type Node struct {
	id         string
	color      color
	neighbours []*Node
	d          int
	f          int
	scc        int
}

type color string

const (
	WHITE color = "White"
	GRAY  color = "Gray"
	BLACK color = "Black"
)
