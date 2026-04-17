# ROS2 Jazzy Navigation Course Setup for macOS

This setup allows you to run the ROS2 Jazzy navigation course on macOS using Docker.

## Prerequisites

1. **Install Docker Desktop for Mac**
   - Download from: https://www.docker.com/products/docker-desktop
   - Install and start Docker Desktop

2. **Allow X11 forwarding (for GUI applications)**
   - Install XQuartz: `brew install xquartz`
   - Start XQuartz and allow connections from network clients
   - In XQuartz preferences → Security → Allow connections from network clients

## Setup Steps

1. **Build the Docker image:**
   ```bash
   cd ~/ros2_navigation_workspace
   docker-compose build
   ```

2. **Copy the course repository:**
   ```bash
   # The repository should already be cloned to ~/Week-7-8-ROS2-Navigation
   # If not, clone it:
   git clone -b starter-branch https://github.com/MOGI-ROS/Week-7-8-ROS2-Navigation ~/Week-7-8-ROS2-Navigation
   ```

3. **Start the container and run setup:**
   ```bash
   docker-compose run --rm ros2-navigation ./setup.sh
   ```

## Running the Course

After setup, you can start learning:

Use the commands below from `~/ros2_navigation_workspace`.
If you use `docker run` directly, include the `build` mount so symlink-install packages resolve correctly.

### Terminal 1 - Simulator
```bash
docker run --rm \
   -v $(pwd)/src:/ros2_ws/src \
   -v $(pwd)/build:/ros2_ws/build \
   -v $(pwd)/install:/ros2_ws/install \
   -v $(pwd)/log:/ros2_ws/log \
   -e DISPLAY=${DISPLAY} \
   -e QT_X11_NO_MITSHM=1 \
   --network host \
   ros2-jazzy-navigation \
   ros2 launch bme_ros2_navigation spawn_robot.launch.py
```

### Terminal 2 - Choose a feature

#### Mapping
```bash
docker run --rm \
   -v $(pwd)/src:/ros2_ws/src \
   -v $(pwd)/build:/ros2_ws/build \
   -v $(pwd)/install:/ros2_ws/install \
   -v $(pwd)/log:/ros2_ws/log \
   -e DISPLAY=${DISPLAY} \
   -e QT_X11_NO_MITSHM=1 \
   --network host \
   ros2-jazzy-navigation \
   ros2 launch bme_ros2_navigation mapping.launch.py
```

#### Localization
```bash
docker run --rm \
   -v $(pwd)/src:/ros2_ws/src \
   -v $(pwd)/build:/ros2_ws/build \
   -v $(pwd)/install:/ros2_ws/install \
   -v $(pwd)/log:/ros2_ws/log \
   -e DISPLAY=${DISPLAY} \
   -e QT_X11_NO_MITSHM=1 \
   --network host \
   ros2-jazzy-navigation \
   ros2 launch bme_ros2_navigation localization.launch.py
```

#### Navigation
```bash
docker run --rm \
   -v $(pwd)/src:/ros2_ws/src \
   -v $(pwd)/build:/ros2_ws/build \
   -v $(pwd)/install:/ros2_ws/install \
   -v $(pwd)/log:/ros2_ws/log \
   -e DISPLAY=${DISPLAY} \
   -e QT_X11_NO_MITSHM=1 \
   --network host \
   ros2-jazzy-navigation \
   ros2 launch bme_ros2_navigation navigation.launch.py
```

#### Exploration
```bash
docker run --rm \
   -v $(pwd)/src:/ros2_ws/src \
   -v $(pwd)/build:/ros2_ws/build \
   -v $(pwd)/install:/ros2_ws/install \
   -v $(pwd)/log:/ros2_ws/log \
   -e DISPLAY=${DISPLAY} \
   -e QT_X11_NO_MITSHM=1 \
   --network host \
   ros2-jazzy-navigation \
   ros2 launch bme_ros2_navigation exploration.launch.py
```

#### Waypoint navigation
```bash
docker run --rm \
   -v $(pwd)/src:/ros2_ws/src \
   -v $(pwd)/build:/ros2_ws/build \
   -v $(pwd)/install:/ros2_ws/install \
   -v $(pwd)/log:/ros2_ws/log \
   -e DISPLAY=${DISPLAY} \
   -e QT_X11_NO_MITSHM=1 \
   --network host \
   ros2-jazzy-navigation \
   ros2 run bme_ros2_navigation_py follow_waypoints
```

For GUI tools, make sure XQuartz is running and accepting connections.

## Course Topics

The course covers:

1. **Mapping** - Using SLAM Toolbox to create environment maps
2. **Localization** - AMCL and SLAM-based robot positioning
3. **Navigation** - Path planning and waypoint navigation
4. **Exploration** - Autonomous environment exploration

## Troubleshooting

- **GUI not showing**: Make sure XQuartz is running and allows network connections
- **Container issues**: Try `docker-compose down` then rebuild
- **Permission issues**: The Docker setup should handle permissions automatically

## Learning Resources

- Course repository: https://github.com/MOGI-ROS/Week-7-8-ROS2-Navigation
- ROS2 Documentation: https://docs.ros.org/en/jazzy/
- Nav2 Documentation: https://navigation.ros.org/