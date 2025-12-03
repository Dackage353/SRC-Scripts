from datetime import datetime, timezone
from pathlib import Path
import src_helper
import json
import pandas as pd
import data_classes

game_names = {}
category_names = {}
player_names = {}

runs = []
valid_runs = []
invalid_runs = []

json_files = [
    "ksitt_0_burger.json",
    "ksitt_30_burger.json",
    "ksitt_40_burger.json",
    "bb_any%.json",
    "bb_any%_warpless.json",
    "bb_111_star.json",
    "ama_0_star.json",
    "ama_50_star.json",
    "ama_120_star.json"
]

start_time = datetime(2025, 10, 4, 4, 35, tzinfo=timezone.utc)
end_time = datetime(2025, 12, 1, 11, 0, tzinfo=timezone.utc)


def load_names(file_name):
    path = Path(f"reference/{file_name}")
    
    if path.exists():
        with path.open("r") as file:
            return json.load(file)
    
    return {}
    
    
def process_category_json(file_name):
    path = f"raw_data/{file_name}"
    
    with open(path, "r") as f:
        data = json.load(f)["data"]
        
        for run_data in data:
            run = data_classes.Run.create_from_json(run_data)
            
            runs.append(run)
            if start_time <= run.time_submitted <= end_time and run.verified_status == "verified":
                valid_runs.append(run)
            else:
                invalid_runs.append(run)
    
    
def fetch_missing_names():
    for run in runs:
        if run.game_id not in game_names:
            game_data = src_helper.request_src(src_helper.get_game(run.game_id))["data"]
            game_name = game_data["names"]["international"]
            game_names[run.game_id] = game_name
            print(f"fetched name for {run.game_id} - {game_name}")
            
        if run.category_id not in category_names:
            category_data = src_helper.request_src(src_helper.get_category(run.category_id))["data"]
            category_name = category_data["name"]
            category_names[run.category_id] = category_name
            print(f"fetched name for {run.category_id} - {category_name}")
            
        if run.player_id not in player_names:
            player_data = src_helper.request_src(src_helper.get_user(run.player_id))["data"]
            player_name = player_data["names"]["international"]
            player_names[run.player_id] = player_name
            print(f"fetched name for {run.player_id} - {player_name}")
            
        if run.verifier_id not in player_names:
            verifier_data = src_helper.request_src(src_helper.get_user(run.verifier_id))["data"]
            verifier_name = verifier_data["names"]["international"]
            player_names[run.verifier_id] = verifier_name
            print(f"fetched name for {run.verifier_id} - {verifier_name}")
    
    
def make_files_for_runs(runs, file_name):
    df = get_data_frame_for_runs(runs)
    
    csv_path = Path(f"output/{file_name}.csv")
    csv_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(str(csv_path), index=False)
    
    make_text_file(df.groupby("game_name").size().to_string(header=False), f"output/{file_name} - runs per game.txt")
    make_text_file(df.groupby("category_name").size().to_string(header=False), f"output/{file_name} - runs per category.txt")
    make_text_file(df.groupby("player_name").size().to_string(header=False), f"output/{file_name} - runs per player.txt")
    make_text_file(df.groupby("verifier_name").size().to_string(header=False), f"output/{file_name} - runs per verifier.txt")
    
    
def sort_and_save_names(names, file_name):
    sorted_names = dict(sorted(names.items(), key=lambda item: item[1]))
    
    path = Path(f"reference/{file_name}")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(sorted_names, indent=4))
    
    
def get_data_frame_for_runs(runs):
    run_dicts = [vars(run) for run in runs]
    df = pd.DataFrame(run_dicts)
    
    
    df["game_name"] = df["game_id"].map(game_names)
    df["category_name"] = df["category_id"].map(category_names)
    df["player_name"] = df["player_id"].map(player_names)
    df["verifier_name"] = df["verifier_id"].map(player_names)
    
    df = df[sorted(df.columns)]
    df = df.sort_values(["game_name", "category_name", "player_name"], ascending=[True, True, True])
    
    return df
    
    
def make_text_file(text, file_name):
    path = Path(file_name)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text)
    
    
if __name__ == "__main__":
    game_names = load_names("game_names.json")
    category_names = load_names("category_names.json")
    player_names = load_names("player_names.json")
    
    for file_name in json_files:
        process_category_json(file_name)
    
    fetch_missing_names()
    
    make_files_for_runs(valid_runs, "valid_runs")
    make_files_for_runs(invalid_runs, "invalid_runs")
    make_files_for_runs(runs, "runs")
    
    sort_and_save_names(game_names, "game_names.json")
    sort_and_save_names(category_names, "category_names.json")
    sort_and_save_names(player_names, "player_names.json")
    