"""
data_loader.py
Downloads Binance public klines from data.binance.vision
Data source: https://github.com/binance/binance-public-data
"""

import os
import io
import zipfile
import requests
import pandas as pd
from tqdm import tqdm

KLINE_COLS = [
    "open_time", "open", "high", "low", "close", "volume",
    "close_time", "quote_asset_volume", "num_trades",
    "taker_buy_base_vol", "taker_buy_quote_vol", "ignore"
]

BASE_URL = "https://data.binance.vision/data/spot/monthly/klines"


def download_klines(symbol: str, interval: str, year: int, month: int,
                    save_dir: str = "data/raw") -> pd.DataFrame:
    """Download one month of klines from Binance public data."""
    os.makedirs(save_dir, exist_ok=True)
    filename = f"{symbol}-{interval}-{year}-{month:02d}"
    csv_path = os.path.join(save_dir, filename + ".csv")

    if os.path.exists(csv_path):
        print(f"  [cache] {filename}.csv already exists, loading from disk.")
        return _load_csv(csv_path)

    url = f"{BASE_URL}/{symbol}/{interval}/{filename}.zip"
    print(f"  [download] {url}")
    response = requests.get(url, timeout=60)
    if response.status_code != 200:
        raise FileNotFoundError(f"Could not download: {url} (status {response.status_code})")

    with zipfile.ZipFile(io.BytesIO(response.content)) as zf:
        zf.extractall(save_dir)

    return _load_csv(csv_path)


def _load_csv(path: str) -> pd.DataFrame:
    df = pd.read_csv(path, header=None, names=KLINE_COLS)
    df["open_time"] = pd.to_datetime(df["open_time"], unit="ms")
    df["close_time"] = pd.to_datetime(df["close_time"], unit="ms")
    for col in ["open", "high", "low", "close", "volume",
                "taker_buy_base_vol", "taker_buy_quote_vol"]:
        df[col] = df[col].astype(float)
    df["num_trades"] = df["num_trades"].astype(int)
    return df.set_index("open_time")


def load_range(symbol: str, interval: str, start_year: int,
               start_month: int, end_month: int,
               save_dir: str = "data/raw") -> pd.DataFrame:
    """Load multiple months and concatenate into one DataFrame."""
    frames = []
    for month in tqdm(range(start_month, end_month + 1), desc="Loading months"):
        df = download_klines(symbol, interval, start_year, month, save_dir)
        frames.append(df)
    return pd.concat(frames).sort_index()
