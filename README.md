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
systemctl list-units --type=service
- list all services

sudo journalctl -u dcabot.service -n 100 --no-pager
- displays journal of the service

sudo systemctl restart dcabot.service
- to restart service after changing period in the config