import csv

def simplify_csv(input_path, output_path):
    with open(input_path, newline='') as f_in, open(output_path, mode='w', newline='') as f_out:
        reader = csv.DictReader(f_in)

        # Desired output fieldnames and order
        fieldnames = [
            'Iteration',
            'Target Points',
            'Original Points',
            'Compression Time (s)',
            'Compressed File',
            'Hausdorff Distance',
            'Chamfer Distance',
            'Kmeans Time'
        ]

        writer = csv.DictWriter(f_out, fieldnames=fieldnames)
        writer.writeheader()

        for row in reader:
            simplified_row = {key: row.get(key, "N/A") for key in fieldnames}
            writer.writerow(simplified_row)

    print(f"✅ Simplified CSV written to: {output_path}")

if __name__ == "__main__":
    input_path = "final_combined_metrics.csv"
    output_path = "MAINDATA2.csv"

    simplify_csv(input_path, output_path)
