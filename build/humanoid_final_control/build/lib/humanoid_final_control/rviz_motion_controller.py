import rclpy
from rclpy.node import Node
from std_msgs.msg import Bool
from sensor_msgs.msg import JointState
from math import sin, pi

class RvizMotionControllerNode(Node):
    """
    A node that listens for a trigger and animates the humanoid's neck in RViz.
    """
    def __init__(self):
        super().__init__('rviz_motion_controller_node')
        
        # Subscriber to the object detection trigger from our perception package
        self.trigger_subscription = self.create_subscription(
            Bool,
            '/humanoid/color_detection/object_close_trigger',
            self.trigger_callback,
            10)
            
        # Publisher for the joint states to animate the robot in RViz
        self.joint_state_publisher = self.create_publisher(
            JointState,
            'joint_states', # RViz listens to this topic
            10)
            
        self.get_logger().info('RViz Motion Controller has started.')
        
        # State variables for the animation
        self.animation_timer = None
        self.animation_start_time = None
        self.is_animating = False

    def trigger_callback(self, msg):
        """
        Callback function for the trigger.
        If trigger is True and we are not already animating, start the nod animation.
        """
        if msg.data and not self.is_animating:
            self.get_logger().info('Trigger received! Starting nod animation in RViz.')
            self.is_animating = True
            # Start the animation timer, calling the animation step function every 20ms
            self.animation_timer = self.create_timer(0.02, self.animation_step)
            self.animation_start_time = self.get_clock().now()

    def animation_step(self):
        """
        Calculates and publishes one frame of the nod animation.
        """
        # Calculate how long the animation has been running
        current_time = self.get_clock().now()
        elapsed_time = (current_time - self.animation_start_time).nanoseconds / 1e9
        
        # --- Calculate the "nod" motion ---
        # The animation will last 2 seconds.
        animation_duration = 2.0
        
        if elapsed_time < animation_duration:
            # Use a sine wave to create a smooth nod down and back up
            # It goes from 0 -> 0.5 -> 0 over the 2 seconds
            amplitude = 0.5 # Nod down by 0.5 radians
            position = amplitude * sin(pi * (elapsed_time / animation_duration))
        else:
            # Animation is over, clean up
            position = 0.0
            self.is_animating = False
            # --- THIS IS THE FIX ---
            self.animation_timer.cancel() 
            self.get_logger().info('Nod animation finished.')

        # Create and publish the JointState message
        joint_state_msg = JointState()
        joint_state_msg.header.stamp = current_time.to_msg()
        joint_state_msg.name = ['neck_joint']
        joint_state_msg.position = [position]
        self.joint_state_publisher.publish(joint_state_msg)


def main(args=None):
    rclpy.init(args=args)
    rviz_motion_controller_node = RvizMotionControllerNode()
    rclpy.spin(rviz_motion_controller_node)
    
    rviz_motion_controller_node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
