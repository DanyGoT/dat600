package tasks

import (
	"fmt"
)

func Task1() {
	Adj := [][]int{
		{0, 1, 0, 0, 0, 0}, // 1
		{0, 1, 1, 1, 0, 0}, // 2
		{1, 1, 0, 0, 1, 0}, // 3
		{0, 0, 0, 0, 1, 1}, // 4
		{0, 0, 1, 1, 0, 0}, // 5
		{0, 0, 0, 1, 0, 0}, // 6
	}
	fmt.Printf("Matrice: \n%v", Adj)
}
