from src.point_cloud import PointCloud
from src.sensitivity_sampling import SensitivitySampling

import numpy as np
import os
import time
import tracemalloc
import pandas as pd

# Setup
original_file = "NRG-seminar/data/GK_462_100_500x500.laz"
output_folder = "NRG-seminar/data/compressed"
os.makedirs(output_folder, exist_ok=True)

# Load original point cloud
pc = PointCloud.from_laz_file(original_file)
print(f"Original point cloud loaded: {len(pc.points_x)} points")

kmeans_start_time = time.time()
pc.kmeans()
kmeans_end_time = time.time()
# Compression targets
compression_targets = [1000000, 1000000, 1000000, 
                       1500000, 1500000, 1500000, 
                       2000000, 2000000, 2000000,
                       2500000, 2500000, 2500000,
                       3000000, 3000000, 3000000,
                       3500000, 3500000, 3500000,
                       4000000, 4000000, 4000000]

# To store evaluation metrics
results = []

for i, target_points in enumerate(compression_targets):
    print(f"\nCompressing to {target_points} points...")

    ss_start_time = time.time()
    ss = SensitivitySampling(pc)
    ss_end_time = time.time()
    
    # Measure time and memory
    tracemalloc.start()
    start_time = time.time()

    compressed_pc = ss.compress(target_points)

    end_time = time.time()
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    # Export compressed point cloud
    out_path = os.path.join(output_folder, f"{i}_{target_points}_compressed.laz")
    compressed_pc.export_to_laz_file(out_path)

    # Log metrics
    compression_time = end_time - start_time
    ss_time = ss_end_time - ss_start_time
    kmeans_time= kmeans_end_time - kmeans_start_time
    memory_MB = peak / 1024 / 1024

    results.append({
        "Iteration": i,
        "Target Points": target_points,
        "Original Points": len(pc.points_x),
        "Compression Time (s)": compression_time,
        "Sensitivity Sampling Time (s)": ss_time,
        "Peak Memory Usage (MB)": memory_MB,
        "Kmeans Time": kmeans_time
    })

    print(f"Done in {compression_time:.2f}s, peak memory: {memory_MB:.2f} MB")

# Save results to CSV
df = pd.DataFrame(results)
csv_path = os.path.join(output_folder, "compression_results.csv")
df.to_csv(csv_path, index=False)

print(f"\nAll compression steps completed. Results saved to {csv_path}")
