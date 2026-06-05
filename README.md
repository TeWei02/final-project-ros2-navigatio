# ROS2 Navigation — Final Project

NTHU RNE 2024 Final Project: autonomous robotic navigation with visual target detection and recovery.

## Architecture

- **`bme_ros2_navigation`** (C++ & Launch): Nav2 integration, YOLO detection bridge, mission launch files
- **`bme_ros2_navigation_py`** (Python): YOLO detector node, vision-based navigation state machine

## Mission Pipeline

1. **SEARCH** — Robot patrols waypoints autonomously
2. **TRACK** — Switches to visual tracking upon target detection via `/yolo/target_info`
3. **OBSERVE** — Waits 5s near target, sends `UNLOCK` command
4. **RECOVER** — Navigates back to base `(0, 0, 0)`

## Quick Start

```bash
cd ros2_navigation_workspace
colcon build --packages-select bme_ros2_navigation bme_ros2_navigation_py
source install/setup.bash
ros2 launch bme_ros2_navigation final_project_mission.launch.py
```

## Tech Stack

- ROS2 Humble
- Nav2 Stack
- YOLO (real-time object detection)
- Gazebo / Unity Simulation

## License

MIT