import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.conditions import IfCondition
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node


def generate_launch_description():
    pkg_bme_ros2_navigation = get_package_share_directory("bme_ros2_navigation")

    gazebo_models_path, _ = os.path.split(pkg_bme_ros2_navigation)
    gz_resource_path = os.environ.get("GZ_SIM_RESOURCE_PATH", "")
    os.environ["GZ_SIM_RESOURCE_PATH"] = (
        f"{gz_resource_path}{os.pathsep}{gazebo_models_path}"
        if gz_resource_path
        else gazebo_models_path
    )

    rviz_launch_arg = DeclareLaunchArgument(
        "rviz", default_value="true", description="Open RViz"
    )

    rviz_config_arg = DeclareLaunchArgument(
        "rviz_config", default_value="mapping.rviz", description="RViz config file"
    )

    sim_time_arg = DeclareLaunchArgument(
        "use_sim_time", default_value="True", description="Flag to enable use_sim_time"
    )

    interactive_marker_config_file_path = os.path.join(
        get_package_share_directory("interactive_marker_twist_server"),
        "config",
        "linear.yaml",
    )

    slam_toolbox_launch_path = os.path.join(
        get_package_share_directory("slam_toolbox"),
        "launch",
        "online_async_launch.py",
    )

    slam_toolbox_params_path = os.path.join(
        pkg_bme_ros2_navigation,
        "config",
        "slam_toolbox_mapping.yaml",
    )

    rviz_node = Node(
        package="rviz2",
        executable="rviz2",
        arguments=[
            "-d",
            PathJoinSubstitution(
                [pkg_bme_ros2_navigation, "rviz", LaunchConfiguration("rviz_config")]
            ),
        ],
        condition=IfCondition(LaunchConfiguration("rviz")),
        parameters=[{"use_sim_time": LaunchConfiguration("use_sim_time")}],
    )

    interactive_marker_twist_server_node = Node(
        package="interactive_marker_twist_server",
        executable="marker_server",
        name="twist_server_node",
        parameters=[interactive_marker_config_file_path],
        output="screen",
    )

    slam_toolbox_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(slam_toolbox_launch_path),
        launch_arguments={
            "use_sim_time": LaunchConfiguration("use_sim_time"),
            "slam_params_file": slam_toolbox_params_path,
        }.items(),
    )

    launch_description = LaunchDescription()

    launch_description.add_action(rviz_launch_arg)
    launch_description.add_action(rviz_config_arg)
    launch_description.add_action(sim_time_arg)
    launch_description.add_action(rviz_node)
    launch_description.add_action(interactive_marker_twist_server_node)
    launch_description.add_action(slam_toolbox_launch)

    return launch_description
