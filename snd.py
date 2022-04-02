# %%
from sklearn.preprocessing import MaxAbsScaler, StandardScaler
import pandas as pd

from crypto_cast.dataprep import CryptoDataPrep

data_prep = CryptoDataPrep(
    train_path="data/train.csv",
    asset_details_path="data/asset_details.csv",
    asset_filter=["Bitcoin"],
)

data_prep.get_data()
#%%
train_data = data_prep.train_data
test_data = data_prep.test_data

#%%
data = test_data
#%%
data["High"] -= data["Open"]
data["Low"] -= data["Open"]
data["Close"] -= data["Open"]
data["VWAP"] -= data["Open"]
#%%
data.sample(30)
