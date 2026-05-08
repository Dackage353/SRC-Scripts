from common import fetch_handler, file_helper, reference, src_helper, tool, constants
import time
from classes import Game


FORCE_FETCH = True
GAME_ID = '9d3wnky1' #iron mario

start = time.perf_counter()

if __name__ == '__main__':

    runs = fetch_handler.get_game_run_list(GAME_ID, FORCE_FETCH)
    tool.check_for_missing_names_in_run_list(runs)

    rejected_iron_runs = []

    for run in runs:
        if run.game_id == GAME_ID and run.verify_status == 'rejected':
            rejected_iron_runs.append(run)
            print(f'name:{reference.user_names[run.solo_player_id]} - run id: {run.run_id}')

    print(f'rejected runs count: {len(rejected_iron_runs)}')


    end = time.perf_counter()
    print(f"\nElapsed time: {end - start:.2f} seconds")


