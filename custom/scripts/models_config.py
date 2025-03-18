from custom.scripts.utils import require_env_var

models = [
    {
        "model_name": "o3-mini-project",
        "litellm_params": {
            "model": "azure/o3-mini", # note the model name starts with "us." because this model requires using an inference profile
            "api_base": require_env_var("PROJECT_AZURE_API_BASE"),
            "api_key": require_env_var("PROJECT_AZURE_API_KEY"),
            "api_version": "2024-12-01-preview",
            "input_cost_per_token": 0.00000121,
            "output_cost_per_token": 0.00000484
        }
    },
    {
        "model_name": "o3-mini-birthright",
        "litellm_params": {
            "model": "azure/o3-mini",
            "api_base": require_env_var("BIRTHRIGHT_AZURE_API_BASE"),
            "api_key": require_env_var("BIRTHRIGHT_AZURE_API_KEY"),
            "api_version": "2024-12-01-preview",
            "input_cost_per_token": 0.00000121,
            "output_cost_per_token": 0.00000484
        }
    },
    {
        "model_name": "claude-3-7-sonnet-20250219-v1-openwebui",
        "litellm_params": {
            "model": "us.anthropic.claude-3-7-sonnet-20250219-v1:0", # note the model name starts with "us." because this model requires using an inference profile
            "aws_access_key_id": require_env_var("BEDROCK_AWS_ACCESS_KEY_ID"),
            "aws_secret_access_key": require_env_var("BEDROCK_AWS_SECRET_ACCESS_KEY"),
            "aws_region_name": "us-west-2"
        }
    },
    {
        "model_name": "claude-3-7-sonnet-20250219-v1-project",
        "litellm_params": {
            "model": "us.anthropic.claude-3-7-sonnet-20250219-v1:0",
            "aws_access_key_id": require_env_var("PROJECT_AWS_ACCESS_KEY_ID"),
            "aws_secret_access_key": require_env_var("PROJECT_AWS_SECRET_ACCESS_KEY"),
            "aws_region_name": "us-west-2"
        }
    },
    {
        "model_name": "claude-3-7-sonnet-20250219-v1-birthright",
        "litellm_params": {
            "model": "us.anthropic.claude-3-7-sonnet-20250219-v1:0",
            "aws_access_key_id": require_env_var("BIRTHRIGHT_AWS_ACCESS_KEY_ID"),
            "aws_secret_access_key": require_env_var("BIRTHRIGHT_AWS_SECRET_ACCESS_KEY"),
            "aws_region_name": "us-west-2"
        }
    },
    {
        "model_name": "claude-3-5-sonnet-20241022-v2-openwebui",
        "litellm_params": {
            "model": "anthropic.claude-3-5-sonnet-20241022-v2:0",
            "aws_access_key_id": require_env_var("BEDROCK_AWS_ACCESS_KEY_ID"),
            "aws_secret_access_key": require_env_var("BEDROCK_AWS_SECRET_ACCESS_KEY"),
            "aws_region_name": "us-west-2"
        }
    },
    {
        "model_name": "claude-3-5-haiku-20241022-openwebui",
        "litellm_params": {
            "model": "anthropic.claude-3-5-haiku-20241022-v1:0",
            "aws_access_key_id": require_env_var("BEDROCK_AWS_ACCESS_KEY_ID"),
            "aws_secret_access_key": require_env_var("BEDROCK_AWS_SECRET_ACCESS_KEY"),
            "aws_region_name": "us-west-2"
        }
    },
    {
        "model_name": "claude-3-sonnet-20240229-openwebui",
        "litellm_params": {
            "model": "anthropic.claude-3-sonnet-20240229-v1:0",
            "aws_access_key_id": require_env_var("BEDROCK_AWS_ACCESS_KEY_ID"),
            "aws_secret_access_key": require_env_var("BEDROCK_AWS_SECRET_ACCESS_KEY"),
            "aws_region_name": "us-west-2"
        }
    },
    {
        "model_name": "claude-3-5-sonnet-20241022-v2-project",
        "litellm_params": {
            "model": "anthropic.claude-3-5-sonnet-20241022-v2:0",
            "aws_access_key_id": require_env_var("PROJECT_AWS_ACCESS_KEY_ID"),
            "aws_secret_access_key": require_env_var("PROJECT_AWS_SECRET_ACCESS_KEY"),
            "aws_region_name": "us-west-2"
        }
    },
    {
        "model_name": "claude-3-5-haiku-20241022-project",
        "litellm_params": {
            "model": "anthropic.claude-3-5-haiku-20241022-v1:0",
            "aws_access_key_id": require_env_var("PROJECT_AWS_ACCESS_KEY_ID"),
            "aws_secret_access_key": require_env_var("PROJECT_AWS_SECRET_ACCESS_KEY"),
            "aws_region_name": "us-west-2"
        }
    },
    {
        "model_name": "claude-3-5-sonnet-20241022-v2-birthright",
        "litellm_params": {
            "model": "anthropic.claude-3-5-sonnet-20241022-v2:0",
            "aws_access_key_id": require_env_var("BIRTHRIGHT_AWS_ACCESS_KEY_ID"),
            "aws_secret_access_key": require_env_var("BIRTHRIGHT_AWS_SECRET_ACCESS_KEY"),
            "aws_region_name": "us-west-2"
        }
    },
    {
        "model_name": "claude-3-5-haiku-20241022-birthright",
        "litellm_params": {
            "model": "anthropic.claude-3-5-haiku-20241022-v1:0",
            "aws_access_key_id": require_env_var("BIRTHRIGHT_AWS_ACCESS_KEY_ID"),
            "aws_secret_access_key": require_env_var("BIRTHRIGHT_AWS_SECRET_ACCESS_KEY"),
            "aws_region_name": "us-west-2"
        }
    }
]