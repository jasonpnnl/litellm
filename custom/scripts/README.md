# LiteLLM Model Management Script
The add_models.py script is used to add models to LiteLLM in GitLab CI.

## Usage
**Model Configuration:**
Define new models in models_config.py with required parameters. Refer to [LiteLLM's documentation](https://docs.litellm.ai/docs/proxy/model_management#add-a-new-model) for details.

**Environment Variables:**
See .env.example for required environment variables.
- Set `LITELLM_API_URI` to the correct LiteLLM endpoint (e.g., for local: https://ai-incubator-dev-api.pnnl.gov)
- Use `LITELLM_MASTER_KEY` for the appropriate environment. should be able to retrieve this from CI variables or the LiteLLM config. 
- Bedrock models use AWS access keys. Use the `gitlab-ci` user in AWS account `019116610105` with `AmazonBedrockFullAccess` permissions.

**Local Setup:**

When running locally, define a `.env` file in the `custom/scripts` directory with required environment variables. You can grab the secret values from GitLab CI.

e.g.
```
BEDROCK_AWS_ACCESS_KEY_ID=
BEDROCK_AWS_SECRET_ACCESS_KEY=
LITELLM_API_URI=https://ai-incubator-dev-api.pnnl.gov
LITELLM_MASTER_KEY=
```