FROM ros:noetic

ENV DEBIAN_FRONTEND=noninteractive

# Update
RUN apt-get update && apt-get install -y \
    git \
    python3-catkin-tools \
    ros-noetic-gazebo-ros \
    ros-noetic-gazebo-ros-pkgs \
    ros-noetic-turtlebot3 \
    ros-noetic-turtlebot3-simulations \
    && rm -rf /var/lib/apt/lists/*

# Create workspace
RUN mkdir -p /root/catkin_ws/src
WORKDIR /root/catkin_ws/src

# Clone tortoisebot simulation
RUN git clone https://github.com/Angelo9AC/checkpoint23.git

# Copy your package (will mount later)
WORKDIR /root/catkin_ws

# Build workspace
RUN /bin/bash -c "source /opt/ros/noetic/setup.bash && catkin_make"

CMD ["bash"]
