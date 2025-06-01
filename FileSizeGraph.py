import csv
import matplotlib.pyplot as plt

def read_csv(filepath):
    data = {
        'Original Points': [],
        'Compression Time (s)': [],
        'Peak Memory Usage (MB)': [],
        'HD': [],
        'CD': []
    }

    with open(filepath, newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            data['Original Points'].append(int(row['Original Points']))
            data['Compression Time (s)'].append(float(row['Compression Time (s)']))
            data['Peak Memory Usage (MB)'].append(float(row['Peak Memory Usage (MB)']))
    return data

def plot_metric(x, y, x_label, y_label, title, filename):
    plt.figure(dpi=200)
    plt.scatter(x, y, color='blue')
    plt.plot(x, y, linestyle='--', color='gray')
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.title(title)
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(filename)
    print(f"📊 Saved plot: {filename}")
    plt.close()

def main():
    input_path = "NRG-seminar/data/compressed/FileSizeTest/compression_log.csv"  # ← Change if needed
    data = read_csv(input_path)

    x = data['Original Points']

    plot_metric(x, data['Compression Time (s)'],
                "Original Points", "Compression Time (s)",
                "Compression Time vs Original Points",
                "compression_time_vs_original_points.png")

    plot_metric(x, data['Peak Memory Usage (MB)'],
                "Original Points", "Peak Memory Usage (MB)",
                "Memory Usage vs Original Points",
                "memory_usage_vs_original_points.png")

if __name__ == "__main__":
    main()
