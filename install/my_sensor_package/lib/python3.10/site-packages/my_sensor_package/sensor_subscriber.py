import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32

class DistanceSubscriber(Node):

    def __init__(self):
        super().__init__("distance_subscriber")

        self.subscriptions_ = self.create_subscription(Float32, "distance_sensor", self.distance_callback, 10)

        self.get_logger().info("Distance sensor node has started")

    def distance_callback(self, msg: Float32):
        self.get_logger().info(f'Received Distance: "{msg.data:.2f} meters" ')

def main(args=None):
    rclpy.init(args=args)
    simple_distance_subscriber = DistanceSubscriber()
    rclpy.spin(simple_distance_subscriber)
    rclpy.shutdown()