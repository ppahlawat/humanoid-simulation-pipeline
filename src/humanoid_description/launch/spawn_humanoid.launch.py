import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node
import xacro

def generate_launch_description():

    # Get path to the Gazebo ROS package
    pkg_gazebo_ros = get_package_share_directory('gazebo_ros')
    
    # Get path to your package
    pkg_humanoid_description = get_package_share_directory('humanoid_description')

    # Process the Xacro file
    xacro_file = os.path.join(pkg_humanoid_description, 'urdf', 'humanoid.urdf.xacro')
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

    # 2. Gazebo Server
    # This starts the physics simulation
    start_gazebo_server_cmd = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_gazebo_ros, 'launch', 'gzserver.launch.py')
        )
    )

    # 3. Gazebo Client
    # This starts the graphical user interface
    start_gazebo_client_cmd = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_gazebo_ros, 'launch', 'gzclient.launch.py')
        )
    )

    # 4. Spawn Entity
    # This node spawns your robot model in the Gazebo simulation
    spawn_entity_cmd = Node(
        package='gazebo_ros',
        executable='spawn_entity.py',
        arguments=['-topic', 'robot_description', '-entity', 'humanoid_robot'],
        output='screen'
    )

    return LaunchDescription([
        start_gazebo_server_cmd,
        start_gazebo_client_cmd,
        node_robot_state_publisher,
        spawn_entity_cmd,
    ])