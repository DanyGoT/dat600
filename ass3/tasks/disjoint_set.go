package tasks

// Go port of ass2/adt/disjoint_set.py

type DisjointSet struct {
	parent map[string]string
	rank   map[string]int
}

func newDisjointSet() *DisjointSet {
	return &DisjointSet{make(map[string]string), make(map[string]int)}
}

func (ds *DisjointSet) makeSet(x string) {
	if _, ok := ds.parent[x]; !ok {
		ds.parent[x] = x
		ds.rank[x] = 0
	}
}

func (ds *DisjointSet) findSet(x string) string {
	if ds.parent[x] != x {
		ds.parent[x] = ds.findSet(ds.parent[x])
	}
	return ds.parent[x]
}

func (ds *DisjointSet) union(x, y string) {
	rx, ry := ds.findSet(x), ds.findSet(y)
	if rx == ry {
		return
	}
	if ds.rank[rx] < ds.rank[ry] {
		ds.parent[rx] = ry
	} else if ds.rank[rx] > ds.rank[ry] {
		ds.parent[ry] = rx
	} else {
		ds.parent[ry] = rx
		ds.rank[rx]++
	}
}
