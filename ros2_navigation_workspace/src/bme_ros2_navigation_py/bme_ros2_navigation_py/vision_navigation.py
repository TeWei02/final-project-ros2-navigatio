import rclpy
from rclpy.node import Node
from rclpy.action import ActionClient
from geometry_msgs.msg import PoseStamped, Point, Twist
from nav2_msgs.action import NavigateToPose
import time
from std_msgs.msg import String, Float32MultiArray

# -- USER CONFIGURABLE TOPICS --
CMD_VEL_TOPIC = '/cmd_vel'
CLAW_CMD_TOPIC = '/claw_cmd'  # Placeholder for Claw Actuation
INTERACTION_TOPIC = '/interaction_cmd' # Placeholder for 'Unlock'/'Clear'

class VisionNavigation(Node):
    def __init__(self):
        super().__init__('vision_navigation')
        
        # Action Client for Nav2
        self.nav_to_pose_client = ActionClient(self, NavigateToPose, 'navigate_to_pose')
        
        # Publishers
        self.cmd_vel_pub = self.create_publisher(Twist, CMD_VEL_TOPIC, 10)
        self.claw_pub = self.create_publisher(String, CLAW_CMD_TOPIC, 10)
        self.interaction_pub = self.create_publisher(String, INTERACTION_TOPIC, 10)
        
        # Subscribers
        self.yolo_sub = self.create_subscription(Float32MultiArray, '/yolo/target_info', self.yolo_callback, 10)
        
        # State variables
        self.state = 'SEARCHING' # SEARCHING, SERVOING, OBSERVING, RECOVERING, FINISHED
        self.target_found = False
        self.target_dist = 0.0
        self.target_delta_x = 0.0
        
        # Waypoints for searching the map (Placeholder coordinates, assuming WFC randomization needs dynamic goals)
        self.search_waypoints = [
            self.create_pose(2.0, 2.0),
            self.create_pose(4.0, -2.0),
            self.create_pose(-2.0, 4.0),
        ]
        self.current_waypoint_idx = 0
        
        # Goal handle to allow cancellation
        self.current_goal_handle = None
        
        # Start immediately checking state
        self.timer = self.create_timer(0.5, self.state_machine_loop)
        
        self.get_logger().info("Final Project Controller Started. Waiting for Nav2 Action Server...")
        self.nav_to_pose_client.wait_for_server()
        self.get_logger().info("Nav2 Action Server connected. Starting mission.")
        
        self.send_next_waypoint()

    def create_pose(self, x, y):
        pose = PoseStamped()
        pose.header.frame_id = 'map'
        pose.pose.position.x = x
        pose.pose.position.y = y
        pose.pose.orientation.w = 1.0 # Facing forward
        return pose

    def yolo_callback(self, msg):
        # msg.data = [found, distance, delta_x]
        if len(msg.data) >= 3:
            self.target_found = bool(msg.data[0])
            self.target_dist = msg.data[1]
            self.target_delta_x = msg.data[2]

    def send_next_waypoint(self):
        if self.current_waypoint_idx >= len(self.search_waypoints):
            self.get_logger().info("All search waypoints visited. Restarting.")
            self.current_waypoint_idx = 0
            
        goal_pose = self.search_waypoints[self.current_waypoint_idx]
        self.send_nav_goal(goal_pose)
        self.current_waypoint_idx += 1

    def send_nav_goal(self, pose):
        goal_msg = NavigateToPose.Goal()
        goal_msg.pose = pose
        goal_msg.pose.header.stamp = self.get_clock().now().to_msg()
        
        self.get_logger().info(f"Sending goal to Nav2...")
        send_goal_future = self.nav_to_pose_client.send_goal_async(goal_msg)
        send_goal_future.add_done_callback(self.goal_response_callback)

    def goal_response_callback(self, future):
        goal_handle = future.result()
        if not goal_handle.accepted:
            self.get_logger().info('Goal rejected :(')
            return

        self.get_logger().info('Goal accepted :)')
        self.current_goal_handle = goal_handle
        self.get_result_future = goal_handle.get_result_async()
        self.get_result_future.add_done_callback(self.get_result_callback)

    def get_result_callback(self, future):
        result = future.result().result
        status = future.result().status
        if status == 4: # GoalStatus.STATUS_SUCCEEDED
            self.get_logger().info('Goal succeeded!')
            if self.state == 'SEARCHING':
                self.send_next_waypoint()
            elif self.state == 'RECOVERING':
                self.get_logger().info('Mission Complete! Releasing object...')
                claw_msg = String()
                claw_msg.data = "RELEASE"
                self.claw_pub.publish(claw_msg)
                self.state = 'FINISHED'
        else:
            self.get_logger().info(f'Goal failed with status: {status}')

    def cancel_navigation(self):
        if self.current_goal_handle is not None:
            self.get_logger().info('Canceling current navigation goal...')
            self.current_goal_handle.cancel_goal_async()
            self.current_goal_handle = None

    def state_machine_loop(self):
        if self.state == 'SEARCHING':
            if self.target_found:
                self.get_logger().info("Target Found! Switching to SERVOING.")
                self.state = 'SERVOING'
                self.cancel_navigation()
        
        elif self.state == 'SERVOING':
            twist = Twist()
            
            if not self.target_found:
                # Lost target, go back to searching
                self.get_logger().warn("Lost target. Returning to SEARCHING.")
                self.state = 'SEARCHING'
                self.send_next_waypoint()
                return

            # Proportional Control for steering
            # target_delta_x is range [-1, 1]
            twist.angular.z = -1.0 * self.target_delta_x 
            
            # Forward speed based on distance
            if self.target_dist > 0.8:
                twist.linear.x = 0.2
            else:
                twist.linear.x = 0.1
                
            # Stop condition (Canva: Close enough)
            if self.target_dist < 0.5: 
                twist.linear.x = 0.0
                twist.angular.z = 0.0
                self.cmd_vel_pub.publish(twist)
                
                self.get_logger().info("Reached Target! Observing for 5 seconds...")
                self.state = 'OBSERVING'
                self.observe_start_time = self.get_clock().now()
            else:
                self.cmd_vel_pub.publish(twist)
                
            # Reset detection to require constant confirmation
            self.target_found = False

        elif self.state == 'OBSERVING':
            current_time = self.get_clock().now()
            elapsed = (current_time - self.observe_start_time).nanoseconds / 1e9
            
            # Publish 'UNLOCK' during observation (Task 3 Requirement)
            if elapsed < 1.0:
                msg = String()
                msg.data = "UNLOCK"
                self.interaction_pub.publish(msg)

            if elapsed > 5.0:
                self.get_logger().info("Observation complete. Returning to origin...")
                self.state = 'RECOVERING'
                
                # Send Nav2 back to spawn (0,0)
                self.send_nav_goal(self.create_pose(0.0, 0.0))

        elif self.state == 'RECOVERING':
            # Logic handled in get_result_callback
            pass
        
        elif self.state == 'FINISHED':
            # Stop all motion
            twist = Twist()
            self.cmd_vel_pub.publish(twist)


def main(args=None):
    rclpy.init(args=args)
    controller_node = VisionNavigation()
    
    try:
         rclpy.spin(controller_node)
    except KeyboardInterrupt:
         pass
         
    controller_node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
