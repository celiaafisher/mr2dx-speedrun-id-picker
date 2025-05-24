import pandas as pd


def load_monster_data(part1_path="en_sqlout_1.csv", part2_path="en_sqlout_2.csv"):
    """Load the two en_sqlout CSV files and clean their column names.

    Parameters
    ----------
    part1_path : str
        Path to the first CSV file.
    part2_path : str
        Path to the second CSV file.

    Returns
    -------
    pandas.DataFrame
        Concatenated dataframe with cleaned columns.
    """
    df1 = pd.read_csv(part1_path)
    df2 = pd.read_csv(part2_path)

    df = pd.concat([df1, df2], ignore_index=True)

    df.rename(
        columns={
            "Lifespan\n": "Lifespan",
            "Arena speed": "ArenaSpeed",
        },
        inplace=True,
    )

    # Add additional training information used in speedrun notes
    df["WeeksAvail"] = df["Lifespan"].clip(upper=104)
    df["HeavyCycles"] = (df["WeeksAvail"] // 4).astype(int)

    # Decide which stat to prioritize for training
    df["MainStat"] = df.apply(
        lambda row: "Pow" if row["Pow gain"] > row["Int gain"] else "Int",
        axis=1,
    )

    return df


if __name__ == "__main__":
    df = load_monster_data()
    print(df.head())
