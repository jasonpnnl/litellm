# These are required
export AWS_PROFILE=AdministratorAccess-019116610105
export AWS_REGION=us-east-1
aws sso login
# These are needed if not set in .claude/settings.json
export CLAUDE_CODE_AWS_PROFILE=AdministratorAccess-019116610105
export ANTHROPIC_MODEL='us.anthropic.claude-sonnet-4-20250514-v1:0'
export CLAUDE_CODE_USE_BEDROCK=1
export CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC=1

