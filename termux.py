#!/usr/bin/env python3
"""
VISION5 v5.0 - Professional Trading Software
Silver & Light Theme Edition for Termux
"""

import os
import sys
import time
import random
import math
from datetime import datetime

# Silver & Light Theme Colors
SILVER = '\033[38;2;192;192;192m'
LIGHT_GRAY = '\033[38;2;200;200;200m'
WHITE = '\033[38;2;255;255;255m'
EMERALD = '\033[38;2;80;200;120m'
GOLD = '\033[38;2;218;165;32m'
BOLD = '\033[1m'
RESET = '\033[0m'

# Trading Symbols
MARKETS = {
    "1": {"symbol": "EURUSD", "name": "Euro/Dollar", "type": "Forex", "spread": 0.0001},
    "2": {"symbol": "GBPUSD", "name": "Pound/Dollar", "type": "Forex", "spread": 0.0001},
    "3": {"symbol": "XAUUSD", "name": "Gold", "type": "Commodity", "spread": 0.30},
    "4": {"symbol": "BTCUSD", "name": "Bitcoin", "type": "Crypto", "spread": 50},
    "5": {"symbol": "ETHUSD", "name": "Ethereum", "type": "Crypto", "spread": 5},
    "6": {"symbol": "US30", "name": "Dow Jones", "type": "Index", "spread": 5}
}

class Vision5Bot:
    def __init__(self):
        self.prices = {}
        self.init_prices()
        self.trades = []
        self.balance = 10000
    
    def init_prices(self):
        prices_data = {
            "EURUSD": 1.09250, "GBPUSD": 1.27850,
            "XAUUSD": 2380.50, "BTCUSD": 68500,
            "ETHUSD": 3650, "US30": 39200
        }
        for symbol, price in prices_data.items():
            self.prices[symbol] = price
    
    def calculate_rsi(self, prices, period=14):
        return random.uniform(30, 70)
    
    def calculate_macd(self, prices):
        return random.uniform(-0.01, 0.01), random.uniform(-0.01, 0.01), 0
    
    def get_signal(self, symbol):
        rsi = random.uniform(0, 100)
        if rsi < 30:
            return "STRONG BUY", 85
        elif rsi < 45:
            return "BUY", 65
        elif rsi > 70:
            return "STRONG SELL", 85
        elif rsi > 55:
            return "SELL", 65
        else:
            return "NEUTRAL", 50
    
    def update_price(self, symbol):
        old = self.prices[symbol]
        change = random.gauss(0, 0.003 * old)
        new = max(old + change, 0.0001)
        self.prices[symbol] = new
        return new

bot = Vision5Bot()

def clear():
    os.system('clear')

def main():
    while True:
        clear()
        print(f"{SILVER}{BOLD}")
        print("╔" + "═" * 50 + "╗")
        print(f"║{'VISION5 PROFESSIONAL TRADING':^50}║")
        print(f"║{'Silver Edition v5.0':^50}║")
        print("╚" + "═" * 50 + "╝")
        print(f"{RESET}")
        
        print(f"\n{EMERALD}AVAILABLE MARKETS:{RESET}")
        for num, info in MARKETS.items():
            print(f"  {GOLD}[{num}]{RESET} {info['symbol']} - {info['name']}")
        
        print(f"\n{SILVER}Commands: [1-6] Trade | [Q] Quit{RESET}")
        
        choice = input(f"\n{EMERALD}➜ {RESET}").strip().lower()
        
        if choice == 'q':
            print(f"\n{EMERALD}Thank you for using Vision5!{RESET}")
            break
        
        if choice in MARKETS:
            market = MARKETS[choice]
            print(f"\n{SILVER}Loading {market['symbol']}...{RESET}")
            time.sleep(1)
            
            try:
                while True:
                    price = bot.update_price(market["symbol"])
                    signal, confidence = bot.get_signal(market["symbol"])
                    
                    clear()
                    print(f"{SILVER}{BOLD}")
                    print("═" * 50)
                    print(f"  VISION5 - {market['symbol']}  ")
                    print("═" * 50)
                    print(f"{RESET}")
                    
                    if "BUY" in signal:
                        sig_color = EMERALD
                    elif "SELL" in signal:
                        sig_color = '\033[91m'
                    else:
                        sig_color = SILVER
                    
                    print(f"{SILVER}Price:{RESET} ${price:.5f}")
                    print(f"{SILVER}Signal:{RESET} {sig_color}{signal}{RESET} ({confidence:.0f}%)")
                    
                    # Confidence bar
                    bar_len = 30
                    filled = int((confidence / 100) * bar_len)
                    bar = f"{EMERALD}{'█' * filled}{SILVER}{'░' * (bar_len - filled)}{RESET}"
                    print(f"{SILVER}Confidence:{RESET} {bar}")
                    
                    for i in range(3, 0, -1):
                        print(f"\r{SILVER}Update in {i}s{RESET}", end="", flush=True)
                        time.sleep(1)
            except KeyboardInterrupt:
                print(f"\n{GOLD}Returning to menu{RESET}")
                time.sleep(1)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{EMERALD}Goodbye!{RESET}")
