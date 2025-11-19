import pandas as pd, json, yaml
from tsfresh import extract_features
from sklearn.tree import DecisionTreeClassifier, export_text
from pathlib import Path

with open("config.yaml") as f:
    config = yaml.safe_load(f)

df = pd.read_parquet("processed_data.parquet")
all_rules = {}

for actuator in config["actuators"]:
    cmd = actuator["command_tag"]
    if cmd not in df.columns:
        continue

    y = df[cmd].shift(-1).fillna(0) > df[cmd]   # detect rising edge (start)
    relevant = actuator["relevant_tags"] + [cmd]
    X = df[relevant]

    # Simple but extremely effective features
    extracted = extract_features(X, column_id=lambda x: 0, column_sort=lambda x: 0,
                                 default_fc_parameters={"last": None, "maximum": None, "minimum": None, "mean": None})

    # Add lag features manually (very important for control logic)
    for col in relevant:
        for lag in [1, 3, 6, 12]:   # 10s, 30s, 1min, 2min ago
            extracted[f"{col}_lag{lag}"] = X[col].shift(lag * (10//pd.Timedelta(config["resample_interval"]).seconds))

    extracted = extracted.dropna()

    model = DecisionTreeClassifier(max_depth=6, min_samples_leaf=0.005)
    model.fit(extracted.iloc[:,1:], y.loc[extracted.index])   # drop constant id column

    text_rules = export_text(model, feature_names=extracted.columns[1:].tolist(), decimals=1)
    all_rules[actuator["name"]] = {
        "tag": cmd,
        "rules_text": text_rules,
        "feature_importance": dict(zip(extracted.columns[1:], model.feature_importances_))
    }

Path("rules.json").write_text(json.dumps(all_rules, indent=2))
print("Rules discovered and saved to rules.json")
