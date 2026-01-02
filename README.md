# SRC-Scripts
derivative of AussieAdam's src scripts
https://github.com/aussieadam/SM64RomhackSRC

- these are python scripts which can be ran simply by double clicking them (must install python)
- easily install the modules used by opening "_install modules.bat"

### Tips
- a leaderboard is a list of runs ranked by placing. it does not include obsolete or rejected runs
- a run list includes all runs for that category. it includes obsolete and rejected runs

## fetch_category_info.py
- fetches basic category info dumps without runs
- set the category id's, then run the script
- the json dumps will be in "category_info_dump"

## fetch_game_info.py
- fetches basic game info dumps without runs
- set the game id's, then run the script
- it will print the key info. the full dump is in "hack_info"

## fetch_leaderboards.py
- fetches category leaderboard dumps
- set the category id's, then run the script
- the output will be in "leaderboard_dump"

## fetch_run_lists.py
- fetches category run list dumps
- set the category id's, then run the script
- .csv files will be in "output"
- the json dumps will be in "category_run_list_dump"

## make_league_stats.py
- makes the stats for the rom hack league
- set the category id's, start and end date, then run the script
- the output will be in the "output" folder

## Self explanatory
- print_fullgame_categories_without_rules.py
- print_fullgame_category_list.py
- print_hack_list.py
- print_hack_platform_count.py
- print_hacks_without_levels.py
- print_non_main_mods.py