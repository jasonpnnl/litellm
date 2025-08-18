function ccv() {
  local env_vars=(
    "AWS_PROFILE=AdministratorAccess-019116610105"
    "AWS_REGION=us-east-1"
    "ENABLE_BACKGROUND_TASKS=true"
    "FORCE_AUTO_BACKGROUND_TASKS=true"
  )
  
  env "${env_vars[@]}" aws sso login
  
  local claude_args=()
  
  if [[ "$1" == "-y" ]]; then
    claude_args+=("--dangerously-skip-permissions")
  elif [[ "$1" == "-r" ]]; then
    claude_args+=("--resume")
  elif [[ "$1" == "-ry" ]] || [[ "$1" == "-yr" ]]; then
    claude_args+=("--resume" "--dangerously-skip-permissions")
  fi
  
  env "${env_vars[@]}" claude "${claude_args[@]}"
}
