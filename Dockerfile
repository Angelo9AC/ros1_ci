FROM osrf/ros:noetic-desktop-full

ENV DEBIAN_FRONTEND=noninteractive

# =========================
# Instalar dependencias básicas
# =========================
RUN apt-get update && apt-get install -y \
    python3-catkin-tools \
    python3-osrf-pycommon \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# =========================
# Crear workspace
# =========================
RUN mkdir -p /root/catkin_ws/src
WORKDIR /root/catkin_ws

# =========================
# Copiar TODOS los paquetes
# (tortoisebot + checkpoint23)
# =========================
COPY ./src /root/catkin_ws/src

# =========================
# Build normal (catkin_make)
# =========================
RUN /bin/bash -c "source /opt/ros/noetic/setup.bash && catkin_make"

# =========================
# Source automático
# =========================
RUN echo "source /opt/ros/noetic/setup.bash" >> ~/.bashrc && \
    echo "source /root/catkin_ws/devel/setup.bash" >> ~/.bashrc

WORKDIR /root/catkin_ws

# =========================
# Entrypoint para abrir bash listo para ROS + GUI
# =========================
CMD ["/bin/bash"]