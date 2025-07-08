#!/usr/bin/env python3

import rclpy
from rclpy.node import Node


class MyNode(Node):

    def __init__(self):
        super().__init__("first_node") #node name used
        #self.get_logger().info("Hello from ROS2")
        self.counter_ = 0
        self.create_timer(1.0, self.timer_callback) #create_timer is a built-in function

    def timer_callback(self):        #timer callback inside the node
        
        self.get_logger().info("Hello " + str(self.counter_))
        self.counter_ += 1

def main(args=None):  #this is useful to install the node with ros2 functionalities
    rclpy.init(args=args) #initialize ros2 communications
    node = MyNode()
    rclpy.spin(node) #keep running until ctrl c
    rclpy.shutdown()   

if __name__ == '__main__': #this is useful to directly execute the file from the terminal
    main()