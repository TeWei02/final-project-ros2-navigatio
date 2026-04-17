FROM osrf/ros:jazzy-desktop-full

ENV DEBIAN_FRONTEND=noninteractive
ENV ROS_DISTRO=jazzy

# Install additional system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    gnupg2 \
    lsb-release \
    sudo \
    software-properties-common \
    wget \
    git \
    vim \
    python3-pip \
    python3-colcon-common-extensions \
    xvfb \
    x11vnc \
    screen \
    ffmpeg \
    libssl-dev \
    libudev-dev \
    pkg-config \
    ros-jazzy-slam-toolbox \
    ros-jazzy-nav2-bringup \
    ros-jazzy-nav2-amcl \
    ros-jazzy-interactive-marker-twist-server \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies for YOLO
RUN pip3 install --no-cache-dir --break-system-packages ultralytics opencv-python-headless


# Source ROS2 in bashrc
RUN echo "source /opt/ros/jazzy/setup.bash" >> ~/.bashrc

# Create workspace directories
RUN mkdir -p /ros2_ws/src
RUN mkdir -p /data/{images,train,valid}

WORKDIR /ros2_ws

# Create entrypoint script
RUN cat > /entrypoint.sh << 'EOS'
#!/bin/bash
source /opt/ros/jazzy/setup.bash
if [ -f "/ros2_ws/install/setup.bash" ]; then
    source /ros2_ws/install/setup.bash
fi

# Start VNC server for remote GUI
if [ "${VNC_ENABLED}" = "true" ]; then
    echo "Starting VNC server..."
    x11vnc -display :0 -forever -shared &
fi

exec "$@"
EOS

RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
CMD ["/bin/bash"]