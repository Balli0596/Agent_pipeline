
import yfinance as yf


def get_stock_price(symbol: str) -> dict:
    """Get the latest available price for a stock ticker."""

    try:
        symbol = symbol.strip().upper()

        if not symbol:
            return {"error": "Please provide a stock ticker symbol."}

        ticker = yf.Ticker(symbol)
        history = ticker.history(period="5d", auto_adjust=False)

        if history.empty:
            return {"error": f"No price data found for {symbol}."}

        latest = history.dropna(subset=["Close"])

        if latest.empty:
            return {"error": f"No closing price available for {symbol}."}

        last_row = latest.iloc[-1]

        return {
            "symbol": symbol,
            "latest_close": round(float(last_row["Close"]), 2),
            "date": str(latest.index[-1].date()),
            "currency": ticker.info.get("currency", "Unknown"),
            "price_type": "latest available closing price",
        }

    except Exception as exc:
        return {"error": f"Stock service unavailable: {exc}"}
