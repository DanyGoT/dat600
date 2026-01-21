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
	fn   func([]int) ([]int, error)
}

var sortFunctions = []sortFunc{
	{"InsertionSort", func(arr []int) ([]int, error) { return insertion_sort(arr) }},
	{"MergeSort", func(arr []int) ([]int, error) { return merge_sort(arr) }},
	{"HeapSort", func(arr []int) ([]int, error) { return heap_sort(arr) }},
	{"QuickSort", func(arr []int) ([]int, error) { return quick_sort(arr) }},
}

func expected(arr []int) []int {
	a := append([]int(nil), arr...)
	sort.Ints(a)
	return a
}

func TestSortCorrect(t *testing.T) {
	for _, s := range sortFunctions {
		for _, c := range testCases {
			got, err := s.fn(c)
			if err != nil {
				t.Errorf("%s not implemented", s.name)
				break
			}

			want := expected(c)
			if !reflect.DeepEqual(got, want) {
				t.Errorf("%s failed for input %v: got %v, want %v", s.name, c, got, want)
			}
		}
	}
}
