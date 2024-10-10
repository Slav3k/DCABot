import ccxt
import datetime
from datetime import datetime, timedelta, timezone
import schedule
import time
import json
import pytz
import os
from tzlocal import get_localzone
import sys
import syslog

class ConfigFileNotFoundError(Exception):
    pass

class DcaBot:
    def __init__(self, directory, config_file):
        # Initialize the class with the provided directory
        self.directory = directory
        self.config_file = config_file
        self.log_add_boot_entry()
        self.read_config()

        # wait x seconds before we start the bot
        time.sleep(self.initial_sleep_s)

        self.exch_handle = self.create_exchange(self.apiKey, self.apiSecret, self.exchange_name)
        self.verify_API_keys()
        self.open_orders = []

    def verify_API_keys(self):
        """
        Verifies API credentials by making an authenticated API call.
        """
        try:
            # Attempt to fetch account balance as a benign authenticated call
            balance = self.exch_handle.fetch_balance()
        except Exception as e:
            self.log_add_line(f"Error verifying echange API credentials. Check if your API keys are correct.")
            syslog.syslog(syslog.LOG_ERR, f"Error verifying echange API credentials. Check if your API keys are correct.")
            sys.exit(1)

    def log_add_boot_entry(self):
        ct = datetime.now()

        self.log_add_line("")
        self.log_add_line("**********************************")
        self.log_add_line(f"Boot time: {datetime.fromtimestamp(int(ct.timestamp()))}")
        self.log_add_line(f"PWD: {self.directory}")
        self.log_add_line(f"Config file: {self.config_file}")


    def log_add_line(self, log_msg, log_dir=""):
        try:
            if log_dir == "":
                log_dir = self.directory

            with open(os.path.join(log_dir, "log.txt"), "a") as f:
                print(log_msg, file=f)

        except (FileNotFoundError, OSError) as e:
            print(f"An error occurred while adding entry to log: {e}")

    def start(self):
        self.schedule_order()

        self.__start_print()

        # endless loop
        while True:
            schedule.run_pending()
            time.sleep(1)  # wait 1 sec

    def schedule_order(self):
        if self.side == "buy":
            if self.order_type == "below_above":
                raise NotImplementedError("Buy order 'below/above' is not implemented yet")
            else:
                schedule.every(int(self.periodHours * 60)).minutes.do(self.execute_buy_orders_market)
        elif self.side == "sell":
            if self.order_type == "below_above":
                raise NotImplementedError("Sell order 'below/above' is not implemented yet")
            else:
                schedule.every(int(self.periodHours * 60)).minutes.do(self.execute_sell_orders_market)
        else:
            raise ValueError("Invalid 'side' value")

    def __start_print(self):
        print("DCA bot active")
        print(f"Using exchange: {self.exchange_name}")
        print(f"Period: {self.periodHours} hrs")
        print(f"Order type: {self.order_type}")

    def buy_market(self, trading_pair, quote_qty):
        try:
            # Fetch the ticker price for the trading pair
            ticker = self.exch_handle.fetch_ticker(trading_pair)
            ask_price = ticker['ask']  # Use the ask price for market buy

            # Calculate the base_qty of the base asset to buy with the given quote_qty amount
            base_qty = quote_qty / ask_price

            # Create a market buy order
            order = self.exch_handle.create_market_buy_order(trading_pair, base_qty)

            order_id = order['id']
            symbol = order['symbol']

            # Loop until the order status is 'closed'
            while True:
                order_fetched = self.exch_handle.fetch_order(order_id, symbol=symbol)
                if order_fetched['status'] == 'closed':
                    break
                time.sleep(1) # seconds

            self.print_info_order(order_fetched, "closed")

        except ccxt.BaseError as e:
            print(f"An error occurred in buy_market: {e}")

    def sell_market(self, trading_pair, quote_qty):
        try:
            # Fetch the ticker price for the trading pair
            ticker = self.exch_handle.fetch_ticker(trading_pair)
            ask_price = ticker['ask']  # Use the ask price for market buy

            # Calculate the base_qty of the base asset to buy with the given quote_qty amount
            base_qty = quote_qty / ask_price

            # Create a market sell order
            order = self.exch_handle.create_market_sell_order(trading_pair, base_qty)

            order_id = order['id']
            symbol = order['symbol']

            # Loop until the order status is 'closed'
            while True:
                order_fetched = self.exch_handle.fetch_order(order_id, symbol=symbol)
                if order_fetched['status'] == 'closed':
                    break
                time.sleep(1) # seconds

            self.print_info_order(order_fetched, "closed")

        except ccxt.BaseError as e:
            print(f"An error occurred in sell_market: {e}")

    def print_info_order(self, order, status):
        datetime_str = order['datetime']  # Assuming format: 2023-10-10T22:50:02.802Z
        original_datetime = datetime.strptime(datetime_str, '%Y-%m-%dT%H:%M:%S.%fZ')
        # Convert the original datetime to Lisbon time
        local_datetime = original_datetime.astimezone(self.timezone)

        # Open the file for appending the order details
        with open(os.path.join(self.directory, "OrderLog.txt"), "a") as f:
            print("***********************", file=f)
            print(f"Order ID: {order['id']}", file=f)
            print(f"Order type: {order['type']} - {order['side']}", file=f)
            print(f"Time: {local_datetime.strftime('%Y-%m-%d %H:%M:%S')}", file=f)
            print(f"Trading Pair: {order['symbol']}", file=f)

            # Switch behavior based on the 'status' parameter
            if status == 'closed':
                print(f"Avg price: {order['average']}", file=f)
                print(f"Base quantity: {order['filled']}", file=f)
                print(f"Status: {order['status']}", file=f)
            elif status == 'canceled':
                print(f"Base quantity: {order['filled']}", file=f)
                print(f"Avg price: {order['average']}", file=f)
                print(f"Spent: {order['cost']}", file=f)
                print(f"Status: {order['status']}", file=f)
            elif status == 'placed':
                print("Limit order placed", file=f)
                print(f"Base quantity: {order['amount']}", file=f)
                print(f"Limit price: {order['price']}", file=f)

    def execute_buy_orders_market(self):
        with open(os.path.join(self.directory, self.config_file), "r") as read_json:
            config = json.load(read_json)
            pairs = config["pairs"]
            for pair in pairs:
                quote_qty = pairs[pair]
                self.buy_market(pair, quote_qty)

    def execute_sell_orders_market(self):
        with open(os.path.join(self.directory, self.config_file), "r") as read_json:
            config = json.load(read_json)
            pairs = config["pairs"]
            for pair in pairs:
                quote_qty = pairs[pair]
                self.sell_market(pair, quote_qty)

    def create_exchange(self, api_key, api_secret, exchange_name):
        if exchange_name == 'kraken':
            exch_handle = ccxt.kraken({
                'apiKey': api_key,
                'secret': api_secret,
            })
        elif exchange_name == 'binance':
            exch_handle = ccxt.binance({
                'apiKey': api_key,
                'secret': api_secret,
            })
        else:
            raise ValueError("Unsupported exch_handle name. Supported exchanges: 'kraken', 'binance'")

        return exch_handle

    def get_automatic_timezone(self):
        """
        Detects the system's local timezone automatically.

        Returns:
            str: The name of the local timezone (e.g., 'Europe/Lisbon').
        """
        try:
            local_timezone = get_localzone()

            # For pytz objects, use the 'zone' attribute.
            if hasattr(local_timezone, 'zone'):
                timezone_name = local_timezone.zone
            else:
                # For ZoneInfo objects, convert to string.
                timezone_name = str(local_timezone)

            return timezone_name

        except Exception as e:
            print(f"Error detecting local timezone: {e}")
            # Fallback to 'UTC' if detection fails
            return pytz.utc

    def read_config(self):
        try:
            # Parse the config file
            with open(os.path.join(self.directory, self.config_file), "r") as read_json:
                config = json.load(read_json)

                # Read all the values from the json
                self.initial_sleep_s = config.get("initial_sleep_s", 0)
                time_zone_option = config.get("timezone", "auto-detect")
                if(time_zone_option == "auto-detect"):
                    #call autodetect timezone based on machine
                    self.timezone = pytz.timezone(self.get_automatic_timezone())
                    self.log_add_line(f"Autodetected timezone from device: {self.timezone}")
                else:
                    # use the string directly
                    # 'Europe/Lisbon', 'Europe/Prague', 'Europe/Rome',...
                    self.timezone = pytz.timezone(time_zone_option)
                    self.log_add_line(f"Timezone from config: {self.timezone}")

                self.exchange_name = config.get("exchange_name", "binance").lower()
                self.periodHours = config.get("period_hours", 12.0)
                self.apiKey = config.get("api_key")
                self.apiSecret = config.get("api_secret")
                self.order_type = config.get("order_type", "market").lower()
                self.side = config.get("side", "buy").lower()
                self.maxTimeOpen = config.get("max_time_open", 2)


                config_str = "\n".join([f"Exchange Name: {self.exchange_name}",
                                        f"Period Hours: {self.periodHours}",
                                        f"Order Type: {self.order_type}",
                                        f"Side: {self.side}",])

                self.log_add_line(config_str)

        except FileNotFoundError:
            error_msg = "Config file not found. Using default values."
            directory_msg = f"Logging / config directory: {self.directory}"
            config_file_msg = f"Config File: {self.config_file}"
            together_msg = f"Together: {os.path.join(self.directory, self.config_file)}"

            log_message = "\n".join([error_msg, directory_msg, config_file_msg, together_msg])
            print(log_message)
            self.log_add_line(log_message)
            raise ConfigFileNotFoundError("Config file not found. Exiting program.") from None


