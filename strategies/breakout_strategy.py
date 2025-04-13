
import pandas as pd

class BreakoutStrategy:
    def __init__(self, parameters: dict):
        self.parameters = parameters

    def generate_signals(self, candle_data):
        """
        Groups 1-minute candles into 15-minute blocks, takes the first minute's high/low, 
        and returns a breakout signal if later candles break that range.
        """
        df = pd.DataFrame(candle_data)
        df['time'] = pd.to_datetime(df['time'])
        df.sort_values(by='time', inplace=True)
        df['15min_group'] = df['time'].dt.floor('15T')
        signals = []
        for group, group_data in df.groupby('15min_group'):
            if len(group_data) < 2:
                continue  # Skip if insufficient data in the group
            first_minute = group_data.iloc[0]
            first_high = first_minute['high']
            first_low = first_minute['low']
            signal = None
            # Check for breakout conditions
            for _, row in group_data.iloc[1:].iterrows():
                if row['high'] > first_high:
                    signal = "buy"
                    break
                elif row['low'] < first_low:
                    signal = "sell"
                    break
            signals.append({"group": group, "signal": signal})
        return signals
