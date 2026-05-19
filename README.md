# ptcg-tools

Tools for Pokémon TCG competitive play analysis.

## LAIC Stipend Calculator

Recalculates the EU Championship Points leaderboard from a specific tournament onward, **including dropped (crossed-out) CP**. Useful for estimating LAIC travel stipend eligibility.

### How it works

1. Scrapes the top 150 EU players from [Limitless Labs](https://labs.limitlesstcg.com/rankings?season=2026&region=EU)
2. Visits each player's profile and sums all CP from tournaments with ID ≥ 0055 (Seattle Regional, Feb 28 2026, onward)
3. Includes crossed-out/dropped points that were earned in that timeframe
4. Outputs a ranked leaderboard sorted by recalculated CP

### Usage

```bash
pip install requests beautifulsoup4
python3 laic_stipend.py --region EU
```

Options:
- `--region` — Region to query: `EU`, `NA`, `LA`, `OC`, `Global` (default: EU)
- `--limit N` — Number of players to process (max 150, default 150)
- `--delay S` — Delay between requests in seconds (default 0.3)

### Notes

- Limitless only serves 150 players per page server-side. For stipend purposes (top 22–32) this is more than sufficient.
- Data comes from Limitless Labs, which may have minor discrepancies vs official Pokémon rankings.
- The official Pokémon leaderboard API (`pokemon.com`) only provides total CP without per-event breakdown, so Limitless is required for this calculation.
