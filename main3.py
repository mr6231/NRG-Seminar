from src.point_cloud import PointCloud
from src.sensitivity_sampling import SensitivitySampling

import numpy as np
import os
import time
import tracemalloc
import pandas as pd

# Configuration
INPUT_FOLDER = "NRG-seminar/data/"
OUTPUT_FOLDER = "NRG-seminar/data/compressed"
CSV_LOG_PATH = os.path.join(OUTPUT_FOLDER, "compression_log.csv")
TARGET_POINTS = 100000  # constant target for compression

# Create output folder if it doesn't exist
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# Get all .las or .laz files in input folder
input_files = [f for f in os.listdir(INPUT_FOLDER) if f.endswith((".las", ".laz"))]

# Store results for CSV
results = []

for i, file_name in enumerate(input_files):
    input_path = os.path.join(INPUT_FOLDER, file_name)
    print(f"\n[{i}] Processing: {file_name}")

    # Load point cloud
    pc = PointCloud.from_laz_file(input_path)
    original_point_count = len(pc.points_x)

    print(f"Original points: {original_point_count}")

    ss = SensitivitySampling(pc)

    # Measure time and memory usage
    tracemalloc.start()
    start_time = time.time()

    compressed_pc = ss.compress(TARGET_POINTS)

    end_time = time.time()
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    compression_time = end_time - start_time
    memory_MB = peak / 1024 / 1024

    # Export compressed point cloud
    base_name = os.path.splitext(file_name)[0]
    out_file_name = f"{i}_{base_name}_compressed_{TARGET_POINTS}.laz"
    out_path = os.path.join(OUTPUT_FOLDER, out_file_name)
    compressed_pc.export_to_laz_file(out_path)

    # Log results
    results.append({
        "Index": i,
        "Input File": file_name,
        "Original Points": original_point_count,
        "Compressed Points": TARGET_POINTS,
        "Compression Time (s)": compression_time,
        "Peak Memory Usage (MB)": memory_MB,
    })

    print(f"→ Done: {compression_time:.2f}s, {memory_MB:.2f} MB used.")

# Save results to CSV
df = pd.DataFrame(results)
df.to_csv(CSV_LOG_PATH, index=False)
print(f"\n✅ All files processed. Log saved to {CSV_LOG_PATH}")
