import csv
from collections import defaultdict

def average_by_target(input_path, output_path):
    grouped_data = defaultdict(list)

    # Read and group rows by Target Points
    with open(input_path, newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            key = row['Target Points']
            grouped_data[key].append(row)

    # Define output structure
    fieldnames = [
        'Target Points',
        'Original Points',
        'Average Compression Time (s)',
        'Average HD',
        'Average CD',
        'Average Kmeans Time',
        'Num Samples'
    ]

    with open(output_path, mode='w', newline='') as f_out:
        writer = csv.DictWriter(f_out, fieldnames=fieldnames)
        writer.writeheader()

        for target, rows in grouped_data.items():
            n = len(rows)
            avg = lambda field: sum(float(row[field]) for row in rows) / n

            writer.writerow({
                'Target Points': target,
                'Original Points': rows[0]['Original Points'],
                'Average Compression Time (s)': f"{avg('Compression Time (s)'):.4f}",
                'Average HD': f"{avg('HD'):.6f}",
                'Average CD': f"{avg('CD'):.6f}",
                'Average Kmeans Time': f"{avg('Kmeans Time'):.4f}",
                'Num Samples': n
            })

    print(f"✅ Averaged CSV written to: {output_path}")

if __name__ == "__main__":
    input_path = "MAIN DATA.csv"
    output_path = "AVGDATA.csv"
    average_by_target(input_path, output_path)
