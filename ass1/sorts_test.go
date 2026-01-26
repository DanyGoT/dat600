package main

import (
	"reflect"
	"sort"
	"testing"
)

var testCases = [][]int{
	{},
	{1},
	{1, 2, 3},
	{3, 2, 1},
	{3, 1, 2, 1},
	{0, -1, 5, -3, 2},
}

type sortFunc struct {
	name string
	fn   func([]int) error
}

var sortFunctions = []sortFunc{
	{"InsertionSort", func(arr []int) error { return insertion_sort(arr) }},
	{"MergeSort", func(arr []int) error { return merge_sort(arr) }},
	{"HeapSort", func(arr []int) error { return heap_sort(arr) }},
	{"QuickSort", func(arr []int) error { return quick_sort(arr) }},
}

func expected(arr []int) []int {
	a := append([]int(nil), arr...)
	sort.Ints(a)
	return a
}

func TestInsertionSort(t *testing.T) {
	test(t, sortFunctions[0])
}
func TestMergeSort(t *testing.T) {
	test(t, sortFunctions[1])
}
func TestHeapSort(t *testing.T) {
	test(t, sortFunctions[2])
}
func TestQuickSort(t *testing.T) {
	test(t, sortFunctions[3])
}

func test(t *testing.T, s sortFunc) {
	for _, tc := range testCases {
		c := append([]int(nil), tc...)
		err := s.fn(c)
		if err != nil {
			t.Errorf("%s not implemented", s.name)
			break
		}

		want := expected(c)
		if !reflect.DeepEqual(c, want) {
			t.Errorf("%s failed for input %v: got %v, want %v", s.name, tc, c, want)
		}
	}
}
