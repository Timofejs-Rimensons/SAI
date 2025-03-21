import pandas as pd


df = pd.DataFrame(columns=("timestamp", "btn_state"))
df.to_csv("button_data.csv", index=False)

