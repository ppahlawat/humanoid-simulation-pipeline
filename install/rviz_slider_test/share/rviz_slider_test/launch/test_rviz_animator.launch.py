import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node
from launch.substitutions import Command

def generate_launch_description():

    # --- Paths ---
    pkg_rviz_slider_test = get_package_share_directory('rviz_slider_test')

    # --- Robot Description (URDF) ---
    xacro_file = os.path.join(pkg_rviz_slider_test, 'urdf', 'animated_cube.urdf.xacro')
    robot_description_config = Command(['xacro ', xacro_file])
    robot_description = {'robot_description': robot_description_config}

    # --- Nodes to Launch ---

    # 1. Robot State Publisher
    # This node reads the URDF and publishes the robot's structure and TF frames.
    node_robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        output='screen',
        parameters=[robot_description]
    )

    # 2. Cube Animator Node
    # This is our custom node that publishes the joint states to animate the cube.
    node_cube_animator = Node(
        package='rviz_slider_test',
        executable='cube_animator',
        name='cube_animator_node'
    )

    # 3. RViz2 Node
    # This starts the RViz visualization tool.
    node_rviz = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        output='screen'
    )

    return LaunchDescription([
        node_robot_state_publisher,
        node_cube_animator,
        node_rviz
    ])
