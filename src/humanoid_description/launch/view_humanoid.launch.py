import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch.conditions import IfCondition
import xacro

def generate_launch_description():

    # Launch argument to toggle the GUI
    use_gui = LaunchConfiguration('use_gui')

    # 🎯 Get the path to the URDF file from the CORRECT package
    pkg_path = get_package_share_directory('humanoid_description')
    xacro_file = os.path.join(pkg_path, 'urdf', 'humanoid.urdf.xacro')
    
    # Process the Xacro file to generate the URDF XML
    robot_description_config = xacro.process_file(xacro_file)
    robot_description = {'robot_description': robot_description_config.toxml()}

    # --- Nodes to Launch ---

    # 1. Robot State Publisher
    node_robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        output='screen',
        parameters=[robot_description]
    )

    # 2. Joint State Publisher GUI
    node_joint_state_publisher_gui = Node(
        package='joint_state_publisher_gui',
        executable='joint_state_publisher_gui',
        condition=IfCondition(use_gui)
    )

    # 3. RViz2
    node_rviz = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        output='screen',
    )

    # --- Create the Launch Description ---
    return LaunchDescription([
        DeclareLaunchArgument(
            'use_gui',
            default_value='true',
            description='Flag to enable joint_state_publisher_gui'),
        
        node_robot_state_publisher,
        node_joint_state_publisher_gui,
        node_rviz
    ])