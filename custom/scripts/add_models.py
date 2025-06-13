import os
import sys
import json
import requests
import traceback
from pathlib import Path
from dotenv import load_dotenv

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parents[1]

if not os.getenv("CI"): # CI is a built-in environment variable in GitLab
    ENV_PATH = SCRIPT_DIR.joinpath(".env").resolve()
    load_dotenv(dotenv_path=ENV_PATH)

sys.path.insert(1, str(PROJECT_ROOT)) # Add project root to path

from custom.scripts.models_config import models
from custom.scripts.utils import require_env_var

LITELLM_API_URI = require_env_var("LITELLM_API_URI")
LITELLM_MASTER_KEY = require_env_var("LITELLM_MASTER_KEY")

def check_model_exists(model_name):
    try:
        response = requests.get(
            f"{LITELLM_API_URI}/model/info",
            headers={"Authorization": f"Bearer {LITELLM_MASTER_KEY}"}
        )

        if response.status_code == 200:
            response_json = response.json()
            if "data" in response_json and isinstance(response_json["data"], list):
                models = response_json["data"]
                for model in models:
                    if model.get("model_name") == model_name:
                        return model.get("model_info", {}).get("id")
                return False
            else:
                raise Exception(f"Unexpected response format: {response_json}")
        else:
            raise Exception(f"Failed to get models. Status code: {response.status_code}. Response: {response.text}")
    except Exception as e:
        raise Exception(f"Error checking model existence: {e}")

def add_model_to_litellm(model):
    model_name = model["model_name"]
    try:
        response = requests.post(
            f"{LITELLM_API_URI}/model/new",
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {LITELLM_MASTER_KEY}"
            },
            data=json.dumps(model)
        )
        if response.status_code == 200:
            print(f"Model {model_name} added successfully.")
        else:
            raise Exception(f"Failed to add model. Status code: {response.status_code}. Response: {response.text}")
    except Exception as e:
        raise Exception(f"Error adding model {model_name}: {e}")
    
def update_model(model, model_id):
    model_name = model["model_name"]
    try:
        response = requests.patch(
            f"{LITELLM_API_URI}/model/{model_id}/update",
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {LITELLM_MASTER_KEY}"
            },
            data=json.dumps(model)
        )
        if response.status_code == 200:
            print(f"Model {model_name} updated successfully.")
        else:
            raise Exception(f"Failed to update model. Status code: {response.status_code}. Response: {response.text}")
    except Exception as e:
        raise Exception(f"Error updating model {model_name}: {e}")

def add_models_to_team(team_id: str, model_names: list[str]):
    """
    Add models to a team's allowed model list.
    
    Args:
        team_id (str): The team ID to add models to
        model_names (list): List of model names to add to the team
    """
    try:
        payload = {
            "team_id": team_id,
            "models": model_names
        }
        
        response = requests.post(
            f"{LITELLM_API_URI}/team/model/add",
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {LITELLM_MASTER_KEY}"
            },
            data=json.dumps(payload)
        )
        
        if response.status_code == 200:
            print(f"Successfully added models {model_names} to team {team_id}.")
            return response.json()
        else:
            raise Exception(f"Failed to add models to team. Status code: {response.status_code}. Response: {response.text}")
    except Exception as e:
        raise Exception(f"Error adding models to team {team_id}: {e}")

if __name__ == "__main__":
    # Load model configurations
    try:
        for model in models:
            model_name = model["model_name"]
            model_id = check_model_exists(model_name)
            
            if model_id:
                print(f"Model {model_name} already exists. Updating.")
                update_model(model, model_id)
            else:
                print(f"Adding model: {model_name}")
                add_model_to_litellm(model)
            
            if model_name.endswith("-birthright"):
                add_models_to_team(
                    team_id="api-key-depot-birthright-keys",
                    model_names=[model_name]
                )
                
            if model_name.endswith("-project"):
                add_models_to_team(
                    team_id="api-key-depot-project-keys",
                    model_names=[model_name]
                )
                
    except Exception as e:
        print(f"Error: {e}")
        traceback.print_exc()
        exit(1)