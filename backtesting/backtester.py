# backtesting/backtester.py
import pandas as pd
import numpy as np

def calculate_sharpe_ratio(returns, risk_free_rate=0):
    """Calculates the Sharpe ratio for the given returns."""
    mean_return = np.mean(returns)
    std_return = np.std(returns)
    return (mean_return - risk_free_rate) / std_return if std_return != 0 else np.nan

def calculate_max_drawdown(equity_curve):
    """Calculates the maximum drawdown from an equity curve."""
    cumulative_max = equity_curve.cummax()
    drawdowns = (equity_curve - cumulative_max) / cumulative_max
    return drawdowns.min()

class Backtester:
    def __init__(self, initial_capital=100000):
        self.initial_capital = initial_capital

    def run_strategy(self, strategy, historical_data):
        """
        Runs a single strategy on historical data.
        The strategy is expected to have a generate_signals method.
        Returns a list of returns and an equity curve series.
        """
        signals = strategy.generate_signals(historical_data)
        equity_curve = []
        capital = self.initial_capital
        returns = []
        # For illustration: apply a fixed percentage change per signal.
        for signal in signals:
            if signal['signal'] == "buy":
                daily_return = 0.01   # Assume 1% profit for a buy signal
            elif signal['signal'] == "sell":
                daily_return = -0.01  # Assume 1% loss for a sell signal
            else:
                daily_return = 0  # No action means 0% change
            returns.append(daily_return)
            capital *= (1 + daily_return)
            equity_curve.append(capital)
        return returns, pd.Series(equity_curve)

    def run_backtests(self, strategies, historical_data):
        """
        Runs backtests for all provided strategies and computes key metrics.
        Returns a dictionary keyed by the strategy’s class name.
        """
        results = {}
        for strategy in strategies:
            returns, equity_curve = self.run_strategy(strategy, historical_data)
            sharpe = calculate_sharpe_ratio(returns)
            max_dd = calculate_max_drawdown(equity_curve)
            win_rate = np.mean([1 if r > 0 else 0 for r in returns])
            results[type(strategy).__name__] = {
                "sharpe_ratio": sharpe,
                "max_drawdown": max_dd,
                "win_rate": win_rate,
                "final_equity": equity_curve.iloc[-1]
            }
        return results

# Example usage:
if __name__ == "__main__":
    # Dummy historical data sample
    sample_data = [
        {"time": "2023-04-01 09:15:00", "open": 100, "high": 102, "low": 99, "close": 101},
        {"time": "2023-04-01 09:16:00", "open": 101, "high": 103, "low": 100, "close": 102},
        {"time": "2023-04-01 09:17:00", "open": 102, "high": 102.5, "low": 100, "close": 101},
        # Add more data as needed...
    ]
    # Import your strategy; here we assume a breakout strategy exists.
    from strategies.breakout_strategy import BreakoutStrategy
    strategy_instance = BreakoutStrategy(parameters={"dummy": True})
    
    backtester = Backtester(initial_capital=100000)
    results = backtester.run_backtests([strategy_instance], sample_data)
    print("Backtesting results:", results)
