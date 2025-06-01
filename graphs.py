import pandas as pd
import matplotlib.pyplot as plt

def load_data(filepath):
    """Load CSV data and compute compression ratio."""
    df = pd.read_csv(filepath)
    df["Compression Ratio"] = df["Target Points"] / df["Original Points"]
    return df

def plot_compression_time_vs_ratio(df):
    """Plot Compression Time vs Compression Ratio."""
    plt.figure(figsize=(8, 6), dpi=200)
    plt.plot(df["Compression Ratio"], df["Compression Time (s)"], marker='o', linestyle='-')
    plt.title("Compression Time vs Compression Ratio")
    plt.xlabel("Compression Ratio")
    plt.ylabel("Avg. Compression Time (s)")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("compression_time_vs_ratio.png")
    plt.show()

def plot_chamfer_vs_ratio(df):
    """Plot Chamfer Distance vs Compression Ratio."""
    plt.figure(figsize=(8, 6), dpi=200)
    plt.plot(df["Compression Ratio"], df["CD"], marker='s', linestyle='-', color='green')
    plt.title("Chamfer Distance vs Compression Ratio")
    plt.xlabel("Compression Ratio")
    plt.ylabel("Avg. Chamfer Distance")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("chamfer_vs_ratio.png")
    plt.show()

def plot_hausdorff_vs_ratio(df):
    """Plot Hausdorff Distance vs Compression Ratio."""
    plt.figure(figsize=(8, 6), dpi=200)
    plt.plot(df["Compression Ratio"], df["HD"], marker='^', linestyle='-', color='red')
    plt.title("Hausdorff Distance vs Compression Ratio")
    plt.xlabel("Compression Ratio")
    plt.ylabel("Avg. Hausdorff Distance")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("hausdorff_vs_ratio.png")
    plt.show()

def main():
    filepath = "AVGDATA.csv"  # Replace with your actual CSV file
    df = load_data(filepath)
    plot_compression_time_vs_ratio(df)
    plot_chamfer_vs_ratio(df)
    plot_hausdorff_vs_ratio(df)

if __name__ == "__main__":
    main()
