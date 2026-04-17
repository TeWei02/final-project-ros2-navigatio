#!/bin/bash

echo "Setting up ROS2 Navigation workspace..."

# Copy the downloaded repository to src if not already done
if [ ! -f "src/bme_ros2_navigation/package.xml" ]; then
	if [ -f "/host/Week-7-8-ROS2-Navigation/bme_ros2_navigation/package.xml" ]; then
		cp -r /host/Week-7-8-ROS2-Navigation/* src/
		echo "Copied source files from host"
	else
		echo "Warning: Source files not found. Please ensure Week-7-8-ROS2-Navigation is available"
	fi
fi

# Build the workspace
echo "Building workspace..."
colcon build --symlink-install

# Source the setup
echo "Sourcing setup..."
source install/setup.bash

echo "======================================"
echo "Setup complete!"
echo "======================================"
echo ""
echo "You can now run:"
echo "  ros2 launch bme_ros2_navigation spawn_robot.launch.py"
echo ""
echo "To start the navigation course, run:"
echo "  ros2 launch bme_ros2_navigation mapping.launch.py"
echo ""
echo "======================================"
