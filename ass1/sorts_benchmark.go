package main

import (
	"encoding/csv"
	"fmt"
	"math/rand"
	"os"
	"strconv"
	"time"
)

func main() {
	inputSizes := []int{100, 500, 1000, 2000, 5000, 10000}

	numRuns := 5

	file, err := os.Create("benchmark_results.csv")
	if err != nil {
		fmt.Printf("Error creating CSV file: %v\n", err)
		return
	}
	defer file.Close()

	writer := csv.NewWriter(file)
	defer writer.Flush()

	header := []string{"Algorithm", "InputSize", "TimeMs"}
	if err := writer.Write(header); err != nil {
		fmt.Printf("Error writing header: %v\n", err)
		return
	}

	fmt.Println("Running benchmarks...")
	fmt.Println("===================")

	// Benchmark each sorting function
	for _, sortFunc := range sortFunctions {
		fmt.Printf("\nTesting %s:\n", sortFunc.name)

		for _, size := range inputSizes {
			var totalTime time.Duration

			// Run multiple times and average
			for range numRuns {
				arr := generateRandomArray(size)

				start := time.Now()
				err := sortFunc.fn(arr)
				elapsed := time.Since(start)

				if err != nil {
					fmt.Printf("Error in %s with size %d: %v\n", sortFunc.name, size, err)
					continue
				}

				totalTime += elapsed
			}

			// Calculate average time in milliseconds
			avgTime := totalTime / time.Duration(numRuns)
			avgTimeMs := float64(avgTime.Microseconds()) / 1000.0

			record := []string{
				sortFunc.name,
				strconv.Itoa(size),
				fmt.Sprintf("%.4f", avgTimeMs),
			}

			if err := writer.Write(record); err != nil {
				fmt.Printf("Error writing record: %v\n", err)
				continue
			}

			fmt.Printf("  Size %d: %.4f ms (avg of %d runs)\n", size, avgTimeMs, numRuns)
		}
	}

	fmt.Println("\n===================")
	fmt.Println("Benchmark results saved to benchmark_results.csv")
}

func generateRandomArray(size int) []int {
	arr := make([]int, size)
	for i := range size {
		arr[i] = rand.Intn(10000)
	}
	return arr
}
