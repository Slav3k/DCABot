# DCABot
Dca bot written in python that is relying on CCXT

# How to install dependencies
To deploy, you can first install deps using "InstallDeps.sh" or "InstallDeps.bat".

# How to configure the service
sudo nano /etc/systemd/system/DcaBot.service

Contents of the DcaBot.service:

[Unit]
Description=Dollar-Cost Averaging (DCA) Bot
After=network.target

[Service]
ExecStart=/home/slavek/git/DcaBot/start.sh
WorkingDirectory=/home/slavek/git/DcaBot
User=slavek
Restart=always

[Install]
WantedBy=multi-user.target

After that execute:
sudo systemctl enable dcabot.service
sudo systemctl start dcabot.service
sudo systemctl daemon-reload

# Useful commands
# General Service Management
# List All Services currently registered with systemd
systemctl list-units --type=service
# Filter registered Services by Name 
systemctl list-units --type=service | grep -i DCA

# Specific Service Operations
# View Service Logs Displays the last 100 log entries for the 'dcabot.service' without using a pager
sudo journalctl -u dcabot.service -n 100 --no-pager
# Stop a Service 
sudo systemctl stop dcabot1.service
# Restart a Service 
sudo systemctl restart dcabot.service

# Service Enablement/Disablement
# Enable a Service
sudo systemctl enable dcabot1.service
# Disable a Service 
sudo systemctl disable dcabot1.service
# Check Service Enablement Checks if 'dcabot1.service' is set to start automatically on boot
systemctl is-enabled dcabot1.service





# Lists all services currently registered with systemd
systemctl list-units --type=service

# Displays the last 100 log entries for the 'dcabot.service' without using a pager
sudo journalctl -u dcabot.service -n 100 --no-pager

# Restarts the 'dcabot.service', useful after making configuration changes
sudo systemctl restart dcabot.service

# Disables 'dcabot1.service' from starting automatically at boot
sudo systemctl disable dcabot1.service

# Checks if 'dcabot1.service' is set to start automatically on boot
systemctl is-enabled dcabot1.service

# Stops the 'dcabot1.service', halting its current operations
sudo systemctl stop dcabot1.service

# Filters and lists all services whose names contain 'DCA', regardless of case
systemctl list-units --type=service | grep -i DCA