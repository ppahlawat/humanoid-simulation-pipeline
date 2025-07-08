#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from turtlesim.msg import Pose
class PoseSubscriberNode(Node):

    def __init__(self):
        super().__init__("pose_subscriber") #node name used
        self.pose_subscriber_ = self.create_subscription(Pose, "/turtle1/pose", self.pose_callback, 10) #that 10 is kind of a buffer
        self.get_logger().info("Pose subscriber node has been started")

    def pose_callback(self, msg: Pose): #callback is set so i can receive what i need to
        self.get_logger().info( "(" + str(msg.x) + ", " + str(msg.y) + ")" )

def main(args=None):  #this is useful to install the node with ros2 functionalities
    rclpy.init(args=args) #initialize ros2 communications
    node = PoseSubscriberNode()
    rclpy.spin(node)
    rclpy.shutdown()   

