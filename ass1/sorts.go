package main

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

func insertion_sort(arr []int) error {
	for j := range len(arr) {
		key := arr[j]
		i := j - 1
		for i >= 0 && arr[i] > key {
			arr[i+1] = arr[i]
			i--
		}
		arr[i+1] = key
	}
	return nil
}

func merge_sort(arr []int) error {
	actual_merge_sort(arr, 1, len(arr))
	return nil
}

func actual_merge_sort(arr []int, p int, r int) {
	if p < r {
		q := (p + r) / 2
		actual_merge_sort(arr, p, q)
		actual_merge_sort(arr, q+1, r)
		merge(arr, p, q, r)
	}
}

func merge(arr []int, p int, q int, r int) {
	n1 := q - p + 1
	n2 := r - q

	left := arr[p-1 : q]
	right := arr[q:r]

	i := 0
	j := 0
	for k := p - 1; k < r; k++ {
		if i < n1 && (j > n2-1 || left[i] <= right[j]) {
			arr[k] = left[i]
			i++
		} else {
			arr[k] = right[j]
			j++
		}
	}
}

func heap_sort(arr []int) error {
	n := len(arr)
	for i := (n / 2) - 1; i > -1; i-- {
		max_heapify(arr, n, i)
	}
	for i := n - 1; i > 0; i-- {
		arr[0], arr[i] = arr[i], arr[0]
		max_heapify(arr, i, 0)
	}
	return nil
}
func max_heapify(arr []int, n int, i int) {
	max := i
	left_node := 2*i + 1
	right_node := 2*i + 2

	if left_node < n && arr[left_node] > arr[max] {
		max = left_node
	}
	if right_node < n && arr[right_node] > arr[max] {
		max = right_node
	}

	if max != i {
		arr[i], arr[max] = arr[max], arr[i]
		max_heapify(arr, n, max)
	}
}

func quick_sort(arr []int) error {
	actual_quick_sort(arr, 0, len(arr)-1)
	return nil
}
func actual_quick_sort(arr []int, start int, pivot_point int) {
	if arr == nil {
		return
	}

	i := start
	j := i

	pivot := arr[pivot_point]

	for j < pivot_point {
		if arr[j] < pivot {
			arr[i], arr[j] = arr[j], arr[i]
			i++
		}
		j++
	}

	arr[i], arr[pivot_point] = arr[pivot_point], arr[i]

	if start < i-1 {
		actual_quick_sort(arr, start, i-1)
	}
	if i+1 < pivot_point {
		actual_quick_sort(arr, i+1, pivot_point)
	}
}
