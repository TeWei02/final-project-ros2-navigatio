# ROS2 Navigation — Final Project: Vision-Guided Autonomous Navigation

[![ROS2](https://img.shields.io/badge/ROS2-Humble-%2322314E?logo=ros)](https://docs.ros.org/en/humble/)
[![C++](https://img.shields.io/badge/C++-17-%2300599C?logo=c%2B%2B)](https://isocpp.org/)
[![Python](https://img.shields.io/badge/Python-3-%233776AB?logo=python)](https://www.python.org/)
[![YOLO](https://img.shields.io/badge/YOLO-Object%20Detection-%2300FFFF)](https://github.com/ultralytics/ultralytics)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

NTHU RNE 2024 Final Project: autonomous robotic navigation with visual target detection and autonomous recovery.

## Architecture

| Module | Language | Responsibility |
|--------|----------|---------------|
| `bme_ros2_navigation` | C++ + Launch | Nav2 integration, YOLO detection bridge, mission orchestration |
| `bme_ros2_navigation_py` | Python | YOLO detector node, vision-based navigation state machine |

## Mission Pipeline

| Phase | Action | Description |
|-------|--------|-------------|
| 1. SEARCH | Waypoint patrol | Robot autonomously patrols predefined waypoints |
| 2. TRACK | Visual tracking | Switches to visual tracking upon target detection via `/yolo/target_info` |
| 3. OBSERVE | Hold position | Waits 5s near target, sends `UNLOCK` command |
| 4. RECOVER | Return to base | Navigates back to origin `(0, 0, 0)` |

## Quick Start

```bash
cd ros2_navigation_workspace
colcon build --packages-select bme_ros2_navigation bme_ros2_navigation_py
source install/setup.bash
ros2 launch bme_ros2_navigation final_project_mission.launch.py
```

## Tech Stack

| Component | Technology |
|-----------|-----------|
| Framework | ROS2 Humble |
| Navigation | Nav2 Stack (AMCL, DWA, global/local planners) |
| Perception | YOLO real-time object detection |
| Simulation | Gazebo / Unity |
| Sensor Fusion | EKF, SLAM Toolbox |

## Project Structure

```
final-project-ros2-navigatio/
├── ros2_navigation_workspace/
│   ├── src/
│   │   └── bme_ros2_navigation/      # C++ packages + configs
│   │       ├── config/                # AMCL, EKF, Nav2, SLAM params
│   │       ├── launch/                # Mission launch files
│   │       └── CMakeLists.txt
│   ├── setup.sh                       # Environment setup
│   └── README.md
├── Submission_README.md
└── README.md
```

## License

MIT
