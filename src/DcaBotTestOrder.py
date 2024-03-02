from CcxtWrap import DcaBot
import os
import argparse

def get_script_folder():
    script_folder = os.path.dirname(os.path.realpath(__file__))
    return script_folder + os.sep

def parse_input_arg_config():
    # Create an ArgumentParser object
    parser = argparse.ArgumentParser(description='DCA Bot Script')

    # Add a command-line argument for the configuration file name
    parser.add_argument('config_file', type=str, help='Name of the configuration file (e.g., "config_binance.json")')

    # Parse the command-line arguments
    args = parser.parse_args()

    return args.config_file

def main():
    # Get current working directory
    script_pth = get_script_folder()

    # Create an instance of the DcaBot class
    dca_bot = DcaBot(script_pth, "config_binance_test.json")

    # Start the DCA bot
    dca_bot.execute_buy_orders_market()

if __name__ == "__main__":
    main()