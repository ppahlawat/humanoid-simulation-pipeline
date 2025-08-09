import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node
from launch.substitutions import Command

def generate_launch_description():

    # --- Paths ---
    pkg_humanoid_description = get_package_share_directory('humanoid_description')
    pkg_humanoid_perception = get_package_share_directory('humanoid_perception')

    # --- Included Launch Files ---

    # 1. Include the launch file to start Gazebo and spawn the robot.
    start_simulation_cmd = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_humanoid_description, 'launch', 'spawn_humanoid.launch.py')
        )
    )

    # --- Nodes to Launch ---

    # 2. Start the Color Detector Node
    start_color_detector_cmd = Node(
        package='humanoid_perception',
        executable='color_detector',
        name='color_detector_node'
    )

    # 3. Start our new RViz Motion Controller
    start_rviz_motion_controller_cmd = Node(
        package='humanoid_final_control',
        executable='rviz_motion_controller',
        name='rviz_motion_controller_node'
    )

    # 4. Start RViz using your custom launch file
    # This is the corrected section
    start_rviz_cmd = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_humanoid_description, 'launch', 'view_humanoid.launch.py')
        )
    )

    return LaunchDescription([
        start_simulation_cmd,
        start_color_detector_cmd,
        start_rviz_motion_controller_cmd,
        start_rviz_cmd
    ])
