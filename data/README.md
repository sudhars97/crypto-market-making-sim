# Data Directory

Raw market data files are NOT committed to this repository.

## How to download data
Run `src/data_loader.py` or execute notebook `01_data_exploration.ipynb`.
Data is fetched directly from Binance's public S3 bucket:
  https://data.binance.vision

## What gets downloaded
- Spot Klines (OHLCV) at 1-minute intervals for BTCUSDT
- Stored locally under `data/raw/` (gitignored)

## Sample file
`data/sample/BTCUSDT-1m-sample.csv` — one day of 1-min bars included
for reproducibility and quick testing without downloading full data.

## Attribution
See DATA_SOURCES.md at the root of this repository.
