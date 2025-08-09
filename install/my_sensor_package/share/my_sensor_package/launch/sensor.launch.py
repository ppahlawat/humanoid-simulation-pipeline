import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    #package_dir = get_package_share_directory('my_sensor_package')

    return LaunchDescription([
       
        Node(
            package='my_sensor_package',
            executable='sensor_publisher_node', 
            name='distance_publisher_node', 
            
        ),

        Node(
            package='my_sensor_package',
            executable='sensor_subscriber_node', 
            name='distance_subscriber_node',
            
        )
    ])

