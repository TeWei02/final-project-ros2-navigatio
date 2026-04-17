# Final Project - ROS2 Navigation Guide

## Current Status
- Docker daemon not running - need to start Docker Desktop
- ROS2 packages already downloaded and built in `~/ros2_navigation_workspace/`

## Files Ready
- `~/HW4_YOLO/detection.pt` - YOLO detection model
- `~/HW4_YOLO/segmentation.pt` - YOLO segmentation model

## How to Run When Docker is Ready

### Step 1: Start Docker Desktop
```bash
open -a Docker
# Wait for Docker to fully start
docker ps  # Should show empty list
```

### Step 2: Build Docker Image (first time only)
```bash
cd ~/ros2_navigation_workspace
docker-compose build
```

### Step 3: Run the Simulation (Terminal 1)
```bash
cd ~/ros2_navigation_workspace
docker-compose run --rm ros2-full ros2 launch bme_ros2_navigation spawn_robot.launch.py
```

### Step 4: Run Navigation (Terminal 2)
```bash
cd ~/ros2_navigation_workspace
docker-compose run --rm ros2-full ros2 launch bme_ros2_navigation navigation.launch.py
```

### Step 5: Run Waypoint Following (Terminal 3)
```bash
cd ~/ros2_navigation_workspace
docker-compose run --rm ros2-full ros2 run bme_ros2_navigation_py follow_waypoints
```

## Alternative: Direct Docker Commands
```bash
# Build
docker build -t ros2-jazzy-nav -f Dockerfile .

# Run simulation
docker run --rm -it \
  -v $(pwd)/src:/ros2_ws/src \
  -e DISPLAY=${DISPLAY} \
  --network host \
  ros2-jazzy-nav \
  ros2 launch bme_ros2_navigation spawn_robot.launch.py
```

## Course Topics Covered
1. **Mapping** - SLAM Toolbox for creating maps
2. **Localization** - AMCL for robot positioning
3. **Navigation** - Nav2 stack for path planning
4. **Waypoint Navigation** - Follow waypoints automatically
5. **Exploration** - Autonomous environment exploration

## Troubleshooting
- "Cannot connect to Docker": Start Docker Desktop app
- "X11 display error": Install XQuartz and enable network connections
- Permission issues: Check Docker Desktop settings