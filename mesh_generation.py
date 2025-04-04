import numpy as np
import open3d as o3d
from skimage import measure
from scipy.spatial import cKDTree
import time  # For measuring execution time

def point_cloud_to_mesh(file_path):
    voxel_size = 0.1  # Initial voxel size for grid resolution
    iso_level_percentile = 20  # Percentile to determine the iso-surface level
    max_grid_size = 500  # Limit grid size to avoid excessive computation 

    try:
        start_time = time.time()
        print(f"Loading point cloud from {file_path}...")
        pcd = o3d.io.read_point_cloud(file_path)
        print(f"Point cloud loaded in {time.time() - start_time:.2f} seconds.")

        if pcd is None or len(np.asarray(pcd.points)) == 0:
            raise ValueError("The point cloud file is empty or could not be read.")

        # Step 1: Downsample the point cloud to reduce point count
        downsample_voxel_size = 0.5  # Aggressively reduce number of points
        print(f"Downsampling with voxel size {downsample_voxel_size}...")
        start_time = time.time()
        pcd = pcd.voxel_down_sample(voxel_size=downsample_voxel_size)
        print(f"Downsampling complete in {time.time() - start_time:.2f} seconds.")
        points = np.asarray(pcd.points)
        print(f"Number of points after initial downsampling: {len(points)}")

        # Step 2: Remove statistical outliers from the point cloud
        print("Removing outliers...")
        start_time = time.time()
        cl, ind = pcd.remove_statistical_outlier(nb_neighbors=50, std_ratio=0.5)  # Aggressive outlier filtering
        pcd = pcd.select_by_index(ind)  # type: ignore
        print(f"Outlier removal complete in {time.time() - start_time:.2f} seconds.")
        points = np.asarray(pcd.points)
        print(f"Number of points after outlier removal: {len(points)}")

        # Optional: Further downsample if still too many points
        if len(points) > 100000:
           print("Doing a second downsample")
           pcd = pcd.voxel_down_sample(voxel_size=downsample_voxel_size * 2)  # Even more aggressive
           points = np.asarray(pcd.points)
           print(f"Number of points after second downsample: {len(points)}")

        # Stop if the point count remains too high
        if len(points) > 300000:
            raise ValueError("Point count is still too high. Increase downsampling or outlier removal aggressiveness.")

        # Step 3: Determine spatial bounds of the point cloud
        mins = np.min(points, axis=0)
        maxs = np.max(points, axis=0)

        # Adjust voxel size to ensure the grid fits within memory limits
        grid_dimensions = np.ceil((maxs - mins) / voxel_size).astype(int)
        if np.any(grid_dimensions > max_grid_size):
            scaling_factor = np.max(grid_dimensions / max_grid_size)
            voxel_size *= scaling_factor
            print(f"Adjusted voxel size to {voxel_size} to limit grid dimensions.")

        # Step 4: Generate a 3D grid for scalar field calculation
        x = np.arange(mins[0], maxs[0], voxel_size)
        y = np.arange(mins[1], maxs[1], voxel_size)
        z = np.arange(mins[2], maxs[2], voxel_size)
        x, y, z = np.meshgrid(x, y, z, indexing='ij')

        # Step 5: Use KD-tree for efficient nearest neighbor search
        print("Creating KD-tree...")
        start_time = time.time()
        tree = cKDTree(points)
        print(f"KD-tree created in {time.time() - start_time:.2f} seconds.")

        # Step 6: Compute distances from grid points to nearest point cloud points
        print("Calculating distances...")
        start_time = time.time()
        grid_points = np.vstack([x.ravel(), y.ravel(), z.ravel()]).T
        distances, _ = tree.query(grid_points)  # Efficient distance computation

        if np.isnan(distances).any() or np.isinf(distances).any():
            raise ValueError("Distances contain NaN or Inf values.")

        scalar_field = distances.reshape(x.shape)
        del distances  # Free up memory
        print(f"Distances calculated in {time.time() - start_time:.2f} seconds.")

        # Step 7: Choose iso-level from the distance field
        iso_level = np.percentile(scalar_field, iso_level_percentile)
        print(f"Iso Level: {iso_level}")

        # Step 8: Use Marching Cubes algorithm to extract surface mesh
        print("Applying Marching Cubes...")
        start_time = time.time()
        verts, faces, _, _ = measure.marching_cubes(scalar_field, level=iso_level)  # type: ignore
        del scalar_field  # Free up memory
        print(f"Marching Cubes applied in {time.time() - start_time:.2f} seconds.")

        # Step 9: Transform vertices back to original coordinate space
        verts = verts * voxel_size + mins

        # Step 10: Construct a triangle mesh with the extracted surface
        print("Creating mesh...")
        mesh = o3d.geometry.TriangleMesh()
        mesh.vertices = o3d.utility.Vector3dVector(verts)
        mesh.triangles = o3d.utility.Vector3iVector(faces)
        del verts, faces  # Free up memory

        # Step 11: Compute normals for visualization
        mesh.compute_vertex_normals()

        # Step 12: Save the mesh to disk
        output_path = "output_mesh.ply"
        print(f"Saving mesh to {output_path}...")
        start_time = time.time()
        o3d.io.write_triangle_mesh(output_path, mesh)  # Save mesh to file
        print(f"Mesh saved in {time.time() - start_time:.2f} seconds.")

        print(f"Mesh saved as {output_path}")
        return output_path

    except Exception as e:
        print(f"Error during point cloud processing: {e}")
        return None


if __name__ == "__main__":
    file_path = input("Enter the path to the point cloud file: ")
    if file_path:
        output_path = point_cloud_to_mesh(file_path)
        if output_path:
            print(f"Successfully converted to mesh: {output_path}")
        else:
            print("Mesh conversion failed.")
    else:
        print("No file path provided.")