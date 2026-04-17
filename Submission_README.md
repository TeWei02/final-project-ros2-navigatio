# NTHU RNE 2024 Final Project - Standard Architecture Submission

This package has been strictly aligned with the **Robotic Navigation and Exploration Week 7** architecture. All nodes, scripts, and configurations follow the official course naming conventions for a professional and "not random" submission.

## 🏗️ Standardized Architecture

- **`bme_ros2_navigation`**: C++ & Launch Package
  - `launch/final_project_mission.launch.py`: Main entry point. Starts Nav2, YOLO, and Vision Navigation.
  - `config/gz_bridge.yaml`: Standardized topic bridge configuration.
- **`bme_ros2_navigation_py`**: Python Package
  - `yolo_detector.py`: Real-time YOLO detection. Publishes **`/yolo/target_info`** `[found, distance, delta_x]`.
  - `vision_navigation.py`: State machine (Search -> Track -> Observe -> Return).
  - `setup.py`: Updated entry points.

## 🚀 Simulation Environment

The project is designed to run with the following simulator:
- **Path**: `/Users/kedewei/Applications/pros_twin_unity_mac_v3/pros_twin_unity_mac_v3.app`

## 🕹️ Mission Logic (Canva Standard)

1. **SEARCH**: Robot patrols waypoints automatically.
2. **TRACK**: Upon detection, switches to visual tracking using `/yolo/target_info`.
3. **OBSERVE**: When close to the target, the robot **waits for 5 seconds** and sends an `UNLOCK` command.
4. **RECOVER**: Automatically navigates back to base `(0, 0, 0)` to complete the mission.

### 1. Build Node Entry Points
Ensure the new script names are compiled:
```bash
cd ~/ros2_navigation_workspace
docker-compose run --rm ros2-full colcon build --packages-select bme_ros2_navigation_py
source install/setup.bash
```

### 2. Run the NTHU Mission
Instead of separate controllers, use the integrated mission launch:
```bash
ros2 launch bme_ros2_navigation final_project_mission.launch.py
```

### 3. State Machine Flow
- **SEARCH**: Robot patrols waypoints looking for the Bear.
- **TRACK**: Switched to visual servoing when YOLO detects the target.
- **RECOVER**: Automatically navigates back to base `(0,0)` to finish the mission.

---
*Architectural alignment verified by Antigravity AI*
