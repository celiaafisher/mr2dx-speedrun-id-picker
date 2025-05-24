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

    return df


if __name__ == "__main__":
    df = load_monster_data()
    print(df.head())
