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

from custom.scripts.utils import require_env_var

LITELLM_API_URI = require_env_var("LITELLM_API_URI")
LITELLM_MASTER_KEY = require_env_var("LITELLM_MASTER_KEY")

def get_customers():
    """
    Get the list of all customers from the LiteLLM API.
    
    Returns:
        list: List of customer objects
    """
    try:
        response = requests.get(
            f"{LITELLM_API_URI}/customer/list",
            headers={"Authorization": f"Bearer {LITELLM_MASTER_KEY}"}
        )

        if response.status_code == 200:
            response_json = response.json()
            if isinstance(response_json, list):
                return response_json
            else:
                raise Exception(f"Unexpected response format: {response_json}")
        else:
            raise Exception(f"Failed to get customers. Status code: {response.status_code}. Response: {response.text}")
    except Exception as e:
        raise Exception(f"Error getting customers: {e}")

def update_customer_budget(user_id, budget_id):
    """
    Update a customer's budget using the /customer/update endpoint.
    
    Args:
        user_id (str): The customer's user ID
        budget_id (str): The budget ID to assign
    
    Returns:
        dict: Response from the API
    """
    try:
        payload = {
            "user_id": user_id,
            "budget_id": budget_id
        }
        
        response = requests.post(
            f"{LITELLM_API_URI}/customer/update",
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {LITELLM_MASTER_KEY}"
            },
            data=json.dumps(payload)
        )
        
        if response.status_code == 200:
            print(f"Successfully updated budget for customer {user_id} with budget_id: {budget_id}")
            return response.json()
        else:
            raise Exception(f"Failed to update customer budget. Status code: {response.status_code}. Response: {response.text}")
    except Exception as e:
        raise Exception(f"Error updating customer budget for {user_id}: {e}")

def process_customers_without_budget():
    """
    Process all customers and add budgets for those without litellm_budget_table.
    """
    try:
        customers = get_customers()
        print(f"Found {len(customers)} customers")
        
        customers_without_budget = []
        customers_updated = 0
        
        for customer in customers:
            user_id = customer.get("user_id")
            litellm_budget_table = customer.get("litellm_budget_table")
            
            if not user_id:
                print(f"Warning: Customer missing user_id: {customer}")
                continue
                
            if litellm_budget_table is None:
                customers_without_budget.append(user_id)
                print(f"Customer {user_id} has no budget table. Adding OpenWebUI budget...")
                
                try:
                    update_customer_budget(user_id, "OpenWebUI")
                    customers_updated += 1
                except Exception as e:
                    print(f"Failed to update customer {user_id}: {e}")
                    continue
            else:
                print(f"Customer {user_id} already has budget table: {litellm_budget_table}")
        
        print(f"\nSummary:")
        print(f"- Total customers: {len(customers)}")
        print(f"- Customers without budget: {len(customers_without_budget)}")
        print(f"- Customers updated successfully: {customers_updated}")
        
        if customers_without_budget:
            print(f"- Customers that needed budget updates: {customers_without_budget}")
            
    except Exception as e:
        raise Exception(f"Error processing customers: {e}")

if __name__ == "__main__":
    try:
        print("Starting customer budget management...")
        process_customers_without_budget()
        print("Customer budget management completed successfully.")
        
    except Exception as e:
        print(f"Error: {e}")
        traceback.print_exc()
        exit(1)
