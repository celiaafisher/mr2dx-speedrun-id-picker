import pandas as pd
import numpy as np


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

    # Projected stats after completing HeavyCycles of training
    df["ProjMain"] = df.apply(
        lambda row: row["Pow"] + row["Pow gain"] * row["HeavyCycles"]
        if row["MainStat"] == "Pow"
        else row["Int"] + row["Int gain"] * row["HeavyCycles"],
        axis=1,
    )
    df["ProjSkill"] = df["Ski"] + df["Ski gain"] * df["HeavyCycles"]
    df["ProjSpeed"] = df["Spd"] + df["Spd gain"] * df["HeavyCycles"]

    # Calculate a single score used for ranking monsters in a speedrun
    # Replace zero guts rates with 20 to avoid division by zero
    df["SafeGutsRate"] = df["Guts Rate"].replace(0, 20)


    df["Score"] = (
        (0.5 * df["ProjMain"] + 0.3 * df["ProjSkill"] + 0.2 * df["ProjSpeed"])
        * (20 / df["SafeGutsRate"])
        / df["WeeksAvail"]
    )

    # ------------------------------------------------------------------
    # Apply offset bonuses. Monsters with "No Offset" equal to 0 can gain
    # additional stats from two offset indices.  Each index provides a
    # random bonus between its minimum and maximum values.  To keep the
    # ranking deterministic we brute force every possible pair of indices
    # using the maximum bonus for each and keep the best resulting score.
    # ------------------------------------------------------------------

    # Read offset tables.  The CSV stores min and max values side by side
    # so we grab the max columns and map them to the monster stat order.
    off = pd.read_csv("sdata_monster_offset.csv", skiprows=1)
    max_cols = [
        "Unused.1",  # Lif
        "Pow.1",
        "Def.1",
        "Ski.1",
        "Spd.1",
        "Int.1",
        "Lif/Lifespan.1",
    ]
    offset_max = off[max_cols].to_numpy()

    # Map to [Lif, Pow, Int, Ski, Spd, Def, Lifespan]
    offset_max = offset_max[:, [0, 1, 5, 3, 4, 2, 6]]

    # Pre-compute all pairwise sums of offset bonuses
    pair_sums = offset_max[:, None, :] + offset_max[None, :, :]
    pair_sums = pair_sums.reshape(-1, 7)

    def calc_score(row, stats):
        lif, pow_, int_, ski, spd, def_, lifespan = stats
        weeks = min(max(lifespan, 1), 104)
        heavy = weeks // 4
        if row["Pow gain"] > row["Int gain"]:
            main = pow_ + row["Pow gain"] * heavy
        else:
            main = int_ + row["Int gain"] * heavy
        skill = ski + row["Ski gain"] * heavy
        speed = spd + row["Spd gain"] * heavy
        safe_guts = 20 if row["Guts Rate"] == 0 else row["Guts Rate"]
        return (0.5 * main + 0.3 * skill + 0.2 * speed) * (20 / safe_guts) / weeks

    # Iterate over monsters that can roll offsets
    for idx, row in df[df["No Offset"] == 0].iterrows():
        base = row[["Lif", "Pow", "Int", "Ski", "Spd", "Def", "Lifespan"]].to_numpy()
        stats = pair_sums + base

        weeks = np.clip(stats[:, 6], None, 104)
        heavy = (weeks // 4).astype(int)
        if row["Pow gain"] > row["Int gain"]:
            main = stats[:, 1] + row["Pow gain"] * heavy
        else:
            main = stats[:, 2] + row["Int gain"] * heavy
        skill = stats[:, 3] + row["Ski gain"] * heavy
        speed = stats[:, 4] + row["Spd gain"] * heavy
        safe_guts = 20 if row["Guts Rate"] == 0 else row["Guts Rate"]
        scores = (0.5 * main + 0.3 * skill + 0.2 * speed) * (20 / safe_guts) / weeks
        df.at[idx, "Score"] = scores.max()

    return df


if __name__ == "__main__":
    df = load_monster_data()
    print(df.head())
