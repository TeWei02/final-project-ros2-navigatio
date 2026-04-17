import os

from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription, TimerAction
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node

def generate_launch_description():
    # Nodes from bme_ros2_navigation_py
    yolo_detector = Node(
        package='bme_ros2_navigation_py',
        executable='yolo_detector',
        name='yolo_detector_node',
        output='screen'
    )
    
    # We add a delay to the controller so Nav2 and YOLO have time to start
    final_controller = TimerAction(
        period=5.0,
        actions=[
            Node(
                package='bme_ros2_navigation_py',
                executable='vision_navigation',
                name='vision_navigation',
                output='screen'
            )
        ]
    )

    return LaunchDescription([
        yolo_detector,
        final_controller
    ])
