#!/usr/bin/env python3
"""
Recalculate EU CP rankings from Seattle Regional onward (tournament ID >= 0055),
including crossed-out (dropped) CP. For LAIC stipend calculation.

Limitless only serves 150 players server-side per page.
Stipend cutoff is typically top 22-32, so 150 is more than enough.

Usage: python3 laic_stipend.py [--limit N] [--delay SECONDS]
"""

import requests
from bs4 import BeautifulSoup
import re
import time
import argparse

BASE_URL = "https://labs.limitlesstcg.com"
SEATTLE_TOURNAMENT_ID = 55  # /0055 = Regional Championship Seattle, Feb 27-Mar 1 2026


def fetch(url):
    resp = requests.get(url)
    return BeautifulSoup(resp.content, 'html.parser')  # use .content for proper UTF-8


def get_top_players():
    soup = fetch(f"{BASE_URL}/rankings?season=2026&region=EU&show=150")
    table = soup.select_one('table.data-table tbody')
    if not table:
        return []

    players = []
    seen = set()
    for row in table.find_all('tr'):
        cols = row.find_all('td')
        if len(cols) < 3:
            continue
        a = cols[1].find('a', href=re.compile(r'^/players/'))
        if not a:
            continue
        href = a['href']
        if href in seen:
            continue
        seen.add(href)
        players.append({"name": a.text.strip(), "url": BASE_URL + href})
    return players


def get_player_cp_from_seattle(player_url):
    soup = fetch(player_url)
    table = soup.select_one('table.data-table tbody')
    if not table:
        return 0

    total = 0
    for row in table.find_all('tr'):
        cols = row.find_all('td')
        if len(cols) < 6:
            continue
        link = cols[1].find('a', href=re.compile(r'^/\d+/'))
        if not link:
            continue
        m = re.match(r'/(\d+)/', link['href'])
        if not m:
            continue
        if int(m.group(1)) < SEATTLE_TOURNAMENT_ID:
            continue
        cp_text = cols[5].get_text(strip=True)
        cp_m = re.search(r'\d+', cp_text)
        if cp_m:
            total += int(cp_m.group())
    return total


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--limit', type=int, default=150)
    parser.add_argument('--delay', type=float, default=0.3)
    args = parser.parse_args()

    print("Fetching top EU players from Limitless...", flush=True)
    players = get_top_players()[:args.limit]
    print(f"Found {len(players)} unique players. Scraping profiles...", flush=True)

    results = []
    for i, p in enumerate(players):
        cp = get_player_cp_from_seattle(p['url'])
        results.append({"name": p['name'], "cp": cp})
        if (i + 1) % 25 == 0:
            print(f"  {i+1}/{len(players)} done...", flush=True)
        time.sleep(args.delay)

    results.sort(key=lambda x: x['cp'], reverse=True)

    print(f"\n{'#':<4} {'Name':<40} {'CP':>5}")
    print("-" * 51)
    for i, r in enumerate(results, 1):
        print(f"{i:<4} {r['name']:<40} {r['cp']:>5}")


if __name__ == "__main__":
    main()
