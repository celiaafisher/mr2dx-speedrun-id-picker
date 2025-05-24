import argparse
from load_monster_data import load_monster_data

def main(top_n):
    df = load_monster_data()
    ranked = df.sort_values("Score", ascending=False)
    print(ranked[["Monster ID", "Name-English", "Main", "Sub", "Score"]].head(top_n).to_string(index=False))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Rank monsters by calculated score.")
    parser.add_argument("--top", type=int, default=20, help="Number of monsters to display")
    args = parser.parse_args()
    main(args.top)
