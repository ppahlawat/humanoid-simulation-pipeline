import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from geometry_msgs.msg import Point
from std_msgs.msg import Bool
from cv_bridge import CvBridge
import cv2
import numpy as np

class ColorDetectorNode(Node):
    """
    A ROS 2 node that detects all red, green, or blue objects, publishes their
    positions, and sends a trigger if any object is close.
    """
    def __init__(self):
        super().__init__('color_detector_node')
        
        self.AREA_THRESHOLD = 15000
        self.bridge = CvBridge()

        self.color_ranges = {
            'red': ([0, 120, 70], [10, 255, 255], [170, 120, 70], [180, 255, 255]),
            'green': ([35, 100, 50], [85, 255, 255]),
            'blue': ([100, 150, 50], [140, 255, 255])
        }

        self.image_subscription = self.create_subscription(
            Image, '/humanoid/camera_sensor/image_raw', self.image_callback, 10)
        
        self.processed_image_publisher = self.create_publisher(
            Image, '/humanoid/color_detection/processed_image', 10)
            
        self.position_publisher = self.create_publisher(
            Point, '/humanoid/color_detection/object_position', 10)
            
        self.trigger_publisher = self.create_publisher(
            Bool, '/humanoid/color_detection/object_close_trigger', 10)
            
        self.get_logger().info('Color Detector Node has started and detects R/G/B.')

    def image_callback(self, msg):
        try:
            cv_image = self.bridge.imgmsg_to_cv2(msg, 'bgr8')
        except Exception as e:
            self.get_logger().error(f'Failed to convert image: {e}')
            return

        hsv_image = cv2.cvtColor(cv_image, cv2.COLOR_BGR2HSV)
        
        # --- MODIFIED: Trigger will be true if ANY object is close ---
        any_object_is_close = False

        # Loop through all defined colors
        for color_name, ranges in self.color_ranges.items():
            if color_name == 'red':
                mask1 = cv2.inRange(hsv_image, np.array(ranges[0]), np.array(ranges[1]))
                mask2 = cv2.inRange(hsv_image, np.array(ranges[2]), np.array(ranges[3]))
                mask = mask1 + mask2
            else:
                mask = cv2.inRange(hsv_image, np.array(ranges[0]), np.array(ranges[1]))

            contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

            # --- MODIFIED: Draw a box around every contour found for each color ---
            if contours:
                for contour in contours:
                    # Optional: filter out very small contours to reduce noise
                    area = cv2.contourArea(contour)
                    if area < 100:
                        continue

                    x, y, w, h = cv2.boundingRect(contour)
                    
                    # Check if this specific object is close
                    if area > self.AREA_THRESHOLD:
                        any_object_is_close = True
                        cv2.rectangle(cv_image, (x, y), (x + w, y + h), (0, 255, 255), 3) # Yellow box
                        cv2.putText(cv_image, f'{color_name.upper()} CLOSE!', (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 255), 2)
                    else:
                        cv2.rectangle(cv_image, (x, y), (x + w, y + h), (0, 255, 0), 2) # Green box
                        cv2.putText(cv_image, f'{color_name.capitalize()} Object', (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
                    
                    # Publish position of every detected object
                    position_msg = Point(x=float(x + w // 2), y=float(y + h // 2), z=0.0)
                    self.position_publisher.publish(position_msg)
        
        # Publish the overall trigger message
        trigger_msg = Bool(data=any_object_is_close)
        self.trigger_publisher.publish(trigger_msg)

        try:
            processed_msg = self.bridge.cv2_to_imgmsg(cv_image, 'bgr8')
            self.processed_image_publisher.publish(processed_msg)
        except Exception as e:
            self.get_logger().error(f'Failed to publish processed image: {e}')


def main(args=None):
    rclpy.init(args=args)
    color_detector_node = ColorDetectorNode()
    rclpy.spin(color_detector_node)
    
    color_detector_node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
