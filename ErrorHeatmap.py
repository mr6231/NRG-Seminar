import numpy as np
import open3d as o3d
import matplotlib.pyplot as plt
import laspy

def read_laz_to_numpy(path):
    las = laspy.read(path)
    return np.vstack((las.x, las.y, las.z)).T


def compute_errors(original_pts, compressed_pts):
    # Build KDTree on original
    pcd_orig = o3d.geometry.PointCloud()
    pcd_orig.points = o3d.utility.Vector3dVector(original_pts)
    tree = o3d.geometry.KDTreeFlann(pcd_orig)

    # Compute nearest neighbor error for each compressed point
    errors = []
    for pt in compressed_pts:
        _, _, dists = tree.search_knn_vector_3d(pt, 1)
        errors.append(np.sqrt(dists[0]))  # Euclidean distance

    return np.array(errors)

def colorize_point_cloud(points, errors):
    max_error = np.max(errors)
    colors = plt.cm.jet(errors / (max_error + 1e-9))[:, :3]
    pcd = o3d.geometry.PointCloud()
    pcd.points = o3d.utility.Vector3dVector(points)
    pcd.colors = o3d.utility.Vector3dVector(colors)
    return pcd

def save_csv(points, errors, path="compressed_with_error.csv"):
    data = np.hstack([points, errors[:, None]])
    np.savetxt(path, data, delimiter=",", header="x,y,z,error", comments="")

def main():
    original_path = "NRG-seminar/data/GK_462_100_500x500.laz"
    compressed_path = "NRG-seminar/data/compressed/CompressionRateTest/20_500000_compressed.laz"

    print("Loading point clouds...")
    original_pts = read_laz_to_numpy(original_path)
    compressed_pts = read_laz_to_numpy(compressed_path)

    print("Computing nearest neighbor errors...")
    errors = compute_errors(original_pts, compressed_pts)

    print("Visualizing error heatmap...")
    pcd_colored = colorize_point_cloud(compressed_pts, errors)
    o3d.visualization.draw_geometries([pcd_colored])

    print("Saving error data to CSV...")
    save_csv(compressed_pts, errors)
    print("Done.")

if __name__ == "__main__":
    main()
