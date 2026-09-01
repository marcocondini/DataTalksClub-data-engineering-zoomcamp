import sys

import pandas as pd

print(f"Arguments: {sys.argv}")
print("Hello, pipeline")

month = int(sys.argv[1])


print(f'hello pipeline, month = {month}')
df = pd.DataFrame({"days": [1, 2], "num_passengers": [3, 4]})
df["month"] = month
print(df.head())
df.to_parquet(f"output_{month}.parquet", engine="pyarrow", index=False)
