# MR2DX Speedrun ID Picker

Find the monster that reaches the credits screen of **Monster Rancher 2 DX** the fastest.

The project turns the big `sdata_monster_*.csv` dump from LegendCup into a single
*Time-to-Credits* score for every breed/sub-type, applies the best legal offset
roll where applicable, and spits out a ranked list you can drop straight into
your speedrun notes.

---

## Why does this exist?

Running MR2 DX is a numbers game:

* You have ~104 in-game weeks before S-Rank.
* Training efficiency, guts-rate, and offset rolls matter more than raw HP.
* Rerolling CDs is legal, so “offset = Yes” breeds can spawn mini-god monsters.

Instead of eyeballing spreadsheets, this repo crunches the math, shows its work,
and tells you which **Monster ID** gets you to the trophy ceremony the quickest.

---

## Quick start

```bash
git clone https://github.com/your-github/mr2dx-speedrun-id-picker.git
cd mr2dx-speedrun-id-picker
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
jupyter lab  # or python tools/rank_ids.py --top 10
