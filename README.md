# DCABot
Dca bot written in python that is relying on CCXT. Note that currently one instance of bot can only do sell or buy and only with one period. If you need both buy and sell and various periods, you will have to create multiple instances of the bot to achieve that. In future releases I plan to enable buy and sell and multiple periods from one instance of the bot.

⚠️ **WARNING**  
This DCA Crypto Bot is provided "as is" without any warranties of any kind, express or implied. By using this bot, you acknowledge that it is entirely at your own risk.

The author of this bot assumes no responsibility for any financial losses, damages, or other consequences that may arise from the use of this bot. Cryptocurrency trading is highly volatile and involves significant risk. Users are strongly advised to conduct their own research, understand the risks involved, and use this bot only if they are comfortable with potential losses.

By using this bot, you agree to the following:

You understand and accept that the author of this bot is not liable for any trading losses, technical failures, or other damages that may result from its use.  
You assume full responsibility for any actions or trades executed by this bot and acknowledge that the author cannot be held responsible for any negative outcomes.  
You will not hold the author liable for any errors, bugs, or unexpected behavior of the bot.  

⚠️ **WARNING**  
The bot currently supports only market buy / sell. The limit (aka below_above) is still under development.

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
#### Start a Service 
sudo systemctl start dcabot.service
#### Stop a Service 
sudo systemctl stop dcabot.service
#### Restart a service
sudo systemctl restart dcabot.service
- useful after making configuration changes
#### Enable a Service
sudo systemctl enable dcabot.service
- starts automatically at boot
#### Disable a Service 
sudo systemctl disable dcabot.service
- prevents from starting automatically at boot
#### Check if enabled
systemctl is-enabled dcabot.service
#### View Service Logs 
sudo journalctl -u dcabot.service -n 100 --no-pager
- Displays the last 100 log entries for the 'dcabot.service'
#### List all services whose names contain 'DCA'
systemctl list-units --type=service | grep -i DCA

