from typing import List, Tuple

import pandas as pd
import sklearn
from sklearn.preprocessing import MaxAbsScaler, StandardScaler


class CryptoDataPrep:
    def __init__(
        self,
        train_path: str,
        asset_details_path: str,
        asset_filter: List[str] = None,
        train_test_ratio: float = 0.8,
    ) -> None:

        self.train_path = train_path
        self.asset_details_path = asset_details_path
        self.asset_filter = asset_filter
        self.train_test_ratio = train_test_ratio

    def get_data(self):

        data = self.load_data()
        data = self.independent_scaling(data)
        self.train_data, self.test_data = self.train_test_split(data)
        self.normalize_data()

    def load_data(self) -> pd.DataFrame:

        cc_data = pd.merge(
            pd.read_csv(self.train_path),
            pd.read_csv(self.asset_details_path),
            on="Asset_ID",
        )

        cc_data["timestamp"] = cc_data["timestamp"].astype("datetime64[s]")
        cc_data["Asset_Name"] = cc_data["Asset_Name"].astype("category")
        cc_data["Count"] = cc_data["Count"].astype("int32")

        cc_data.drop(["Asset_ID", "Weight"], axis=1, inplace=True)

        if self.asset_filter:
            cc_data = cc_data[cc_data["Asset_Name"].isin(self.asset_filter)]

        return cc_data

    def independent_scaling(self, data):

        data["High"] -= data["Open"]
        data["Low"] -= data["Open"]
        data["Close"] -= data["Open"]
        data["VWAP"] -= data["Open"]

        return data

    def train_test_split(self, data: pd.DataFrame) -> Tuple[pd.DataFrame]:

        train_size = int(len(data) * self.train_test_ratio)
        test_size = len(data) - train_size

        train_data = data.head(train_size)
        test_data = data.tail(test_size)

        return (train_data, test_data)

    def normalize_data(
        self, scaler: sklearn.base.TransformerMixin = MaxAbsScaler
    ) -> None:

        self.scaler = scaler()
        scalable_data_types = ["float64", "int32"]

        scalable_data = self.train_data.select_dtypes(include=scalable_data_types)
        scalable_column = scalable_data.columns

        self.scaler = self.scaler.fit(scalable_data)

        self.train_data.loc[:, scalable_column] = self.scaler.transform(scalable_data)

        self.test_data.loc[:, scalable_column] = self.scaler.transform(
            self.test_data[scalable_column]
        )
