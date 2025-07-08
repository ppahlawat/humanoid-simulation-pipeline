from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    ld = LaunchDescription()

    sensor_transmitter_node = Node(
        package="my_sensor_package",
        executable="sensor_publisher_node",
    )

    sensor_receiver_node = Node(
        package="my_sensor_packae",
        executable="sensor_subscriber_node"
    )

    ld.add_action(sensor_transmitter_node)
    ld.add_action(sensor_receiver_node)

    return ld