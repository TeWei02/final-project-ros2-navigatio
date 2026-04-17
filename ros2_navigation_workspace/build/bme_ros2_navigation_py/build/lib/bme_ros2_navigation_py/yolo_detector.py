import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from std_msgs.msg import Float32MultiArray
from cv_bridge import CvBridge
import cv2
import numpy as np
import os

try:
    from ultralytics import YOLO
except ImportError:
    YOLO = None
    print("Warning: ultralytics package not found. YOLO inference will not run.")

class YoloDetector(Node):
    def __init__(self):
        super().__init__('yolo_detector')
        
        # Subscribing to the Unity camera
        self.subscription = self.create_subscription(
            Image,
            '/camera/image',
            self.image_callback,
            10
        )
        self.subscription  # prevent unused variable warning
        
        # Publisher for the target info [found, distance, delta_x]
        self.detection_pub = self.create_publisher(Float32MultiArray, '/yolo/target_info', 10)
        
        self.bridge = CvBridge()
        
        # Load the models
        from ament_index_python.packages import get_package_share_directory
        try:
            package_share_directory = get_package_share_directory('bme_ros2_navigation')
            model_path = os.path.join(package_share_directory, 'models', 'detection.pt')
        except Exception:
            # Fallback path for development if not installed
            model_path = '/ros2_ws/src/bme_ros2_navigation/models/detection.pt'
        
        self.model = None
        if YOLO is not None and os.path.exists(model_path):
            self.get_logger().info(f"Loading YOLO model from {model_path}")
            self.model = YOLO(model_path)
        else:
            self.get_logger().warn(f"YOLO model not found at {model_path} or ultralytics not installed.")
            
    def image_callback(self, msg):
        if self.model is None:
            return
            
        try:
            cv_image = self.bridge.imgmsg_to_cv2(msg, "bgr8")
        except Exception as e:
            self.get_logger().error(f"Failed to convert image: {e}")
            return
            
        # Run inference
        results = self.model(cv_image, verbose=False)
        
        # Extract the highest confidence detection (or process all)
        # Assuming we just need to guide the robot to the closest/most confident target
        best_det = None
        highest_conf = 0.0
        
        for r in results:
            boxes = r.boxes
            for box in boxes:
                conf = float(box.conf[0])
                if conf > highest_conf:
                    highest_conf = conf
                    best_det = box

        # Initialize message with [found=0, dist=0, delta_x=0]
        msg_data = [0.0, 0.0, 0.0]

        if best_det is not None and highest_conf > 0.5:
            # c = [x_center, y_center, width, height] in pixel coordinates
            c = best_det.xywh[0]
            
            # 1. Found flag
            msg_data[0] = 1.0
            
            # 2. Distance estimation (Heuristic based on bbox height)
            # Assuming known_height (bear) ~ 1.0m, focal_length_px ~ 500 (standard for 640x480 cam)
            bbox_h = float(c[3])
            if bbox_h > 0:
                msg_data[1] = (1.0 * 500.0) / bbox_h
            
            # 3. Delta X (Normalized offset from center, range -1.0 to 1.0)
            # Unity image width is typically 640
            img_width = cv_image.shape[1]
            center_x = float(c[0])
            msg_data[2] = (center_x - (img_width / 2.0)) / (img_width / 2.0)

        # Publish the target info
        info_msg = Float32MultiArray()
        info_msg.data = msg_data
        self.detection_pub.publish(info_msg)

def main(args=None):
    rclpy.init(args=args)
    yolo_node = YoloDetector()
    
    try:
        rclpy.spin(yolo_node)
    except KeyboardInterrupt:
        pass
        
    yolo_node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
