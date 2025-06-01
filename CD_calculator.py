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

# === CONFIG ===
original_file = "NRG-seminar/data/GK_462_100_500x500.laz"
compressed_dir = "NRG-seminar/data/compressed/FileSizeTest"
output_csv = "CD_forFileSizeTest.csv"

# === Load Original Point Cloud ===
print(f"Loading original: {original_file}")
pc_original = load_laz_to_numpy(original_file)

# === Process All Compressed Files ===
results = []
for filename in os.listdir(compressed_dir):
    if filename.endswith(".laz"):
        compressed_path = os.path.join(compressed_dir, filename)
        print(f"Processing: {filename}")
        try:
            pc_compressed = load_laz_to_numpy(compressed_path)
            cd = chamfer_distance(pc_original, pc_compressed)
            results.append((filename, cd))
        except Exception as e:
            print(f"Error with {filename}: {e}")
            results.append((filename, "ERROR"))

# === Save to CSV ===
with open(output_csv, mode='w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(["Compressed File", "Chamfer Distance"])
    writer.writerows(results)

print(f"\n✅ Results written to {output_csv}")
