FROM osrf/ros:noetic-desktop-full

ENV DEBIAN_FRONTEND=noninteractive

# =========================
# Dependencias base + herramientas ROS
# =========================
RUN apt-get update && apt-get install -y \
    python3-catkin-tools \
    python3-rosdep \
    python3-osrf-pycommon \
    python3-rospkg \
    build-essential \
    git \
    x11-apps \
    && rm -rf /var/lib/apt/lists/*

# =========================
# Inicializar rosdep
# =========================
RUN rosdep init || true
RUN rosdep update

# =========================
# Crear workspace
# =========================
RUN mkdir -p /root/catkin_ws/src
WORKDIR /root/catkin_ws

# =========================
# Copiar paquetes (SOLO docker_src)
# =========================
COPY ./docker_src /root/catkin_ws/src

# =========================
# Instalar dependencias automáticamente
# =========================
RUN /bin/bash -c "source /opt/ros/noetic/setup.bash && \
    rosdep install --from-paths src --ignore-src -r -y"

# =========================
# Compilar workspace
# =========================
RUN /bin/bash -c "source /opt/ros/noetic/setup.bash && \
    catkin_make"

# =========================
# Configurar entorno automático
# =========================
RUN echo 'source /opt/ros/noetic/setup.bash' >> ~/.bashrc && \
    echo 'source /root/catkin_ws/devel/setup.bash' >> ~/.bashrc

# =========================
# Variables para evitar errores de Gazebo en CI
# =========================
ENV QT_X11_NO_MITSHM=1
ENV DISPLAY=:99

WORKDIR /root/catkin_ws

# =========================
# Comando por defecto
# =========================
CMD ["/bin/bash"]