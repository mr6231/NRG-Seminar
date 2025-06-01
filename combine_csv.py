import csv

def extract_iteration_from_filename(filename):
    """Extracts iteration from filename like '3_1000000_compressed.laz' → '3'"""
    return filename.split('_')[0]

def load_chamfer_csv(path):
    chamfer_data = {}
    with open(path, newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            iteration = extract_iteration_from_filename(row['Compressed File'])
            chamfer_data[iteration] = row['Chamfer Distance']
    return chamfer_data

def load_hausdorff_csv(path):
    hausdorff_data = {}
    with open(path, newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            iteration = extract_iteration_from_filename(row['Compressed File'])
            hausdorff_data[iteration] = row['Hausdorff Distance']
    return hausdorff_data

def merge_csvs(csv1_path, csv2_path, csv3_path, output_path):
    chamfer = load_chamfer_csv(csv2_path)
    hausdorff = load_hausdorff_csv(csv3_path)

    with open(csv1_path, newline='') as f_in, open(output_path, mode='w', newline='') as f_out:
        reader = csv.DictReader(f_in)
        fieldnames = reader.fieldnames + [
            'Compressed File', 'Chamfer Distance', 'Hausdorff Distance', 'Compression Ratio'
        ]
        writer = csv.DictWriter(f_out, fieldnames=fieldnames)
        writer.writeheader()

        for row in reader:
            iteration = row['Iteration']
            target = float(row['Target Points'])
            original = float(row['Original Points'])

            row['Compressed File'] = f"{iteration}_{int(target)}_compressed.laz"
            row['Chamfer Distance'] = chamfer.get(iteration, "N/A")
            row['Hausdorff Distance'] = hausdorff.get(iteration, "N/A")
            row['Compression Ratio'] = f"{target / original:.6f}" if original else "N/A"
            writer.writerow(row)

    print(f"✅ Merged CSV written to: {output_path}")

if __name__ == "__main__":
    # Define file paths here
    csv1_path = "NRG-seminar/data/compressed/CompressionRateTest/compression_results.csv"
    csv2_path = "CD_forCompressionRateTest.csv"
    csv3_path = "HD_forCompressionRateTest.csv"
    output_path = "final_combined_metrics.csv"

    merge_csvs(csv1_path, csv2_path, csv3_path, output_path)
