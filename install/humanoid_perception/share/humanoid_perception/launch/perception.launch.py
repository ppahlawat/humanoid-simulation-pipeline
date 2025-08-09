import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node

def generate_launch_description():

    # Get the path to the simulation launch file from the description package
    humanoid_description_pkg = get_package_share_directory('humanoid_description')
    spawn_humanoid_launch_path = os.path.join(
        humanoid_description_pkg,
        'launch',
        'spawn_humanoid.launch.py'
    )

    # 1. Include the Gazebo simulation launch file
    start_simulation_cmd = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(spawn_humanoid_launch_path)
    )

    # 2. Start the color detector node
    start_color_detector_cmd = Node(
        package='humanoid_perception',
        executable='color_detector',
        name='color_detector_node'
    )

    return LaunchDescription([
        start_simulation_cmd,
        start_color_detector_cmd
    ])
