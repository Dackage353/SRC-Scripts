from pathlib import Path
from common import fetch_handler, file_helper, reference, src_helper, tool, constants
from classes import Game
import time


script_start = time.perf_counter()

FORCE_FETCH = False


if __name__ == '__main__':
    path = Path("output/game_report.txt")
    path.parent.mkdir(parents=True, exist_ok=True)

    with open(path, "w", encoding="utf-8") as f:
        game_data = fetch_handler.get_series_info(constants.MAIN_SERIES, FORCE_FETCH)
        game_data.extend(fetch_handler.get_series_info(constants.SECONDARY_SERIES, FORCE_FETCH))

        games = []

        for data in game_data:
            games.append(Game(data))

        fullgame_category_count = 0
        level_count = 0
        single_star_count = 0

        for game in games:
            print(game.name, file=f)
            print('-----', file=f)

            fullgame_category_count += len(game.fullgame_categories)
            level_count += len(game.levels)
            single_star_count += len(game.single_stars)

            print('fullgames\n-', file=f)
            for fullgame_category in game.fullgame_categories:
                print(fullgame_category.name, file=f)

            print('\nstage_rtas\n-', file=f)
            for stage_rta in game.stage_rtas:
                print(stage_rta.name, file=f)

            print('\nsingle_stars\n-', file=f)
            for single_star in game.single_stars:
                print(single_star.name, file=f)

            print('', file=f)

        print(f'games: {len(games)}', file=f)
        print(f'fullgame_categories: {fullgame_category_count}', file=f)
        print(f'levels: {level_count}', file=f)
        print(f'single_stars: {single_star_count}', file=f)
    
    script_end = time.perf_counter()
    print(f"\nElapsed time: {script_end - script_start:.2f} seconds")
