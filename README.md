# DCABot
Dca bot written in python that is relying on CCXT. Note that currently one instance of bot can only do sell or buy and only on with one period. If you need both buy and sell and various periods, you will have to create multiple instances of the bot to achieve that. In future releases I plan to enable buy and sell and multiple periods from one instance of the bot.

## DCA Bot Configuration
Below is a sample configuration for the DCA bot. Please edit the values in the config.json file according to your needs.
```
{
  "exchange_name": "Binance",
  "api_key": "",
  "api_secret": "",
  "period_hours": 12,
  "side": "buy",
  "order_type": "market",
  "below_above_prc": 0.1,
  "max_time_open": 6,
  "initial_sleep_s": 1,
  "timezone": "auto-detect",
  "pairs": {
    "BTC/EUR": 11,
    "ETH/EUR": 25,
    "SOL/EUR": 25,
    "POLYX/USDT": 30
  }
}
```

### Configuration Options
**exchange_name:** The exchange platform to use. Supported options: 'Binance' or 'Kraken'.  
**api_key:** Your API key for accessing the exchange.  
**api_secret:** Your API secret for accessing the exchange.  
**period_hours:** The time interval in hours between each DCA execution.  
side: The order side. Options: 'buy' or 'sell'.  
**order_type:** The type of order to place. Options include 'market' or 'below_above' (essentially limit).  
**below_above_prc:** The percentage threshold for placing 'below_above' orders relative to the current price. For example, 0.1 equals 10%.  
**max_time_open:** Maximum duration in hours to keep the 'below_above' order open.  
**initial_sleep_s:** Initial delay in seconds before the first execution of the bot.  
**timezone:** Timezone setting. Use 'auto-detect' for the system's local timezone or specify a timezone (e.g., 'Europe/London').  
**pairs:** A dictionary of cryptocurrency pairs to trade and their respective amounts. For example, "BTC/EUR": 11 means to buy 11 EUR worth of Bitcoin.  


## How to install dependencies
To deploy, you can first install deps using "InstallDeps.sh" or "InstallDeps.bat".

## How to configure the service
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

## Useful commands
### General Service Management
#### List All Services currently registered with systemd
systemctl list-units --type=service
#### Filter registered Services by Name 
systemctl list-units --type=service | grep -i DCA

### Specific Service Operations
#### View Service Logs Displays the last 100 log entries for the 'dcabot.service' without using a pager
sudo journalctl -u dcabot.service -n 100 --no-pager
#### Stop a Service 
sudo systemctl stop dcabot1.service
#### Restart a Service 
sudo systemctl restart dcabot.service
#### Enable a Service
sudo systemctl enable dcabot1.service
#### Disable a Service 
sudo systemctl disable dcabot1.service
#### Displays the last 100 log entries for the 'dcabot.service' without using a pager
sudo journalctl -u dcabot.service -n 100 --no-pager
#### Restarts the 'dcabot.service', useful after making configuration changes
sudo systemctl restart dcabot.service
#### Disables 'dcabot1.service' from starting automatically at boot
sudo systemctl disable dcabot1.service
#### Checks if 'dcabot1.service' is set to start automatically on boot
systemctl is-enabled dcabot1.service
#### Lists all services whose names contain 'DCA'
systemctl list-units --type=service | grep -i DCA