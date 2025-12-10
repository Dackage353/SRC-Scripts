# SRC-Scripts
derivative of AussieAdam's src scripts
https://github.com/aussieadam/SM64RomhackSRC

- these are python scripts which can be ran simply by double clicking them (must install python)
- a leaderboard is a list of runs ranked by placing. it does not include obsolete or rejected runs
- a run list includes all runs for that category. it includes obsolete and rejected runs

## fetch_category_leaderboards.py
- set the category id's, then run the script
- the output will be in the "leaderboard_dump" folder

## fetch_category_run_lists.py
- set the category id's, then run the script
- .csv files will be in the "output" folder
- the json dumps will be in the "category_run_list_dump" folder

## fetch_rom_hack_list.py
- the json dump will be in the "dump" folder

## make_league_stats.py
- makes the stats for the rom hack league
- set the category id's, start and end date, then run the script
- the output will be in the "output" folder