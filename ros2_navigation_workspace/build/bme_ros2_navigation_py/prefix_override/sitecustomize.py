import sys
if sys.prefix == '/opt/homebrew/opt/python@3.14/Frameworks/Python.framework/Versions/3.14':
    sys.real_prefix = sys.prefix
    sys.prefix = sys.exec_prefix = '/Users/kedewei/Desktop/final project/FinalProject_Submission/ros2_navigation_workspace/install/bme_ros2_navigation_py'
