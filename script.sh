#!/bin/bash

# Update and install VNC server (RealVNC)
echo "Installing RealVNC server..."
sudo apt update && sudo apt install -y realvnc-vnc-server realvnc-vnc-viewer

# Enable VNC via Raspberry Pi Configuration (if not already done)
echo "Enabling VNC server..."
sudo systemctl enable vncserver-x11-serviced.service

# Create a new systemd service file for VNC server
echo "Creating systemd service for VNC..."
cat <<EOF | sudo tee /etc/systemd/system/vncserver.service > /dev/null
[Unit]
Description=Start VNC Server at boot
After=graphical.target

[Service]
Type=forking
User=pi
ExecStart=/usr/bin/vncserver :0
ExecStop=/usr/bin/vncserver -kill :0
Restart=always

[Install]
WantedBy=multi-user.target
EOF

# Reload systemd to apply the new service
echo "Reloading systemd manager..."
sudo systemctl daemon-reload

# Enable the VNC service to start at boot
echo "Enabling VNC server to start on boot..."
sudo systemctl enable vncserver.service

# Start the VNC service immediately (optional)
echo "Starting VNC server now..."
sudo systemctl start vncserver.service

# Verify the VNC service status
echo "Verifying VNC service status..."
sudo systemctl status vncserver.service

# Prompt for setting VNC password (if not already set)
echo "Please set the VNC password (if not done yet)..."
vncpasswd

echo "VNC server is now configured to start automatically on boot."
echo "You can connect to your Raspberry Pi using a VNC client at <Raspberry Pi IP>:0."
