import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState
from math import sin, pi

class CubeAnimatorNode(Node):
    """
    A node that publishes JointState messages to animate the cube in RViz.
    """
    def __init__(self):
        super().__init__('cube_animator_node')
        
        # Publisher for the joint states
        self.joint_state_publisher = self.create_publisher(
            JointState,
            'joint_states', # This is the standard topic for joint states
            10)
            
        # Create a timer to publish the joint state at 50Hz (20ms period)
        self.timer = self.create_timer(0.02, self.publish_joint_state)
        self.get_logger().info('Cube Animator Node has started.')
        self.start_time = self.get_clock().now()

    def publish_joint_state(self):
        """
        Calculates and publishes the current state of the slider_joint.
        """
        # Calculate elapsed time
        current_time = self.get_clock().now()
        elapsed_time = (current_time - self.start_time).nanoseconds / 1e9

        # --- Calculate the back-and-forth motion using a sine wave ---
        # Amplitude of 3.0 meters, period of 4 seconds
        amplitude = 3.0
        frequency = 0.25  # Corresponds to a 4-second period (1/4)
        position = amplitude * sin(2 * pi * frequency * elapsed_time)
        
        # Create a JointState message
        joint_state_msg = JointState()
        joint_state_msg.header.stamp = current_time.to_msg()
        joint_state_msg.name = ['slider_joint']
        joint_state_msg.position = [position]
        
        # Publish the message
        self.joint_state_publisher.publish(joint_state_msg)


def main(args=None):
    rclpy.init(args=args)
    cube_animator_node = CubeAnimatorNode()
    rclpy.spin(cube_animator_node)
    
    cube_animator_node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
