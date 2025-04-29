import pandas as pd

class BreakoutStrategy:
    
    # BreakoutStrategy identifies simple breakout signals on 15-min candle data.
    # It produces a trade table DataFrame with columns: ['timestamp', 'signal', 'price', 'quantity']

    def __init__(self, breakout_window: int = 15, quantity: int = 1):
        self.breakout_window = breakout_window
        self.quantity = quantity

    def generate_trades(self, candles: pd.DataFrame) -> pd.DataFrame:
        
        # candles: DataFrame with columns ['timestamp', 'open', 'high', 'low', 'close']
        # Returns trades where price breaks above the high of the prior N bars.
        
        trades = []
        for idx in range(self.breakout_window, len(candles)):
            window = candles.iloc[idx - self.breakout_window: idx]
            curr = candles.iloc[idx]
            prev_high = window['high'].max()

            # Long breakout
            if curr['close'] > prev_high:
                trades.append({
                    'timestamp': curr['timestamp'],
                    'signal': 'BUY',
                    'price': curr['close'],
                    'quantity': self.quantity
                })
            # Optional: Short breakout
            # Uncomment below to enable shorts
            prev_low = window['low'].min()
            if curr['close'] < prev_low:
                trades.append({
                    'timestamp': curr['timestamp'],
                    'signal': 'SELL',
                    'price': curr['close'],
                    'quantity': self.quantity
                })

        return pd.DataFrame(trades)