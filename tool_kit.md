# ****Skyfall: Installation and Fine-Tuning Guide****

## ****Installation****

### Prerequisites
- Python 3.6 or higher  
- pip package manager

### Required Packages
Install the necessary dependencies:

pip install numpy open3d scikit-image scipy

### Verify Installation
To check that all packages are installed:

python -c "import numpy; import open3d; import skimage; import scipy; print('All dependencies installed successfully!')"

---

## ****Usage****

Run the script:

python mesh_generation.py

You will be prompted to enter the path to your point cloud file (.ply, .pcd, etc.).

---

## ****Fine-Tuning Parameters****

Adjust the parameters inside the `point_cloud_to_mesh` function for optimal results.

### Core Parameters

**`voxel_size`** (default: `0.1`)  
- Controls 3D grid resolution  
- Smaller = higher detail, slower  
- Larger = faster, less detail  
- Recommended range: `0.01 - 0.5`

**`iso_level_percentile`** (default: `20`)  
- Determines how tightly the mesh fits the point cloud  
- Lower values (5–15): tighter mesh  
- Higher values (25–50): smoother mesh

---

### Preprocessing Parameters

**`downsample_voxel_size`** (default: `0.5`)  
- Simplifies the input point cloud  
- Lower = more detail  
- Higher = faster processing

**Statistical Outlier Removal**  
- `nb_neighbors` (default: `50`)  
- `std_ratio` (default: `0.5`)  
  - Lower `std_ratio` removes more noise  
  - Higher keeps more points

**`max_grid_size`** (default: `500`)  
- Controls voxel grid memory size  
- Increase for high RAM machines  
- Decrease for limited hardware

---

## ****Optimization Tips****

### For Large Point Clouds
- Increase `downsample_voxel_size` (e.g., `1.0`)  
- Increase `voxel_size` (e.g., `0.2`)  
- Decrease `max_grid_size` if running out of memory

### For Detailed Results
- Lower `voxel_size` (e.g., `0.05`)  
- Lower `downsample_voxel_size` (e.g., `0.2`)  
- Set `iso_level_percentile` to `10–15`

### For Noisy Clouds
- Decrease `std_ratio` (e.g., `0.3`)  
- Increase `nb_neighbors` (e.g., `100`)  
- Increase `iso_level_percentile` (e.g., `30–40`)

### For Low Memory Systems
- Increase `voxel_size`  
- Decrease `max_grid_size`  
- Skyfall auto-adjusts based on dimensions

---

## ****Example Configurations****

### High-Quality LiDAR / Photogrammetry
voxel_size = 0.05  
downsample_voxel_size = 0.25  
iso_level_percentile = 15  
nb_neighbors = 50  
std_ratio = 0.5

### Noisy or Sparse Point Cloud
voxel_size = 0.15  
downsample_voxel_size = 0.75  
iso_level_percentile = 35  
nb_neighbors = 100  
std_ratio = 0.3

### Low-End Hardware
voxel_size = 0.25  
downsample_voxel_size = 1.0  
iso_level_percentile = 20  
max_grid_size = 300
