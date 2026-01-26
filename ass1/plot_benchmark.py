import pandas as pd
import matplotlib.pyplot as plt
import sys
import os


def plot_benchmark_results(
    go_csv="benchmark_results.csv", python_csv="python_benchmark_results.csv"
):
    if not os.path.exists(go_csv):
        print(f"Error: {go_csv} not found. Please run the Go benchmark first.")
        sys.exit(1)

    if not os.path.exists(python_csv):
        print(f"Error: {python_csv} not found. Please run the Python benchmark first.")
        sys.exit(1)

    # Read CSV files
    df_go = pd.read_csv(go_csv)
    df_go["Language"] = "Go"

    df_python = pd.read_csv(python_csv)
    df_python["Language"] = "Python"

    # Combine dataframes
    df = pd.concat([df_go, df_python], ignore_index=True)

    algorithms = ["InsertionSort", "MergeSort", "HeapSort", "QuickSort"]

    _, axes = plt.subplots(2, 2, figsize=(14, 10))
    axes = axes.flatten()

    # Plot each algorithm in its own subplot
    for idx, algorithm in enumerate(algorithms):
        ax = axes[idx]

        # Go data
        go_data = df_go[df_go["Algorithm"] == algorithm]
        ax.plot(
            go_data["InputSize"],
            go_data["TimeMs"],
            marker="o",
            label="Go",
            linewidth=2,
            color="C0",
        )

        # Python data
        python_data = df_python[df_python["Algorithm"] == algorithm]
        ax.plot(
            python_data["InputSize"],
            python_data["TimeMs"],
            marker="s",
            label="Python",
            linewidth=2,
            color="C1",
        )

        ax.set_xlabel("Input Size", fontsize=11)
        ax.set_ylabel("Execution Time (ms)", fontsize=11)
        ax.set_title(algorithm, fontsize=13, fontweight="bold")
        ax.legend()
        ax.grid(True, alpha=0.3)

    plt.tight_layout()

    output_file = "benchmark_comparison.png"
    plt.savefig(output_file, dpi=300, bbox_inches="tight")
    print(f"Plot saved to {output_file}")

    plt.show()

    # Print summary statistics
    print("\n=== Benchmark Summary ===")

    print("\n--- Go Implementation ---")
    print("Average execution time by algorithm (ms):")
    avg_times_go = df_go.groupby("Algorithm")["TimeMs"].mean().sort_values()
    for algo, time in avg_times_go.items():
        print(f"  {algo}: {time:.4f} ms")

    print("\n--- Python Implementation ---")
    print("Average execution time by algorithm (ms):")
    avg_times_python = df_python.groupby("Algorithm")["TimeMs"].mean().sort_values()
    for algo, time in avg_times_python.items():
        print(f"  {algo}: {time:.4f} ms")

    print("\n--- Go vs Python Speed Comparison ---")
    print("Speedup factor (Python time / Go time) for largest input size:")
    max_size = df["InputSize"].max()
    for algorithm in df_go["Algorithm"].unique():
        go_time = df_go[
            (df_go["Algorithm"] == algorithm) & (df_go["InputSize"] == max_size)
        ]["TimeMs"].values[0]
        python_time = df_python[
            (df_python["Algorithm"] == algorithm) & (df_python["InputSize"] == max_size)
        ]["TimeMs"].values[0]
        speedup = python_time / go_time
        print(f"  {algorithm}: {speedup:.2f}x (Go is {speedup:.2f}x faster)")

    print("\nExecution time for largest input size (10000):")
    max_size_data = df[df["InputSize"] == max_size].sort_values(["Language", "TimeMs"])
    for _, row in max_size_data.iterrows():
        print(f"  {row['Algorithm']} ({row['Language']}): {row['TimeMs']:.4f} ms")


if __name__ == "__main__":
    go_csv = sys.argv[1] if len(sys.argv) > 1 else "benchmark_results.csv"
    python_csv = sys.argv[2] if len(sys.argv) > 2 else "python_benchmark_results.csv"
    plot_benchmark_results(go_csv, python_csv)
