import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32
import random

class DistancePublisher(Node):

    def __init__(self):
        super().__init__('distance_publisher')
        self.publisher_ = self.create_publisher(Float32, 'distance_sensor', 10)

        self.timer_period = 3000
        self.timer = self.create_timer(self.timer_period, self.publish_distance)

        self.count = 0
        self.get_logger().info("Distance sensor node has started")

    def publish_distance(self):

        distance = random.uniform(1,10)
        msg = Float32()
        msg.data = distance
        #self.get_logger().info(f'Publishing Distance: "{msg.data:.2f} meters" (Count: {self.count})')
        self.count += 1
        self.publisher_.publish(msg)

def main(args=None):
    rclpy.init(args=args)
    simple_distance_publisher = DistancePublisher()
    rclpy.spin(simple_distance_publisher)
    rclpy.shutdown()