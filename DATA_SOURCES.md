## Data Sources

### Binance Public Market Data
- **Source:** [binance/binance-public-data](https://github.com/binance/binance-public-data) by Binance (https://www.binance.com)
- **Data accessed from:** https://data.binance.vision (Binance's official public S3 bucket)
- **Data types used:** Spot Klines (OHLCV, 1-minute), AggTrades
- **Usage:** Research and educational purposes only. Raw data files are NOT
  redistributed in this repository. The `src/data_loader.py` script downloads
  data directly from the official Binance source at runtime.
- **Terms:** See Binance Terms of Use at https://www.binance.com/en/terms
