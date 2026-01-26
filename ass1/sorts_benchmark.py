import csv
import random
import time
from sorts import insertion_sort, merge_sort, heap_sort, quick_sort


def benchmark_sorts():
    sort_functions = [
        ("InsertionSort", insertion_sort),
        ("MergeSort", merge_sort),
        ("HeapSort", heap_sort),
        ("QuickSort", quick_sort),
    ]

    input_sizes = [100, 500, 1000, 2000, 5000, 10000]

    num_runs = 5

    with open("python_benchmark_results.csv", "w", newline="") as file:
        writer = csv.writer(file)

        writer.writerow(["Algorithm", "InputSize", "TimeMs"])

        print("Running Python benchmarks...")
        print("===================")

        # Benchmark each sorting function
        for name, sort_func in sort_functions:
            print(f"\nTesting {name}:")

            for size in input_sizes:
                total_time = 0.0

                # Run multiple times and average
                for _ in range(num_runs):
                    arr = [random.randint(0, 9999) for _ in range(size)]

                    start = time.perf_counter()
                    sort_func(arr)
                    elapsed = time.perf_counter() - start

                    total_time += elapsed

                # Calculate average time in milliseconds
                avg_time_ms = (total_time / num_runs) * 1000

                writer.writerow([name, size, f"{avg_time_ms:.4f}"])

                print(f"  Size {size}: {avg_time_ms:.4f} ms (avg of {num_runs} runs)")

        print("\n===================")
        print("Benchmark results saved to python_benchmark_results.csv")


if __name__ == "__main__":
    benchmark_sorts()
