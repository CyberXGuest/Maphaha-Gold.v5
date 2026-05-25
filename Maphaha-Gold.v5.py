#!/usr/bin/env python3
"""
╔═══════════════════════════════════════════════════════════════════════════════╗
║                         VISION5 PROFESSIONAL TRADING                          ║
║                         Premium Trading Software v5.0                         ║
║                         Silver Edition | Light Theme                          ║
╚═══════════════════════════════════════════════════════════════════════════════╝

Vision5 - Advanced Trading Platform
Features: Real-time signals | Multi-asset trading | AI-powered analytics
"""

import os
import sys
import time
import json
import signal
import sqlite3
import random
import math
import threading
from datetime import datetime, timedelta
from collections import deque
from dataclasses import dataclass, field
from typing import Dict, List, Tuple, Optional, Any
from enum import Enum
import argparse

# ============================================
# PREMIUM SILVER & LIGHT COLOR SCHEME
# ============================================

class Vision5Theme:
    """Professional silver and light theme for Vision5"""
    
    # Silver & Light Color Palette
    SILVER_LIGHT = '\033[38;2;192;192;192m'
    SILVER_METALLIC = '\033[38;2;165;165;165m'
    SILVER_DARK = '\033[38;2;128;128;128m'
    PLATINUM = '\033[38;2;229;228;226m'
    WHITE_PEARL = '\033[38;2;248;248;255m'
    LIGHT_GRAY = '\033[38;2;200;200;200m'
    DARK_GRAY = '\033[38;2;100;100;100m'
    
    # Accent Colors (Muted for professional look)
    ACCENT_GREEN = '\033[38;2;0;150;100m'
    ACCENT_RED = '\033[38;2;200;60;60m'
    ACCENT_BLUE = '\033[38;2;50;120;200m'
    ACCENT_GOLD = '\033[38;2;200;150;50m'
    ACCENT_PURPLE = '\033[38;2;120;80;180m'
    
    # Background Colors (Light theme)
    BG_MAIN = '\033[48;2;245;245;250m'
    BG_PANEL = '\033[48;2;255;255;255m'
    BG_HEADER = '\033[48;2;220;220;230m'
    BG_BUY = '\033[48;2;0;150;100m'
    BG_SELL = '\033[48;2;200;60;60m'
    
    # UI Elements
    BORDER = '\033[38;2;180;180;190m'
    TEXT_PRIMARY = '\033[38;2;40;40;50m'
    TEXT_SECONDARY = '\033[38;2;100;100;110m'
    TEXT_MUTED = '\033[38;2;150;150;160m'
    
    # Effects
    BOLD = '\033[1m'
    DIM = '\033[2m'
    RESET = '\033[0m'
    
    # Box Drawing Characters
    BOX_TL = "╔"
    BOX_TR = "╗"
    BOX_BL = "╚"
    BOX_BR = "╝"
    BOX_H = "═"
    BOX_V = "║"
    BOX_T = "╠"
    BOX_BT = "╣"
    BOX_CROSS = "╬"

# ============================================
# CONFIGURATION
# ============================================

VERSION = "5.0.0"
BUILD = "Professional Silver Edition"
COMPANY = "Vision5 Trading Systems"

class Config:
    """Vision5 Configuration"""
    # Trading Settings
    INITIAL_CAPITAL = 25000.0
    BASE_LOT_SIZE = 0.50
    MAX_POSITIONS = 10
    RISK_PER_TRADE = 0.015
    
    # Strategy Parameters
    SIGNAL_THRESHOLD = 65
    STOP_LOSS_PTS = 800
    TAKE_PROFIT_PTS = 1600
    
    # System Settings
    UPDATE_INTERVAL = 2
    HISTORY_BARS = 1000
    ENABLE_SOUND = False
    ENABLE_ANIMATIONS = True
    
    # Paths
    DB_PATH = os.path.expanduser("~/vision5_trading.db")
    LOG_PATH = os.path.expanduser("~/vision5_logs")

# ============================================
# ENUMS & DATA CLASSES
# ============================================

class SignalStrength(Enum):
    EXTREME = "EXTREME"
    STRONG = "STRONG"
    MODERATE = "MODERATE"
    WEAK = "WEAK"
    NEUTRAL = "NEUTRAL"

class TradeType(Enum):
    LONG = "LONG"
    SHORT = "SHORT"

class OrderType(Enum):
    MARKET = "MARKET"
    LIMIT = "LIMIT"
    STOP = "STOP"

@dataclass
class Position:
    """Trading position"""
    id: int
    symbol: str
    type: TradeType
    entry_price: float
    volume: float
    stop_loss: float
    take_profit: float
    open_time: datetime
    close_price: Optional[float] = None
    close_time: Optional[datetime] = None
    profit: float = 0.0
    status: str = "OPEN"

@dataclass
class MarketData:
    """Market data tick"""
    symbol: str
    bid: float
    ask: float
    timestamp: datetime
    volume: int = 0

@dataclass
class Signal:
    """Trading signal"""
    symbol: str
    type: TradeType
    strength: SignalStrength
    confidence: float
    price: float
    timestamp: datetime
    indicators: Dict[str, Any]
    reasoning: str

# ============================================
# ADVANCED INDICATORS ENGINE
# ============================================

class IndicatorsEngine:
    """Professional technical indicators suite"""
    
    @staticmethod
    def ema(prices: List[float], period: int) -> float:
        if len(prices) < period:
            return prices[-1] if prices else 0
        multiplier = 2 / (period + 1)
        ema = sum(prices[:period]) / period
        for price in prices[period:]:
            ema = (price - ema) * multiplier + ema
        return ema
    
    @staticmethod
    def rsi(prices: List[float], period: int = 14) -> float:
        if len(prices) < period + 1:
            return 50
        
        gains = losses = 0
        for i in range(-period, 0):
            diff = prices[i] - prices[i-1]
            if diff > 0:
                gains += diff
            else:
                losses += abs(diff)
        
        if losses == 0:
            return 100
        if gains == 0:
            return 0
        
        rs = gains / losses
        return 100 - (100 / (1 + rs))
    
    @staticmethod
    def macd(prices: List[float]) -> Tuple[float, float, float]:
        if len(prices) < 26:
            return 0, 0, 0
        
        ema12 = IndicatorsEngine.ema(prices, 12)
        ema26 = IndicatorsEngine.ema(prices, 26)
        macd = ema12 - ema26
        signal = macd * 0.85
        histogram = macd - signal
        return macd, signal, histogram
    
    @staticmethod
    def bollinger(prices: List[float], period: int = 20) -> Tuple[float, float, float]:
        if len(prices) < period:
            return 0, 0, 0
        
        recent = prices[-period:]
        sma = sum(recent) / period
        variance = sum((p - sma) ** 2 for p in recent) / period
        std = math.sqrt(variance)
        
        return sma + (2 * std), sma, sma - (2 * std)
    
    @staticmethod
    def atr(highs: List[float], lows: List[float], period: int = 14) -> float:
        if len(highs) < period + 1:
            return 0
        
        tr_values = []
        for i in range(-period, 0):
            tr = max(highs[i] - lows[i], 
                    abs(highs[i] - lows[i-1]),
                    abs(lows[i] - highs[i-1]))
            tr_values.append(tr)
        
        return sum(tr_values) / period
    
    @staticmethod
    def stochastic(prices: List[float], highs: List[float], lows: List[float]) -> float:
        if len(prices) < 14:
            return 50
        
        period_high = max(highs[-14:])
        period_low = min(lows[-14:])
        
        if period_high == period_low:
            return 50
        
        return ((prices[-1] - period_low) / (period_high - period_low)) * 100

# ============================================
# VISION5 AI SIGNAL GENERATOR
# ============================================

class Vision5AI:
    """Advanced signal generation engine"""
    
    def __init__(self, symbol: str):
        self.symbol = symbol
        self.prices = deque(maxlen=Config.HISTORY_BARS)
        self.highs = deque(maxlen=Config.HISTORY_BARS)
        self.lows = deque(maxlen=Config.HISTORY_BARS)
        self.volumes = deque(maxlen=Config.HISTORY_BARS)
        
        # Indicator history
        self.rsi_history = deque(maxlen=50)
        self.macd_history = deque(maxlen=50)
        
        # Learning data
        self.signal_history = []
        self.accuracy_tracker = {}
        
    def add_price(self, price: float, high: float = None, low: float = None, volume: int = 0):
        self.prices.append(price)
        self.highs.append(high or price)
        self.lows.append(low or price)
        self.volumes.append(volume)
    
    def analyze(self) -> Signal:
        """Comprehensive market analysis"""
        if len(self.prices) < 50:
            return Signal(self.symbol, TradeType.LONG, SignalStrength.NEUTRAL, 
                         0, self.prices[-1] if self.prices else 0, 
                         datetime.now(), {}, "Analyzing...")
        
        # Calculate all indicators
        rsi = IndicatorsEngine.rsi(list(self.prices))
        macd, macd_signal, macd_hist = IndicatorsEngine.macd(list(self.prices))
        upper_bb, mid_bb, lower_bb = IndicatorsEngine.bollinger(list(self.prices))
        stoch = IndicatorsEngine.stochastic(list(self.prices), list(self.highs), list(self.lows))
        atr = IndicatorsEngine.atr(list(self.highs), list(self.lows))
        
        # Trend analysis
        ema20 = IndicatorsEngine.ema(list(self.prices), 20)
        ema50 = IndicatorsEngine.ema(list(self.prices), 50)
        
        current_price = self.prices[-1]
        
        # Scoring system (0-100)
        buy_score = 0
        sell_score = 0
        reasons = []
        
        # RSI Analysis (25 points)
        if rsi < 30:
            buy_score += 25
            reasons.append(f"RSI Oversold ({rsi:.1f})")
        elif rsi > 70:
            sell_score += 25
            reasons.append(f"RSI Overbought ({rsi:.1f})")
        elif rsi < 40:
            buy_score += 12
            reasons.append(f"RSI Approaching Oversold ({rsi:.1f})")
        elif rsi > 60:
            sell_score += 12
            reasons.append(f"RSI Approaching Overbought ({rsi:.1f})")
        
        # MACD Analysis (25 points)
        if macd > macd_signal and macd_hist > 0:
            buy_score += 25
            reasons.append("MACD Bullish Crossover")
        elif macd < macd_signal and macd_hist < 0:
            sell_score += 25
            reasons.append("MACD Bearish Crossover")
        elif macd > macd_signal:
            buy_score += 12
            reasons.append("MACD Positive Momentum")
        elif macd < macd_signal:
            sell_score += 12
            reasons.append("MACD Negative Momentum")
        
        # Bollinger Bands (20 points)
        if current_price <= lower_bb:
            buy_score += 20
            reasons.append("Price at Lower BB")
        elif current_price >= upper_bb:
            sell_score += 20
            reasons.append("Price at Upper BB")
        elif current_price < mid_bb:
            buy_score += 10
            reasons.append("Price Below Mid BB")
        elif current_price > mid_bb:
            sell_score += 10
            reasons.append("Price Above Mid BB")
        
        # Moving Averages (15 points)
        if ema20 > ema50 and current_price > ema20:
            buy_score += 15
            reasons.append("Golden Cross Pattern")
        elif ema20 < ema50 and current_price < ema20:
            sell_score += 15
            reasons.append("Death Cross Pattern")
        elif current_price > ema20:
            buy_score += 7
            reasons.append("Price Above EMA20")
        elif current_price < ema20:
            sell_score += 7
            reasons.append("Price Below EMA20")
        
        # Stochastic (15 points)
        if stoch < 20:
            buy_score += 15
            reasons.append(f"Stochastic Oversold ({stoch:.1f})")
        elif stoch > 80:
            sell_score += 15
            reasons.append(f"Stochastic Overbought ({stoch:.1f})")
        elif stoch < 40:
            buy_score += 7
        elif stoch > 60:
            sell_score += 7
        
        # Volume confirmation (bonus)
        if len(self.volumes) > 1:
            volume_change = (self.volumes[-1] - self.volumes[-2]) / self.volumes[-2] if self.volumes[-2] > 0 else 0
            if volume_change > 0.2 and buy_score > sell_score:
                buy_score += 10
                reasons.append("Volume Confirmation")
            elif volume_change > 0.2 and sell_score > buy_score:
                sell_score += 10
                reasons.append("Volume Confirmation")
        
        # Determine signal
        net_score = buy_score - sell_score
        total_score = max(buy_score, sell_score)
        
        if net_score > 30:
            signal_type = TradeType.LONG
            confidence = min(99, net_score + 20)
            if net_score > 60:
                strength = SignalStrength.EXTREME
            elif net_score > 45:
                strength = SignalStrength.STRONG
            else:
                strength = SignalStrength.MODERATE
        elif net_score < -30:
            signal_type = TradeType.SHORT
            confidence = min(99, abs(net_score) + 20)
            if abs(net_score) > 60:
                strength = SignalStrength.EXTREME
            elif abs(net_score) > 45:
                strength = SignalStrength.STRONG
            else:
                strength = SignalStrength.MODERATE
        else:
            signal_type = TradeType.LONG
            strength = SignalStrength.NEUTRAL
            confidence = 0
        
        # Apply threshold
        if total_score < Config.SIGNAL_THRESHOLD:
            strength = SignalStrength.NEUTRAL
            confidence = 0
        
        return Signal(
            symbol=self.symbol,
            type=signal_type,
            strength=strength,
            confidence=confidence,
            price=current_price,
            timestamp=datetime.now(),
            indicators={
                'RSI': round(rsi, 2),
                'MACD': round(macd, 5),
                'MACD_Signal': round(macd_signal, 5),
                'BB_Upper': round(upper_bb, 5),
                'BB_Middle': round(mid_bb, 5),
                'BB_Lower': round(lower_bb, 5),
                'Stochastic': round(stoch, 2),
                'ATR': round(atr, 5),
                'EMA20': round(ema20, 5),
                'EMA50': round(ema50, 5),
                'Buy_Score': buy_score,
                'Sell_Score': sell_score
            },
            reasoning=" | ".join(reasons[:3]) if reasons else "No clear signals"
        )

# ============================================
# TRADING ENGINE
# ============================================

class TradingEngine:
    """Core trading execution engine"""
    
    def __init__(self):
        self.positions: List[Position] = []
        self.closed_positions: List[Position] = []
        self.position_counter = 0
        self.capital = Config.INITIAL_CAPITAL
        self.initial_capital = Config.INITIAL_CAPITAL
        
    def execute_signal(self, signal: Signal) -> Optional[Position]:
        """Execute trading signal"""
        if signal.strength == SignalStrength.NEUTRAL:
            return None
        
        # Check existing positions
        same_direction = any(p.type == signal.type and p.status == "OPEN" 
                           for p in self.positions)
        if same_direction:
            return None
        
        # Calculate position size based on confidence
        volume = Config.BASE_LOT_SIZE * (signal.confidence / 100)
        volume = max(min(volume, Config.BASE_LOT_SIZE * 2), Config.BASE_LOT_SIZE * 0.3)
        
        # Calculate stop loss and take profit
        atr = signal.indicators.get('ATR', 0.001)
        stop_distance = Config.STOP_LOSS_PTS * 0.0001
        take_distance = Config.TAKE_PROFIT_PTS * 0.0001
        
        if signal.type == TradeType.LONG:
            stop_loss = signal.price - (stop_distance + atr)
            take_profit = signal.price + (take_distance + (atr * 1.5))
        else:
            stop_loss = signal.price + (stop_distance + atr)
            take_profit = signal.price - (take_distance + (atr * 1.5))
        
        self.position_counter += 1
        position = Position(
            id=self.position_counter,
            symbol=signal.symbol,
            type=signal.type,
            entry_price=signal.price,
            volume=volume,
            stop_loss=stop_loss,
            take_profit=take_profit,
            open_time=datetime.now()
        )
        
        self.positions.append(position)
        return position
    
    def update_positions(self, current_price: float) -> List[Position]:
        """Update and check positions"""
        closed = []
        
        for pos in self.positions[:]:
            if pos.type == TradeType.LONG:
                if current_price <= pos.stop_loss:
                    self.close_position(pos, current_price, "Stop Loss")
                    closed.append(pos)
                elif current_price >= pos.take_profit:
                    self.close_position(pos, current_price, "Take Profit")
                    closed.append(pos)
            else:
                if current_price >= pos.stop_loss:
                    self.close_position(pos, current_price, "Stop Loss")
                    closed.append(pos)
                elif current_price <= pos.take_profit:
                    self.close_position(pos, current_price, "Take Profit")
                    closed.append(pos)
        
        return closed
    
    def close_position(self, position: Position, price: float, reason: str):
        """Close a position"""
        if position.type == TradeType.LONG:
            profit = (price - position.entry_price) * position.volume
        else:
            profit = (position.entry_price - price) * position.volume
        
        position.close_price = price
        position.close_time = datetime.now()
        position.profit = profit
        position.status = "CLOSED"
        
        self.capital += profit
        self.closed_positions.append(position)
        self.positions.remove(position)
    
    def get_stats(self) -> Dict:
        """Get trading statistics"""
        total_trades = len(self.closed_positions)
        winning = sum(1 for p in self.closed_positions if p.profit > 0)
        total_profit = sum(p.profit for p in self.closed_positions)
        
        return {
            'total_trades': total_trades,
            'winning_trades': winning,
            'win_rate': (winning / total_trades * 100) if total_trades > 0 else 0,
            'total_profit': total_profit,
            'current_capital': self.capital,
            'return_pct': ((self.capital - self.initial_capital) / self.initial_capital) * 100,
            'open_positions': len(self.positions),
            'avg_profit': total_profit / total_trades if total_trades > 0 else 0
        }

# ============================================
# MARKET SIMULATOR
# ============================================

class MarketSimulator:
    """Realistic market data generator"""
    
    def __init__(self):
        self.symbols = {}
        self._init_symbols()
    
    def _init_symbols(self):
        symbols_config = {
            "EURUSD": {"price": 1.09250, "volatility": 0.008, "trend": 0.0001},
            "GBPUSD": {"price": 1.27850, "volatility": 0.010, "trend": 0.00015},
            "USDJPY": {"price": 149.850, "volatility": 0.007, "trend": -0.0002},
            "XAUUSD": {"price": 2380.50, "volatility": 0.015, "trend": 0.002},
            "BTCUSD": {"price": 68500, "volatility": 0.040, "trend": 0.003},
            "ETHUSD": {"price": 3650, "volatility": 0.045, "trend": 0.002},
            "US30": {"price": 39200, "volatility": 0.012, "trend": 0.001},
            "US500": {"price": 5250, "volatility": 0.013, "trend": 0.0015},
            "GER30": {"price": 18500, "volatility": 0.011, "trend": 0.001},
            "UK100": {"price": 8200, "volatility": 0.009, "trend": 0.0008}
        }
        
        for symbol, config in symbols_config.items():
            self.symbols[symbol] = {
                'price': config['price'],
                'volatility': config['volatility'],
                'trend': config['trend'],
                'history': deque(maxlen=Config.HISTORY_BARS),
                'highs': deque(maxlen=Config.HISTORY_BARS),
                'lows': deque(maxlen=Config.HISTORY_BARS)
            }
            
            for _ in range(Config.HISTORY_BARS):
                self.symbols[symbol]['history'].append(config['price'])
                self.symbols[symbol]['highs'].append(config['price'] * 1.001)
                self.symbols[symbol]['lows'].append(config['price'] * 0.999)
    
    def get_price(self, symbol: str) -> float:
        return self.symbols[symbol]['price']
    
    def get_high_low(self, symbol: str) -> Tuple[float, float]:
        data = self.symbols[symbol]
        return data['highs'][-1], data['lows'][-1]
    
    def update_price(self, symbol: str) -> float:
        data = self.symbols[symbol]
        old = data['price']
        
        trend = data['trend'] * old * 0.1
        noise = random.gauss(0, data['volatility'] * old * 0.3)
        momentum = 0
        
        if len(data['history']) > 20:
            recent_momentum = (data['history'][-1] - data['history'][-20]) / 20
            momentum = recent_momentum * 0.2
        
        change = trend + noise + momentum
        
        if random.random() < 0.02:
            change *= random.uniform(1.5, 2.5)
        
        new_price = max(old + change, 0.0001)
        data['price'] = new_price
        data['history'].append(new_price)
        
        # Generate high/low
        range_val = new_price * data['volatility'] * 0.5
        data['highs'].append(new_price + abs(random.gauss(0, range_val)))
        data['lows'].append(new_price - abs(random.gauss(0, range_val)))
        
        return new_price

# ============================================
# PROFESSIONAL UI RENDERER
# ============================================

class Vision5UI:
    """Professional silver/light theme UI renderer"""
    
    def __init__(self):
        self.theme = Vision5Theme()
        self.current_view = "trading"
        
    def clear(self):
        os.system('clear')
    
    def draw_box(self, title: str, width: int = 70, color: str = None):
        """Draw a professional box"""
        if color is None:
            color = self.theme.BORDER
        
        print(f"{color}{self.theme.BOX_TL}{self.theme.BOX_H * (width-2)}{self.theme.BOX_TR}{self.theme.RESET}")
        if title:
            padding = (width - len(title) - 4) // 2
            print(f"{color}{self.theme.BOX_V}{' ' * padding}{self.theme.TEXT_PRIMARY}{self.theme.BOLD}{title}{self.theme.RESET}{color}{' ' * (width - len(title) - 4 - padding)}{self.theme.BOX_V}{self.theme.RESET}")
            print(f"{color}{self.theme.BOX_T}{self.theme.BOX_H * (width-2)}{self.theme.BOX_BT}{self.theme.RESET}")
    
    def draw_progress_bar(self, percentage: float, width: int = 30, color: str = None):
        """Draw a professional progress bar"""
        if color is None:
            if percentage >= 70:
                color = self.theme.ACCENT_GREEN
            elif percentage >= 40:
                color = self.theme.ACCENT_GOLD
            else:
                color = self.theme.ACCENT_RED
        
        filled = int((percentage / 100) * width)
        bar = f"{color}{'█' * filled}{self.theme.SILVER_LIGHT}{'░' * (width - filled)}{self.theme.RESET}"
        return bar
    
    def render_logo(self):
        """Render Vision5 logo"""
        print(f"{self.theme.SILVER_METALLIC}{self.theme.BOLD}")
        print("╔═══════════════════════════════════════════════════════════════════════════════╗")
        print("║                                                                               ║")
        print("║     ██╗   ██╗██╗███████╗██╗ ██████╗ ███╗   ██╗    ██████╗                     ║")
        print("║     ██║   ██║██║██╔════╝██║██╔═══██╗████╗  ██║    ╚════██╗                    ║")
        print("║     ██║   ██║██║███████╗██║██║   ██║██╔██╗ ██║     █████╔╝                    ║")
        print("║     ╚██╗ ██╔╝██║╚════██║██║██║   ██║██║╚██╗██║    ██╔═══╝                     ║")
        print("║      ╚████╔╝ ██║███████║██║╚██████╔╝██║ ╚████║    ███████╗                    ║")
        print("║       ╚═══╝  ╚═╝╚══════╝╚═╝ ╚═════╝ ╚═╝  ╚═══╝    ╚══════╝                    ║")
        print("║                                                                               ║")
        print(f"║{self.theme.PLATINUM}{'VISION5 PROFESSIONAL TRADING PLATFORM':^71}{self.theme.SILVER_METALLIC}║")
        print(f"║{self.theme.TEXT_SECONDARY}{f'Version {VERSION} | {BUILD}':^71}{self.theme.SILVER_METALLIC}║")
        print("╚═══════════════════════════════════════════════════════════════════════════════╝")
        print(f"{self.theme.RESET}")
    
    def render_trading_dashboard(self, symbol: str, price: float, signal: Signal,
                                 engine: TradingEngine, ai: Vision5AI):
        """Render main trading dashboard"""
        self.clear()
        
        # Header with logo
        print(f"{self.theme.BG_HEADER}{self.theme.TEXT_PRIMARY}")
        print("═" * 80)
        print(f"{'VISION5 • LIVE TRADING DASHBOARD':^80}")
        print(f"{f'{symbol} | ' + datetime.now().strftime('%Y-%m-%d %H:%M:%S'):^80}")
        print("═" * 80)
        print(f"{self.theme.RESET}")
        
        # Price Panel
        print(f"\n{self.theme.BG_PANEL}{self.theme.BORDER}")
        print(f"{self.theme.BOX_V} CURRENT MARKET PRICE{' ' * 57}{self.theme.BOX_V}")
        print(f"{self.theme.BOX_V}{self.theme.RESET}")
        
        price_color = self.theme.ACCENT_GREEN if signal.type == TradeType.LONG else self.theme.ACCENT_RED if signal.type == TradeType.SHORT else self.theme.TEXT_PRIMARY
        print(f"{self.theme.BOX_V}   {self.theme.TEXT_SECONDARY}Symbol:{self.theme.RESET} {self.theme.TEXT_PRIMARY}{self.theme.BOLD}{symbol}{self.theme.RESET} "
              f"{self.theme.TEXT_SECONDARY}Bid:{self.theme.RESET} {price_color}{self.theme.BOLD}${price:.5f}{self.theme.RESET} "
              f"{self.theme.TEXT_SECONDARY}Ask:{self.theme.RESET} ${price + 0.0001:.5f} "
              f"{self.theme.TEXT_SECONDARY}Spread:{self.theme.RESET} 0.0001{self.theme.BORDER}{self.theme.BOX_V}")
        
        # Signal Panel
        print(f"{self.theme.BG_PANEL}{self.theme.BORDER}")
        print(f"{self.theme.BOX_V} SIGNAL ANALYSIS{' ' * 59}{self.theme.BOX_V}")
        print(f"{self.theme.BOX_V}{self.theme.RESET}")
        
        # Signal display with styling
        if signal.strength == SignalStrength.EXTREME:
            signal_icon = "🔴" if signal.type == TradeType.SHORT else "🟢"
            signal_text = f"{signal_icon} {signal.type.value} SIGNAL"
            signal_color = self.theme.ACCENT_RED if signal.type == TradeType.SHORT else self.theme.ACCENT_GREEN
        elif signal.strength == SignalStrength.STRONG:
            signal_icon = "🔴" if signal.type == TradeType.SHORT else "🟢"
            signal_text = f"{signal_icon} {signal.type.value}"
            signal_color = self.theme.ACCENT_RED if signal.type == TradeType.SHORT else self.theme.ACCENT_GREEN
        elif signal.strength == SignalStrength.MODERATE:
            signal_icon = "🟡"
            signal_text = f"{signal_icon} {signal.type.value} (Moderate)"
            signal_color = self.theme.ACCENT_GOLD
        else:
            signal_icon = "⚪"
            signal_text = "NEUTRAL"
            signal_color = self.theme.TEXT_MUTED
        
        print(f"{self.theme.BOX_V}   {self.theme.TEXT_SECONDARY}Signal:{self.theme.RESET} {signal_color}{self.theme.BOLD}{signal_text:^20}{self.theme.RESET} "
              f"{self.theme.TEXT_SECONDARY}Strength:{self.theme.RESET} {signal.strength.value} "
              f"{self.theme.TEXT_SECONDARY}Confidence:{self.theme.RESET} {signal.confidence:.0f}%{self.theme.BORDER}{self.theme.BOX_V}")
        
        # Confidence bar
        if signal.confidence > 0:
            bar = self.draw_progress_bar(signal.confidence, 40)
            print(f"{self.theme.BOX_V}   {self.theme.TEXT_SECONDARY}Confidence:{self.theme.RESET} {bar} {signal.confidence:.0f}%{self.theme.BORDER}{self.theme.BOX_V}")
        
        # Reasoning
        if signal.reasoning:
            print(f"{self.theme.BOX_V}   {self.theme.TEXT_SECONDARY}Analysis:{self.theme.RESET} {signal.reasoning[:55]}{self.theme.BORDER}{self.theme.BOX_V}")
        
        # Indicators Panel
        print(f"{self.theme.BG_PANEL}{self.theme.BORDER}")
        print(f"{self.theme.BOX_V} TECHNICAL INDICATORS{' ' * 55}{self.theme.BOX_V}")
        print(f"{self.theme.BOX_V}{self.theme.RESET}")
        
        ind = signal.indicators
        print(f"{self.theme.BOX_V}   {self.theme.TEXT_SECONDARY}RSI:{self.theme.RESET} {ind.get('RSI', 50):>6.1f}  "
              f"{self.theme.TEXT_SECONDARY}MACD:{self.theme.RESET} {ind.get('MACD', 0):>8.5f}  "
              f"{self.theme.TEXT_SECONDARY}Stoch:{self.theme.RESET} {ind.get('Stochastic', 50):>6.1f}{self.theme.BORDER}{self.theme.BOX_V}")
        
        print(f"{self.theme.BOX_V}   {self.theme.TEXT_SECONDARY}BB Upper:{self.theme.RESET} {ind.get('BB_Upper', 0):>8.5f}  "
              f"{self.theme.TEXT_SECONDARY}Middle:{self.theme.RESET} {ind.get('BB_Middle', 0):>8.5f}  "
              f"{self.theme.TEXT_SECONDARY}Lower:{self.theme.RESET} {ind.get('BB_Lower', 0):>8.5f}{self.theme.BORDER}{self.theme.BOX_V}")
        
        print(f"{self.theme.BOX_V}   {self.theme.TEXT_SECONDARY}EMA20:{self.theme.RESET} {ind.get('EMA20', 0):>8.5f}  "
              f"{self.theme.TEXT_SECONDARY}EMA50:{self.theme.RESET} {ind.get('EMA50', 0):>8.5f}  "
              f"{self.theme.TEXT_SECONDARY}ATR:{self.theme.RESET} {ind.get('ATR', 0):>8.5f}{self.theme.BORDER}{self.theme.BOX_V}")
        
        # Score bars
        buy_score = ind.get('Buy_Score', 0)
        sell_score = ind.get('Sell_Score', 0)
        
        print(f"{self.theme.BOX_V}   {self.theme.ACCENT_GREEN}Bullish Score: {self.draw_progress_bar(buy_score, 25, self.theme.ACCENT_GREEN)} {buy_score}{self.theme.RESET}{self.theme.BORDER}{self.theme.BOX_V}")
        print(f"{self.theme.BOX_V}   {self.theme.ACCENT_RED}Bearish Score: {self.draw_progress_bar(sell_score, 25, self.theme.ACCENT_RED)} {sell_score}{self.theme.RESET}{self.theme.BORDER}{self.theme.BOX_V}")
        
        # Performance Panel
        stats = engine.get_stats()
        print(f"{self.theme.BG_PANEL}{self.theme.BORDER}")
        print(f"{self.theme.BOX_V} PERFORMANCE METRICS{' ' * 56}{self.theme.BOX_V}")
        print(f"{self.theme.BOX_V}{self.theme.RESET}")
        
        win_color = self.theme.ACCENT_GREEN if stats['win_rate'] >= 50 else self.theme.ACCENT_RED
        profit_color = self.theme.ACCENT_GREEN if stats['total_profit'] >= 0 else self.theme.ACCENT_RED
        return_color = self.theme.ACCENT_GREEN if stats['return_pct'] >= 0 else self.theme.ACCENT_RED
        
        print(f"{self.theme.BOX_V}   {self.theme.TEXT_SECONDARY}Trades:{self.theme.RESET} {stats['total_trades']:>4}  "
              f"{self.theme.TEXT_SECONDARY}Win Rate:{self.theme.RESET} {win_color}{stats['win_rate']:>5.1f}%{self.theme.RESET}  "
              f"{self.theme.TEXT_SECONDARY}Profit:{self.theme.RESET} {profit_color}${stats['total_profit']:>9.2f}{self.theme.RESET}{self.theme.BORDER}{self.theme.BOX_V}")
        
        print(f"{self.theme.BOX_V}   {self.theme.TEXT_SECONDARY}Capital:{self.theme.RESET} ${stats['current_capital']:>9.2f}  "
              f"{self.theme.TEXT_SECONDARY}Return:{self.theme.RESET} {return_color}{stats['return_pct']:>+6.1f}%{self.theme.RESET}  "
              f"{self.theme.TEXT_SECONDARY}Open Pos:{self.theme.RESET} {stats['open_positions']}{self.theme.BORDER}{self.theme.BOX_V}")
        
        # Open Positions Panel
        if engine.positions:
            print(f"{self.theme.BG_PANEL}{self.theme.BORDER}")
            print(f"{self.theme.BOX_V} OPEN POSITIONS{' ' * 59}{self.theme.BOX_V}")
            print(f"{self.theme.BOX_V}{self.theme.RESET}")
            
            for pos in engine.positions[:3]:  # Show max 3
                if pos.type == TradeType.LONG:
                    pos_color = self.theme.ACCENT_GREEN
                    unrealized = (price - pos.entry_price) * pos.volume
                else:
                    pos_color = self.theme.ACCENT_RED
                    unrealized = (pos.entry_price - price) * pos.volume
                
                unreal_color = self.theme.ACCENT_GREEN if unrealized >= 0 else self.theme.ACCENT_RED
                
                print(f"{self.theme.BOX_V}   {pos_color}{pos.type.value}{self.theme.RESET} "
                      f"Entry: ${pos.entry_price:.5f}  "
                      f"SL: ${pos.stop_loss:.5f}  "
                      f"TP: ${pos.take_profit:.5f}  "
                      f"P&L: {unreal_color}${unrealized:+.2f}{self.theme.RESET}{self.theme.BORDER}{self.theme.BOX_V}")
        
        # Bottom status bar
        print(f"{self.theme.BG_HEADER}{self.theme.TEXT_SECONDARY}")
        print("═" * 80)
        print(f"{'[Ctrl+C] Menu  |  [Q] Quit  |  [S] Statistics  |  [H] Help':^80}")
        print("═" * 80)
        print(f"{self.theme.RESET}")
    
    def render_menu(self):
        """Render main menu"""
        self.clear()
        self.render_logo()
        
        print(f"\n{self.theme.BG_PANEL}{self.theme.BORDER}")
        print(f"{self.theme.BOX_V}{' '*78}{self.theme.BOX_V}")
        print(f"{self.theme.BOX_V}{self.theme.TEXT_PRIMARY}{self.theme.BOLD}{'TRADING SYMBOLS':^78}{self.theme.RESET}{self.theme.BORDER}{self.theme.BOX_V}")
        print(f"{self.theme.BOX_V}{' '*78}{self.theme.BOX_V}")
        
        symbols = [
            ("1", "EURUSD", "Euro/US Dollar", "🔵"),
            ("2", "GBPUSD", "British Pound", "🔵"),
            ("3", "USDJPY", "USD/Japanese Yen", "🔵"),
            ("4", "XAUUSD", "Gold", "🟡"),
            ("5", "BTCUSD", "Bitcoin", "🟠"),
            ("6", "ETHUSD", "Ethereum", "🔷"),
            ("7", "US30", "Dow Jones", "📈"),
            ("8", "US500", "S&P 500", "📊"),
            ("9", "GER30", "German DAX", "🇩🇪"),
            ("10", "UK100", "UK FTSE", "🇬🇧"),
        ]
        
        # Display in 2 columns
        for i in range(0, len(symbols), 2):
            row1 = symbols[i]
            row2 = symbols[i+1] if i+1 < len(symbols) else None
            
            line = f"{self.theme.BOX_V}   "
            line += f"{self.theme.ACCENT_GOLD}{row1[3]}{self.theme.RESET} "
            line += f"{self.theme.ACCENT_GREEN}{row1[0]:>2}{self.theme.RESET}. "
            line += f"{self.theme.TEXT_PRIMARY}{row1[1]:<8}{self.theme.RESET} "
            line += f"{self.theme.TEXT_SECONDARY}{row1[2]:<20}{self.theme.RESET}"
            
            if row2:
                line += f"   {self.theme.ACCENT_GOLD}{row2[3]}{self.theme.RESET} "
                line += f"{self.theme.ACCENT_GREEN}{row2[0]:>2}{self.theme.RESET}. "
                line += f"{self.theme.TEXT_PRIMARY}{row2[1]:<8}{self.theme.RESET} "
                line += f"{self.theme.TEXT_SECONDARY}{row2[2]:<20}{self.theme.RESET}"
            
            line += f"{self.theme.BORDER}{self.theme.BOX_V}"
            print(line)
        
        print(f"{self.theme.BOX_V}{' '*78}{self.theme.BOX_V}")
        print(f"{self.theme.BOX_BL}{self.theme.BOX_H * 78}{self.theme.BOX_BR}{self.theme.RESET}")
        
        print(f"\n{self.theme.BG_PANEL}{self.theme.BORDER}")
        print(f"{self.theme.BOX_V}{self.theme.TEXT_PRIMARY}{self.theme.BOLD}{'COMMANDS':^78}{self.theme.RESET}{self.theme.BORDER}{self.theme.BOX_V}")
        print(f"{self.theme.BOX_V}{' '*78}{self.theme.BOX_V}")
        print(f"{self.theme.BOX_V}   {self.theme.ACCENT_GREEN}[1-10]{self.theme.RESET}  Select trading symbol{self.theme.BORDER}{self.theme.BOX_V}")
        print(f"{self.theme.BOX_V}   {self.theme.ACCENT_BLUE}[S]{self.theme.RESET}      View statistics{self.theme.BORDER}{self.theme.BOX_V}")
        print(f"{self.theme.BOX_V}   {self.theme.ACCENT_GOLD}[R]{self.theme.RESET}      Reset database{self.theme.BORDER}{self.theme.BOX_V}")
        print(f"{self.theme.BOX_V}   {self.theme.ACCENT_RED}[Q]{self.theme.RESET}      Quit Vision5{self.theme.BORDER}{self.theme.BOX_V}")
        print(f"{self.theme.BOX_BL}{self.theme.BOX_H * 78}{self.theme.BOX_BR}{self.theme.RESET}")
    
    def render_statistics(self, all_stats: Dict):
        """Render statistics view"""
        self.clear()
        self.render_logo()
        
        print(f"\n{self.theme.BG_PANEL}{self.theme.BORDER}")
        print(f"{self.theme.BOX_V}{self.theme.TEXT_PRIMARY}{self.theme.BOLD}{'GLOBAL PERFORMANCE STATISTICS':^78}{self.theme.RESET}{self.theme.BORDER}{self.theme.BOX_V}")
        print(f"{self.theme.BOX_V}{' '*78}{self.theme.BOX_V}")
        
        if not all_stats:
            print(f"{self.theme.BOX_V}   {self.theme.TEXT_MUTED}No trading data available yet{self.theme.BORDER}{self.theme.BOX_V}")
        else:
            total_trades = sum(s['total_trades'] for s in all_stats.values())
            total_profit = sum(s['total_profit'] for s in all_stats.values())
            total_wins = sum(s['winning_trades'] for s in all_stats.values())
            
            print(f"{self.theme.BOX_V}   {self.theme.TEXT_SECONDARY}AGGREGATE METRICS:{self.theme.RESET}{self.theme.BORDER}{self.theme.BOX_V}")
            print(f"{self.theme.BOX_V}      Total Trades: {self.theme.TEXT_PRIMARY}{total_trades}{self.theme.RESET}{self.theme.BORDER}{self.theme.BOX_V}")
            print(f"{self.theme.BOX_V}      Total Wins: {self.theme.ACCENT_GREEN}{total_wins}{self.theme.RESET}{self.theme.BORDER}{self.theme.BOX_V}")
            print(f"{self.theme.BOX_V}      Win Rate: {self.theme.ACCENT_GREEN if total_trades > 0 else self.theme.TEXT_MUTED}{(total_wins/total_trades*100) if total_trades > 0 else 0:.1f}%{self.theme.RESET}{self.theme.BORDER}{self.theme.BOX_V}")
            print(f"{self.theme.BOX_V}      Total P&L: {self.theme.ACCENT_GREEN if total_profit >= 0 else self.theme.ACCENT_RED}${total_profit:.2f}{self.theme.RESET}{self.theme.BORDER}{self.theme.BOX_V}")
            
            print(f"{self.theme.BOX_V}{' '*78}{self.theme.BOX_V}")
            print(f"{self.theme.BOX_V}   {self.theme.TEXT_SECONDARY}PER SYMBOL BREAKDOWN:{self.theme.RESET}{self.theme.BORDER}{self.theme.BOX_V}")
            print(f"{self.theme.BOX_V}   {'Symbol':<10} {'Trades':<8} {'Win Rate':<10} {'Profit':<12}{self.theme.BORDER}{self.theme.BOX_V}")
            print(f"{self.theme.BOX_V}   {self.theme.BORDER}{self.theme.BOX_V}")
            
            for symbol, stats in sorted(all_stats.items()):
                win_color = self.theme.ACCENT_GREEN if stats['win_rate'] >= 50 else self.theme.ACCENT_RED
                profit_color = self.theme.ACCENT_GREEN if stats['total_profit'] >= 0 else self.theme.ACCENT_RED
                
                print(f"{self.theme.BOX_V}   {self.theme.TEXT_PRIMARY}{symbol:<10}{self.theme.RESET} "
                      f"{stats['total_trades']:<8} "
                      f"{win_color}{stats['win_rate']:>5.1f}%{self.theme.RESET}   "
                      f"{profit_color}${stats['total_profit']:>9.2f}{self.theme.RESET}{self.theme.BORDER}{self.theme.BOX_V}")
        
        print(f"{self.theme.BOX_BL}{self.theme.BOX_H * 78}{self.theme.BOX_BR}{self.theme.RESET}")
        print(f"\n{self.theme.TEXT_SECONDARY}Press Enter to continue...{self.theme.RESET}")
        input()

# ============================================
# VISION5 MAIN APPLICATION
# ============================================

class Vision5App:
    """Main Vision5 application"""
    
    def __init__(self):
        self.ui = Vision5UI()
        self.market = MarketSimulator()
        self.ai_engines: Dict[str, Vision5AI] = {}
        self.trading_engines: Dict[str, TradingEngine] = {}
        self.running = True
        
        # Initialize for all symbols
        symbols = ["EURUSD", "GBPUSD", "USDJPY", "XAUUSD", "BTCUSD", "ETHUSD", "US30", "US500", "GER30", "UK100"]
        
        for symbol in symbols:
            self.ai_engines[symbol] = Vision5AI(symbol)
            self.trading_engines[symbol] = TradingEngine()
            
            # Warm up AI
            for _ in range(100):
                price = self.market.get_price(symbol)
                high, low = self.market.get_high_low(symbol)
                self.ai_engines[symbol].add_price(price, high, low)
        
        print(f"{self.ui.theme.ACCENT_GREEN}✓ Vision5 initialized successfully{self.ui.theme.RESET}")
        time.sleep(1)
    
    def run_symbol(self, symbol: str):
        """Run trading for specific symbol"""
        ai = self.ai_engines[symbol]
        engine = self.trading_engines[symbol]
        
        try:
            while self.running:
                # Update market data
                price = self.market.update_price(symbol)
                high, low = self.market.get_high_low(symbol)
                
                # Update AI
                ai.add_price(price, high, low)
                signal = ai.analyze()
                
                # Execute trades
                if signal.strength != SignalStrength.NEUTRAL and signal.confidence >= 50:
                    engine.execute_signal(signal)
                
                # Update positions
                engine.update_positions(price)
                
                # Render UI
                self.ui.render_trading_dashboard(symbol, price, signal, engine, ai)
                
                # Countdown
                for i in range(Config.UPDATE_INTERVAL, 0, -1):
                    print(f"\r{self.ui.theme.TEXT_SECONDARY}Next update in {i} seconds{self.ui.theme.RESET}", end="", flush=True)
                    time.sleep(1)
                print("\r" + " " * 40 + "\r", end="")
                
        except KeyboardInterrupt:
            print(f"\n{self.ui.theme.ACCENT_GOLD}Returning to menu...{self.ui.theme.RESET}")
            time.sleep(1)
    
    def show_statistics(self):
        """Show all statistics"""
        all_stats = {}
        for symbol, engine in self.trading_engines.items():
            stats = engine.get_stats()
            if stats['total_trades'] > 0:
                all_stats[symbol] = stats
        
        self.ui.render_statistics(all_stats)
    
    def reset_database(self):
        """Reset all trading data"""
        self.ui.clear()
        self.ui.render_logo()
        
        print(f"\n{self.ui.theme.BG_PANEL}{self.ui.theme.BORDER}")
        print(f"{self.ui.theme.BOX_V}{self.ui.theme.ACCENT_RED}{self.ui.theme.BOLD}{'⚠️  WARNING: This will delete all trading data!  ⚠️':^78}{self.ui.theme.RESET}{self.ui.theme.BORDER}{self.ui.theme.BOX_V}")
        print(f"{self.ui.theme.BOX_BL}{self.ui.theme.BOX_H * 78}{self.ui.theme.BOX_BR}{self.ui.theme.RESET}")
        
        confirm = input(f"\n{self.ui.theme.TEXT_PRIMARY}Type '{self.ui.theme.ACCENT_RED}RESET{self.ui.theme.TEXT_PRIMARY}' to confirm: {self.ui.theme.RESET}").strip()
        
        if confirm == 'RESET':
            # Reset all trading engines
            for symbol in self.trading_engines:
                self.trading_engines[symbol] = TradingEngine()
            print(f"\n{self.ui.theme.ACCENT_GREEN}✓ Database reset successfully{self.ui.theme.RESET}")
        else:
            print(f"\n{self.ui.theme.ACCENT_GOLD}Reset cancelled{self.ui.theme.RESET}")
        
        time.sleep(2)
    
    def run(self):
        """Main application loop"""
        def signal_handler(sig, frame):
            self.running = False
            print(f"\n{self.ui.theme.ACCENT_GREEN}Thank you for using Vision5!{self.ui.theme.RESET}")
            sys.exit(0)
        
        signal.signal(signal.SIGINT, signal_handler)
        
        while self.running:
            self.ui.render_menu()
            
            try:
                choice = input(f"\n{self.ui.theme.ACCENT_GREEN}{self.ui.theme.BOLD}➜ {self.ui.theme.RESET}").strip().upper()
                
                if choice == 'Q':
                    break
                elif choice == 'S':
                    self.show_statistics()
                elif choice == 'R':
                    self.reset_database()
                else:
                    symbol_map = {
                        "1": "EURUSD", "2": "GBPUSD", "3": "USDJPY",
                        "4": "XAUUSD", "5": "BTCUSD", "6": "ETHUSD",
                        "7": "US30", "8": "US500", "9": "GER30", "10": "UK100"
                    }
                    
                    if choice in symbol_map:
                        self.run_symbol(symbol_map[choice])
                    elif choice:
                        print(f"\n{self.ui.theme.ACCENT_RED}Invalid selection!{self.ui.theme.RESET}")
                        time.sleep(1)
                        
            except Exception as e:
                print(f"\n{self.ui.theme.ACCENT_RED}Error: {e}{self.ui.theme.RESET}")
                time.sleep(1)

# ============================================
# ENTRY POINT
# ============================================

def main():
    """Vision5 entry point"""
    parser = argparse.ArgumentParser(description='Vision5 Professional Trading Platform')
    parser.add_argument('--no-color', action='store_true', help='Disable colored output')
    
    args = parser.parse_args()
    
    if args.no_color:
        # Override colors with empty strings
        for attr in dir(Vision5Theme):
            if not attr.startswith('__'):
                setattr(Vision5Theme, attr, '')
    
    try:
        print(f"\n{Vision5Theme.SILVER_METALLIC}{Vision5Theme.BOLD}")
        print("╔═══════════════════════════════════════════════════════════════╗")
        print("║                      STARTING VISION5                        ║")
        print("║           Professional Trading Platform v5.0                 ║")
        print("╚═══════════════════════════════════════════════════════════════╝")
        print(f"{Vision5Theme.RESET}")
        
        print(f"{Vision5Theme.TEXT_SECONDARY}Initializing trading engines...{Vision5Theme.RESET}")
        time.sleep(1)
        
        app = Vision5App()
        app.run()
        
    except KeyboardInterrupt:
        print(f"\n{Vision5Theme.ACCENT_GREEN}Goodbye! Happy Trading!{Vision5Theme.RESET}")
        sys.exit(0)
    except Exception as e:
        print(f"\n{Vision5Theme.ACCENT_RED}Fatal Error: {e}{Vision5Theme.RESET}")
        sys.exit(1)

if __name__ == "__main__":
    main()
