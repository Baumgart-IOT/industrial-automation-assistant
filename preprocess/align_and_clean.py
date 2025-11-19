import pandas as pd
import yaml

with open("config.yaml") as f:
    config = yaml.safe_load(f)

df = pd.read_parquet("raw_data.parquet")
df = df.resample(config["resample_interval"]).mean()
df = df.ffill().bfill()                     # forward-fill digital commands
df = df.dropna(thresh=int(len(df)*0.95), axis=1)  # drop almost-empty tags
df.to_parquet("processed_data.parquet")
print(f"Clean dataset ready: {df.shape}")
