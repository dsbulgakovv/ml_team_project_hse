import pandas as pd


def split_df(df: pd.DataFrame, n_days: int) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Split dataframe into train and test using amount of days as separator

    :param df: dataframe with user's interactions
    :param n_days: days since the last one to split dataframe
    :return: train and test dataframes
    """
    df["last_watch_dt"] = pd.to_datetime(df["last_watch_dt"])
    test_df = df[
        df["last_watch_dt"] >= df["last_watch_dt"].max() - pd.DateOffset(days=n_days)
    ].copy()
    train_df = df[
        df["last_watch_dt"] < df["last_watch_dt"].max() - pd.DateOffset(days=n_days)
    ].copy()
    return train_df, test_df
