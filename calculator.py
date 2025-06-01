import os
import csv
import laspy
import numpy as np
import open3d as o3d

def load_laz_to_numpy(filepath):
    las = laspy.read(filepath)
    return np.vstack((las.x, las.y, las.z)).T

def chamfer_distance(pc1, pc2):
    pcd1 = o3d.geometry.PointCloud()
    pcd1.points = o3d.utility.Vector3dVector(pc1)

    pcd2 = o3d.geometry.PointCloud()
    pcd2.points = o3d.utility.Vector3dVector(pc2)

    dists1 = np.asarray(pcd1.compute_point_cloud_distance(pcd2))
    dists2 = np.asarray(pcd2.compute_point_cloud_distance(pcd1))

    return np.mean(dists1**2) + np.mean(dists2**2)

def hausdorff_distance(pc1, pc2):
    pcd1 = o3d.geometry.PointCloud()
    pcd1.points = o3d.utility.Vector3dVector(pc1)

    pcd2 = o3d.geometry.PointCloud()
    pcd2.points = o3d.utility.Vector3dVector(pc2)

    dists1 = np.asarray(pcd1.compute_point_cloud_distance(pcd2))
    dists2 = np.asarray(pcd2.compute_point_cloud_distance(pcd1))

    return max(np.max(dists1), np.max(dists2))

def process_csv(input_csv, original_file_path, compressed_dir, output_csv):
    original_pc = load_laz_to_numpy(original_file_path)

    results = []
    with open(input_csv, newline='') as infile:
        reader = csv.DictReader(infile)
        for row in reader:
            iteration = row["Iteration"]
            target_pts = row["Target Points"]
            original_pts = row["Original Points"]
            comp_time = row["Compression Time (s)"]
            kmeans_time = row.get("Kmeans Time", "N/A")

            compressed_filename = f"{iteration}_{target_pts}_compressed.laz"
            compressed_path = os.path.join(compressed_dir, compressed_filename)

            if not os.path.exists(compressed_path):
                print(f"WARNING: File not found: {compressed_path}")
                continue

            compressed_pc = load_laz_to_numpy(compressed_path)

            hd = hausdorff_distance(original_pc, compressed_pc)
            cd = chamfer_distance(original_pc, compressed_pc)

            results.append({
                "Iteration": iteration,
                "Target Points": target_pts,
                "Original Points": original_pts,
                "Compression Time (s)": comp_time,
                "Compressed File": compressed_filename,
                "Hausdorff Distance": f"{hd:.6f}",
                "Chamfer Distance": f"{cd:.6f}",
                "Kmeans Time": kmeans_time
            })

    # Write to output CSV
    fieldnames = [
        "Iteration", "Target Points", "Original Points",
        "Compression Time (s)", "Compressed File",
        "Hausdorff Distance", "Chamfer Distance", "Kmeans Time"
    ]
    with open(output_csv, mode='w', newline='') as outfile:
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()
        for r in results:
            writer.writerow(r)

    print(f"✅ Results saved to: {output_csv}")

if __name__ == "__main__":
    # Set your paths here
    input_csv = "NRG-seminar/data/compressed/compression_results.csv"
    original_file = "NRG-seminar/data/GK_462_100_500x500.laz"
    compressed_dir = "NRG-seminar/data/compressed/"
    output_csv = "NRG-seminar/data/compression_metrics.csv"

    process_csv(input_csv, original_file, compressed_dir, output_csv)
