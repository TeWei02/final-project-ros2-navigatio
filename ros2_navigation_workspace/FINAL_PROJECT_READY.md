# Final Project - ROS2 Navigation Complete Guide

## ✅ Docker 環境已就緒

ROS2 Jazzy 容器已成功構建，包含：
- nav2_bringup, nav2_amcl
- slam_toolbox
- bme_ros2_navigation
- bme_ros2_navigation_py

## 🚀 如何運行 Final Project

### 終端機 1 - 啟動模擬器
```bash
cd ~/ros2_navigation_workspace
docker-compose run --rm ros2-full ros2 launch bme_ros2_navigation spawn_robot.launch.py
```

### 終端機 2 - 啟動導航
```bash
cd ~/ros2_navigation_workspace
docker-compose run --rm ros2-full ros2 launch bme_ros2_navigation navigation.launch.py
```

### 終端機 3 - 顯示 Waypoints
```bash
cd ~/ros2_navigation_workspace
docker-compose run --rm ros2-full ros2 run bme_ros2_navigation_py follow_waypoints
```

## 📋 Final Project 課程內容

1. **Mapping** - 使用 SLAM Toolbox 建立地圖
2. **Localization** - 使用 AMCL 定位
3. **Navigation** - 路徑規劃與導航
4. **Waypoint Navigation** - 自動跟隨航點
5. **Exploration** - 自主環境探索

## 🔧 整合 YOLO 模型

將 HW4 訓練的模型複製到 ROS2 套件中：
```bash
# 在主機上執行
cp ~/HW4_YOLO/detection.pt ~/ros2_navigation_workspace/src/bme_ros2_navigation/models/
cp ~/HW4_YOLO/segmentation.pt ~/ros2_navigation_workspace/src/bme_ros2_navigation/models/
```

## ⚠️ 注意事項

- 需要 XQuartz 才能顯示 GUI
- 請確保 Docker Desktop 正在運行
- 第一次啟動可能需要幾分鐘