import json
from custom.scripts.utils import require_env_var

_SA_FILE = require_env_var("GCP_SERVICE_ACCOUNT_JSON")
_PROJECT_SA_FILE = require_env_var("PROJECT_GCP_SERVICE_ACCOUNT_JSON")
_BIRTHRIGHT_SA_FILE = require_env_var("BIRTHRIGHT_GCP_SERVICE_ACCOUNT_JSON")

with open(_SA_FILE) as f:
    _SA_JSON = json.dumps(json.load(f))

with open(_PROJECT_SA_FILE) as f:
    _PROJECT_SA_JSON = json.dumps(json.load(f))

with open(_BIRTHRIGHT_SA_FILE) as f:
    _BIRTHRIGHT_SA_JSON = json.dumps(json.load(f))

models = [
    # OpenWebUI models - note that going forward, OpenWebUI models will have no suffix to simplify the import process
    # Claude models
    {
        "model_name": "claude-sonnet-4-20250514-v1",
        "litellm_params": {
            "model": "us.anthropic.claude-sonnet-4-20250514-v1:0", # note the model name starts with "us." because this model requires using an inference profile
            "aws_access_key_id": require_env_var("BEDROCK_AWS_ACCESS_KEY_ID"),
            "aws_secret_access_key": require_env_var("BEDROCK_AWS_SECRET_ACCESS_KEY"),
            "aws_region_name": "us-west-2"
        }
    },
    {
        "model_name": "claude-sonnet-4-20250514-v1",
        "litellm_params": {
            "model": "vertex_ai/claude-sonnet-4@20250514",
            "vertex_project": require_env_var("GCP_PROJECT"),
            "vertex_location": "us-east5",
            "vertex_credentials": _SA_JSON,
            "custom_llm_provider": "vertex_ai"
        },
    },
    {
        "model_name": "claude-sonnet-4-thinking-1024-20250514-v1",
        "litellm_params": {
            "model": "us.anthropic.claude-sonnet-4-20250514-v1:0",
            "aws_access_key_id": require_env_var("BEDROCK_AWS_ACCESS_KEY_ID"),
            "aws_secret_access_key": require_env_var("BEDROCK_AWS_SECRET_ACCESS_KEY"),
            "aws_region_name": "us-west-2",
            "thinking": {
                "type": "enabled",
                "budget_tokens": 1024
            },
            "merge_reasoning_content_in_choices": True
        }
    },
    {
        "model_name": "claude-sonnet-4-thinking-1024-20250514-v1",
        "litellm_params": {
            "model": "vertex_ai/claude-sonnet-4@20250514",
            "vertex_project": require_env_var("GCP_PROJECT"),
            "vertex_location": "us-east5",
            "vertex_credentials": _SA_JSON,
            "custom_llm_provider": "vertex_ai",
            "thinking": {
                "type": "enabled",
                "budget_tokens": 1024
            },
            "merge_reasoning_content_in_choices": True
        },
    },
    {
        "model_name": "claude-sonnet-4-thinking-16000-20250514-v1",
        "litellm_params": {
            "model": "us.anthropic.claude-sonnet-4-20250514-v1:0",
            "aws_access_key_id": require_env_var("BEDROCK_AWS_ACCESS_KEY_ID"),
            "aws_secret_access_key": require_env_var("BEDROCK_AWS_SECRET_ACCESS_KEY"),
            "aws_region_name": "us-west-2",
            "thinking": {
                "type": "enabled",
                "budget_tokens": 16000
            },
            "merge_reasoning_content_in_choices": True
        }
    },
    {
        "model_name": "claude-sonnet-4-thinking-16000-20250514-v1",
        "litellm_params": {
            "model": "vertex_ai/claude-sonnet-4@20250514",
            "vertex_project": require_env_var("GCP_PROJECT"),
            "vertex_location": "us-east5",
            "vertex_credentials": _SA_JSON,
            "custom_llm_provider": "vertex_ai",
            "thinking": {
                "type": "enabled",
                "budget_tokens": 16000
            },
            "merge_reasoning_content_in_choices": True
        }
    },
    {
        "model_name": "claude-opus-4-20250514-v1",
        "litellm_params": {
            "model": "us.anthropic.claude-opus-4-20250514-v1:0", # note the model name starts with "us." because this model requires using an inference profile
            "aws_access_key_id": require_env_var("BEDROCK_AWS_ACCESS_KEY_ID"),
            "aws_secret_access_key": require_env_var("BEDROCK_AWS_SECRET_ACCESS_KEY"),
            "aws_region_name": "us-west-2"
        }
    },
    {
        "model_name": "claude-opus-4-thinking-1024-20250514-v1",
        "litellm_params": {
            "model": "us.anthropic.claude-opus-4-20250514-v1:0",
            "aws_access_key_id": require_env_var("BEDROCK_AWS_ACCESS_KEY_ID"),
            "aws_secret_access_key": require_env_var("BEDROCK_AWS_SECRET_ACCESS_KEY"),
            "aws_region_name": "us-west-2",
            "thinking": {
                "type": "enabled",
                "budget_tokens": 1024
            },
            "merge_reasoning_content_in_choices": True
        }
    },
    {
        "model_name": "claude-opus-4-thinking-16000-20250514-v1",
        "litellm_params": {
            "model": "us.anthropic.claude-opus-4-20250514-v1:0",
            "aws_access_key_id": require_env_var("BEDROCK_AWS_ACCESS_KEY_ID"),
            "aws_secret_access_key": require_env_var("BEDROCK_AWS_SECRET_ACCESS_KEY"),
            "aws_region_name": "us-west-2",
            "thinking": {
                "type": "enabled",
                "budget_tokens": 16000
            },
            "merge_reasoning_content_in_choices": True
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
        "model_name": "claude-3-7-sonnet-thinking-1024-20250219-v1-openwebui",
        "litellm_params": {
            "model": "us.anthropic.claude-3-7-sonnet-20250219-v1:0",
            "aws_access_key_id": require_env_var("BEDROCK_AWS_ACCESS_KEY_ID"),
            "aws_secret_access_key": require_env_var("BEDROCK_AWS_SECRET_ACCESS_KEY"),
            "aws_region_name": "us-west-2",
            "thinking": {
                "type": "enabled",
                "budget_tokens": 1024
            },
            "merge_reasoning_content_in_choices": True
        }
    },
    {
        "model_name": "claude-3-7-sonnet-thinking-16000-20250219-v1-openwebui",
        "litellm_params": {
            "model": "us.anthropic.claude-3-7-sonnet-20250219-v1:0",
            "aws_access_key_id": require_env_var("BEDROCK_AWS_ACCESS_KEY_ID"),
            "aws_secret_access_key": require_env_var("BEDROCK_AWS_SECRET_ACCESS_KEY"),
            "aws_region_name": "us-west-2",
            "thinking": {
                "type": "enabled",
                "budget_tokens": 16000
            },
            "merge_reasoning_content_in_choices": True
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
    # Nova models
    {
        "model_name": "nova-pro-v1-openwebui",
        "litellm_params": {
            "model": "us.amazon.nova-pro-v1:0",
            "aws_access_key_id": require_env_var("BEDROCK_AWS_ACCESS_KEY_ID"),
            "aws_secret_access_key": require_env_var("BEDROCK_AWS_SECRET_ACCESS_KEY"),
            "aws_region_name": "us-west-2"
        }
    },
    {
        "model_name": "nova-lite-v1-openwebui",
        "litellm_params": {
            "model": "us.amazon.nova-lite-v1:0",
            "aws_access_key_id": require_env_var("BEDROCK_AWS_ACCESS_KEY_ID"),
            "aws_secret_access_key": require_env_var("BEDROCK_AWS_SECRET_ACCESS_KEY"),
            "aws_region_name": "us-west-2"
        }
    },
    {
        "model_name": "nova-micro-v1-openwebui",
        "litellm_params": {
            "model": "us.amazon.nova-micro-v1:0",
            "aws_access_key_id": require_env_var("BEDROCK_AWS_ACCESS_KEY_ID"),
            "aws_secret_access_key": require_env_var("BEDROCK_AWS_SECRET_ACCESS_KEY"),
            "aws_region_name": "us-west-2"
        }
    },
    # OpenAI models
    {
        "model_name": "whisper-openwebui",
        "litellm_params": {
            "model": "azure/whisper",
            "api_base": require_env_var("AZURE_OPENAI_API_BASE"),
            "api_key": require_env_var("AZURE_OPENAI_API_KEY"),
            "api_version": "2025-04-01-preview"
        },
        "model_info": {
            "base_model": "azure/whisper-1"
        }
    },
    {
        "model_name": "text-embedding-3-large-openwebui",
        "litellm_params": {
            "model": "azure/text-embedding-3-large",
            "api_base": require_env_var("AZURE_OPENAI3_API_BASE"),
            "api_key": require_env_var("AZURE_OPENAI3_API_KEY"),
            "api_version": "2025-04-01-preview"
        },
        "model_info": {
            "base_model": "azure/text-embedding-3-large"
        }
    },
    {
        "model_name": "dall-e-3-openwebui",
        "litellm_params": {
            "model": "azure/dall-e-3",
            "api_base": require_env_var("AZURE_OPENAI2_API_BASE"),
            "api_key": require_env_var("AZURE_OPENAI2_API_KEY"),
            "api_version": "2025-04-01-preview"
        },
        "model_info": {
            "base_model": "azure/dall-e-3"
        }
    },
    {
        "model_name": "gpt-4o-mini-openwebui",
        "litellm_params": {
            "model": "azure/gpt-4o-mini",
            "api_base": require_env_var("AZURE_OPENAI3_API_BASE"),
            "api_key": require_env_var("AZURE_OPENAI3_API_KEY"),
            "api_version": "2025-04-01-preview"
        },
        "model_info": {
            "base_model": "azure/us/gpt-4o-mini-2024-07-18",
        }
    },
    {
        "model_name": "gpt-4o",
        "litellm_params": {
            "model": "azure/gpt-4o",
            "api_base": require_env_var("AZURE_OPENAI3_API_BASE"),
            "api_key": require_env_var("AZURE_OPENAI3_API_KEY"),
            "api_version": "2025-04-01-preview"
        },
        "model_info": {
            "base_model": "azure/us/gpt-4o-2024-11-20",
        }
    },
    {
        "model_name": "o3",
        "litellm_params": {
            "model": "azure/o3",
            "api_base": require_env_var("AZURE_OPENAI3_API_BASE"),
            "api_key": require_env_var("AZURE_OPENAI3_API_KEY"),
            "api_version": "2025-04-01-preview",
        },
        "model_info": {
            "base_model": "azure/o3",
        }
    },
    {
        "model_name": "o4-mini",
        "litellm_params": {
            "model": "azure/o4-mini",
            "api_base": require_env_var("AZURE_OPENAI3_API_BASE"),
            "api_key": require_env_var("AZURE_OPENAI3_API_KEY"),
            "api_version": "2025-04-01-preview",
        },
        "model_info": {
            "base_model": "azure/o4-mini-2025-04-16",
        }
    },
    {
        "model_name": "gpt-4.1-openwebui",
        "litellm_params": {
            "model": "azure/gpt-4.1",
            "api_base": require_env_var("AZURE_OPENAI3_API_BASE"),
            "api_key": require_env_var("AZURE_OPENAI3_API_KEY"),
            "api_version": "2025-04-01-preview"
        },
        "model_info": {
            "base_model": "azure/gpt-4.1-2025-04-14",
        }
    },
    # Gemini models
    {
        "model_name": "gemini-2.0-flash-001",
        "litellm_params": {
            "model": "gemini-2.0-flash-001",
            "vertex_project": require_env_var("GCP_PROJECT"),
            "vertex_location": "us-west1",
            "vertex_credentials": _SA_JSON,
            "custom_llm_provider": "vertex_ai"
        },
    },
    {
        "model_name": "gemini-2.5-pro",
        "litellm_params": {
            "model": "gemini-2.5-pro",
            "vertex_project": require_env_var("GCP_PROJECT"),
            "vertex_location": "us-central1",
            "vertex_credentials": _SA_JSON,
            "custom_llm_provider": "vertex_ai"
        }
    },
    {
        "model_name": "gemini-2.5-flash",
        "litellm_params": {
            "model": "gemini-2.5-flash",
            "vertex_project": require_env_var("GCP_PROJECT"),
            "vertex_location": "us-central1",
            "vertex_credentials": _SA_JSON,
            "custom_llm_provider": "vertex_ai"
        }
    },
    {
        "model_name": "gemini-2.5-pro-birthright",
        "litellm_params": {
            "model": "gemini-2.5-pro",
            "vertex_project": require_env_var("BIRTHRIGHT_GCP_PROJECT"),
            "vertex_location": "us-central1",
            "vertex_credentials": _BIRTHRIGHT_SA_JSON,
            "custom_llm_provider": "vertex_ai"
        }
    },
    {
        "model_name": "gemini-2.5-pro-project",
        "litellm_params": {
            "model": "gemini-2.5-pro",
            "vertex_project": require_env_var("PROJECT_GCP_PROJECT"),
            "vertex_location": "us-central1",
            "vertex_credentials": _PROJECT_SA_JSON,
            "custom_llm_provider": "vertex_ai"
        }
    },
    # Azure Foundry Models
    {
        "model_name": "grok-3",
        "litellm_params": {
            "model": "azure_ai/grok-3",
            "api_base": require_env_var("AZURE_AI_FOUNDRY_API_BASE"),
            "api_key": require_env_var("AZURE_AI_FOUNDRY_API_KEY")
        },
        "model_info": {
            "base_model": "azure_ai/grok-3"
        }
    },
    # Project models - project models have the -project suffix to differentiate them from OpenWebUI models and birthright models have the -birthright suffix
    # OpenAI models
    {
        "model_name": "gpt-4o-project",
        "litellm_params": {
            "model": "azure/gpt-4o",
            "api_base": require_env_var("PROJECT_AZURE_API_BASE"),
            "api_key": require_env_var("PROJECT_AZURE_API_KEY"),
            "api_version": "2025-04-01-preview"
        },
        "model_info": {
            "base_model": "azure/gpt-4o-2024-08-06",
        }
    },
    {
        "model_name": "gpt-4o-birthright",
        "litellm_params": {
            "model": "azure/gpt-4o",
            "api_base": require_env_var("BIRTHRIGHT_AZURE_API_BASE"),
            "api_key": require_env_var("BIRTHRIGHT_AZURE_API_KEY"),
            "api_version": "2025-04-01-preview"
        },
        "model_info": {
            "base_model": "azure/gpt-4o-2024-08-06",
        }   
    },
    {
        "model_name": "text-embedding-3-small-project",
        "litellm_params": {
            "model": "azure/text-embedding-3-small",
            "api_base": require_env_var("PROJECT_AZURE_API_BASE"),
            "api_key": require_env_var("PROJECT_AZURE_API_KEY"),
            "api_version": "2025-04-01-preview"
        },
        "model_info": {
            "base_model": "azure/text-embedding-3-small"
        }
    },
    {
        "model_name": "text-embedding-3-small-birthright",
        "litellm_params": {
            "model": "azure/text-embedding-3-small",
            "api_base": require_env_var("BIRTHRIGHT_AZURE_API_BASE"),
            "api_key": require_env_var("BIRTHRIGHT_AZURE_API_KEY"),
            "api_version": "2025-04-01-preview"
        },
        "model_info": {
            "base_model": "azure/text-embedding-3-small"
        }
    },
    {
        "model_name": "o3-project",
        "litellm_params": {
            "model": "azure/o3",
            "api_base": require_env_var("PROJECT_AZURE_API_BASE"),
            "api_key": require_env_var("PROJECT_AZURE_API_KEY"),
            "api_version": "2025-04-01-preview",
        },
        "model_info": {
            "base_model": "azure/o3",
        }
    },
    {
        "model_name": "o3-birthright",
        "litellm_params": {
            "model": "azure/o3",
            "api_base": require_env_var("BIRTHRIGHT_AZURE_API_BASE"),
            "api_key": require_env_var("BIRTHRIGHT_AZURE_API_KEY"),
            "api_version": "2025-04-01-preview",
        },
        "model_info": {
            "base_model": "azure/o3",
        }
    },
    {
        "model_name": "o3-mini-project",
        "litellm_params": {
            "model": "azure/o3-mini",
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
        "model_name": "o4-mini-project",
        "litellm_params": {
            "model": "azure/o4-mini",
            "api_base": require_env_var("PROJECT_AZURE_API_BASE"),
            "api_key": require_env_var("PROJECT_AZURE_API_KEY"),
            "api_version": "2025-04-01-preview",
        },
        "model_info": {
            "base_model": "azure/o4-mini-2025-04-16",
        }
    },
    {
        "model_name": "o4-mini-birthright",
        "litellm_params": {
            "model": "azure/o4-mini",
            "api_base": require_env_var("BIRTHRIGHT_AZURE_API_BASE"),
            "api_key": require_env_var("BIRTHRIGHT_AZURE_API_KEY"),
            "api_version": "2025-04-01-preview",
        },
        "model_info": {
            "base_model": "azure/o4-mini-2025-04-16",
        }
    },
    # Claude models
    {
        "model_name": "claude-sonnet-4-20250514-v1-project",
        "litellm_params": {
            "model": "us.anthropic.claude-sonnet-4-20250514-v1:0",
            "aws_access_key_id": require_env_var("PROJECT_AWS_ACCESS_KEY_ID"),
            "aws_secret_access_key": require_env_var("PROJECT_AWS_SECRET_ACCESS_KEY"),
            "aws_region_name": "us-west-1"
        }
    },
    {
        "model_name": "claude-sonnet-4-20250514-v1-project",
        "litellm_params": {
            "model": "us.anthropic.claude-sonnet-4-20250514-v1:0",
            "aws_access_key_id": require_env_var("PROJECT_AWS_ACCESS_KEY_ID"),
            "aws_secret_access_key": require_env_var("PROJECT_AWS_SECRET_ACCESS_KEY"),
            "aws_region_name": "us-west-2"
        }
    },
    {
        "model_name": "claude-sonnet-4-20250514-v1-project",
        "litellm_params": {
            "model": "us.anthropic.claude-sonnet-4-20250514-v1:0",
            "aws_access_key_id": require_env_var("PROJECT_AWS_ACCESS_KEY_ID"),
            "aws_secret_access_key": require_env_var("PROJECT_AWS_SECRET_ACCESS_KEY"),
            "aws_region_name": "us-east-1"
        }
    },
    {
        "model_name": "claude-sonnet-4-20250514-v1-project",
        "litellm_params": {
            "model": "us.anthropic.claude-sonnet-4-20250514-v1:0",
            "aws_access_key_id": require_env_var("PROJECT_AWS_ACCESS_KEY_ID"),
            "aws_secret_access_key": require_env_var("PROJECT_AWS_SECRET_ACCESS_KEY"),
            "aws_region_name": "us-east-2"
        }
    },
    {
        "model_name": "claude-sonnet-4-20250514-v1-birthright",
        "litellm_params": {
            "model": "us.anthropic.claude-sonnet-4-20250514-v1:0",
            "aws_access_key_id": require_env_var("BIRTHRIGHT_AWS_ACCESS_KEY_ID"),
            "aws_secret_access_key": require_env_var("BIRTHRIGHT_AWS_SECRET_ACCESS_KEY"),
            "aws_region_name": "us-west-2"
        }
    },
    {
        "model_name": "claude-opus-4-20250514-v1-project",
        "litellm_params": {
            "model": "us.anthropic.claude-opus-4-20250514-v1:0",
            "aws_access_key_id": require_env_var("PROJECT_AWS_ACCESS_KEY_ID"),
            "aws_secret_access_key": require_env_var("PROJECT_AWS_SECRET_ACCESS_KEY"),
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