import pandas as pd
import numpy as np


def score_for_offsets(offset1, offset2, base_stats, gains, guts_rate, offset_max):
    """Return the projected score for the given offset indices."""
    bonus = offset_max[offset1] + offset_max[offset2]
    stats = base_stats + bonus
    weeks = min(max(stats[6], 1), 104)
    heavy = int(weeks // 4)
    pow_gain, int_gain, ski_gain, spd_gain = gains
    pow_total = stats[1] + pow_gain * heavy
    int_total = stats[2] + int_gain * heavy
    main = pow_total if pow_gain > int_gain else int_total
    skill = stats[3] + ski_gain * heavy
    speed = stats[4] + spd_gain * heavy
    safe_guts = 20 if guts_rate == 0 else guts_rate
    score = (0.5 * main + 0.3 * skill + 0.2 * speed) * (20 / safe_guts) / weeks
    return score


def load_monster_data(monster_id: int):
    """Load base stats for the given monster ID and offset tables."""
    monster_df = pd.read_csv("sdata_monster.csv")
    monster_df.rename(columns={"Lifespan\n": "Lifespan"}, inplace=True)
    row = monster_df[monster_df["Monster ID"] == monster_id].iloc[0]
    base_stats = row[['Lif', 'Pow', 'Int', 'Ski', 'Spd', 'Def', 'Lifespan']].to_numpy(dtype=float)
    gains = row[['Pow gain', 'Int gain', 'Ski gain', 'Spd gain']].to_numpy(dtype=float)
    guts_rate = row['Guts Rate']

    off = pd.read_csv('sdata_monster_offset.csv', skiprows=1)
    max_cols = ['Unused.1', 'Pow.1', 'Def.1', 'Ski.1', 'Spd.1', 'Int.1', 'Lif/Lifespan.1']
    offset_max = off[max_cols].to_numpy()
    offset_max = offset_max[:, [0, 1, 5, 3, 4, 2, 6]]

    return base_stats, gains, guts_rate, offset_max


def main():
    monster_id = 1056
    base_stats, gains, guts_rate, offset_max = load_monster_data(monster_id)
    # Reading with low_memory=False avoids dtype warnings on large files
    entries = pd.read_csv(f"{monster_id}.csv", low_memory=False)
    # Drop rows without offset information and convert to integers
    entries = entries.dropna(subset=["Offset 1", "Offset 2"])
    entries["Offset 1"] = entries["Offset 1"].astype(int)
    entries["Offset 2"] = entries["Offset 2"].astype(int)

    scores = []
    for _, row in entries.iterrows():
        s = score_for_offsets(row['Offset 1'], row['Offset 2'], base_stats, gains, guts_rate, offset_max)
        scores.append(s)

    entries['Score'] = scores
    best = entries.loc[entries['Score'].idxmax()]
    print('Best Entry ID:', int(best['Entry ID']))
    print('Offsets:', int(best['Offset 1']), int(best['Offset 2']))
    print('Score:', best['Score'])


if __name__ == '__main__':
    main()
