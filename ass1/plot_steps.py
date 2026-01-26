import random
from typing import List
import matplotlib.pyplot as plt
import numpy as np
from sorts_with_steps import insertion_sort, merge_sort, heap_sort, quick_sort


def sorted_array(input_size):
    return list(range(input_size))


def random_array(input_size):
    arr = []
    for _ in range(input_size):
        arr.append(random.randint(1, 1000))
    return arr


def run_sort(sort_fn, input_size, count) -> List[int]:
    steps = []
    for _ in range(count):
        match sort_fn.__name__:
            case "insertion_sort":
                arr = list(range(input_size, 0, -1))
            case "quick_sort":
                arr = list(range(input_size))
            case _:
                arr = random_array(input_size)

        _, s = sort_fn(arr)
        steps.append(s)
    return steps


def plot_sorting_algorithms():
    # Input sizes to test
    sizes = range(1, 100)

    runs_per_size = 5

    # Store results for each algorithm
    algorithms = [
        ("Insertion Sort", insertion_sort),
        ("Merge Sort", merge_sort),
        ("Heap Sort", heap_sort),
        ("Quick Sort", quick_sort),
    ]

    # Create figure with subplots
    _, axes = plt.subplots(2, 2, figsize=(12, 10))
    axes = axes.flatten()

    # Plot each algorithm
    for idx, (name, sort_fn) in enumerate(algorithms):
        max_steps = []
        for size in sizes:
            steps = run_sort(sort_fn, size, runs_per_size)
            max_steps.append(max(steps))

        axes[idx].plot(sizes, max_steps, marker="o", label="Measured", linewidth=2)

        # Add theoretical curves for comparison
        if name in ["Insertion Sort", "Quick Sort"]:
            # Θ(n²) complexity
            c = max_steps[-1] / (sizes[-1] ** 2)
            theoretical = [c * n**2 for n in sizes]
            axes[idx].plot(
                sizes, theoretical, "--", label="Θ(n²)", alpha=0.7, linewidth=2
            )
        else:  # Merge Sort and Heap Sort
            # Θ(n log n) complexity
            c = max_steps[-1] / (sizes[-1] * np.log2(sizes[-1]))
            theoretical = [c * n * np.log2(n) for n in sizes]
            axes[idx].plot(
                sizes, theoretical, "--", label="Θ(n log n)", alpha=0.7, linewidth=2
            )

        axes[idx].set_xlabel("Input Size (n)")
        axes[idx].set_ylabel("Steps (Max)")
        axes[idx].set_title(name)
        axes[idx].legend()
        axes[idx].grid(True)

    plt.tight_layout()
    plt.savefig("sorting_comparison.png")
    print("Plot saved as sorting_comparison.png")
    plt.show()


if __name__ == "__main__":
    plot_sorting_algorithms()
