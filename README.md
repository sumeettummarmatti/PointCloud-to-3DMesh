# Skyfall

*By Jssateb Hackwell*

## Overview

Skyfall is a powerful tool that converts point cloud data into coherent 3D meshes using the Marching Cubes algorithm. It handles various point cloud formats regardless of capture method (LiDAR, photogrammetry, 3D Gaussian Splatting, etc.).

## Workflow

1. **Data Loading**
   - Loads point cloud data from standard formats (.ply, .pcd) using Open3D

2. **Preprocessing**
   - Downsamples point clouds to reduce complexity
   - Removes statistical outliers for cleaner results

3. **Scalar Field Generation**
   - Creates a 3D voxel grid around the point cloud
   - Uses KD-Tree for efficient nearest-neighbor searches
   - Calculates distances from grid points to nearest points in the cloud

4. **Surface Extraction**
   - Determines optimal iso-level threshold using percentile-based calculation
   - Applies Marching Cubes algorithm to extract surface mesh
   - Generates triangular mesh faces based on iso-surface intersections

5. **Post-processing**
   - Transforms vertices to original coordinate space
   - Computes vertex normals for proper visualization
   - Saves the final mesh to disk

## Key Features

- **Versatile**: Works with any point cloud data source
- **Parameterized Control**:
  - `voxel_size`: Controls detail level and processing speed
  - `iso_level_percentile`: Determines how closely the mesh follows the point cloud
- **Automatic Parameter Adjustment**: Adjusts voxel size based on point cloud dimensions
- **Robust Preprocessing**: Handles noisy or large point clouds effectively
- **Performance Monitoring**: Reports execution time for each processing step
- **Memory Efficient**: Optimized memory management for large datasets

## Technical Details: Marching Cubes Algorithm

The algorithm converts a scalar field (distance values) into a triangle mesh by:

1. Creating a 3D grid and calculating distances to form a scalar field
2. Determining an iso-level threshold that defines the surface boundary
3. Processing each cube (voxel) to determine inside/outside configuration
4. Generating triangles based on how the surface intersects each cube

## Future Improvements

- Adaptive resolution for variable detail levels
- Enhanced parallelization for larger datasets
- Texture mapping from point cloud to mesh
- Machine learning integration for improved surface prediction
- Real-time processing capabilities
- Semantic segmentation integration
- Enhanced web interface with interactive features
