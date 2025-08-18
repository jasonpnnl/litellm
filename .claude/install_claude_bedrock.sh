npm install -g @anthropic-ai/claude-code
mkdir -p ~/.aws
cp .claude/config ~/.aws/
cd ~
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install

# Add sourcing of the launch_claude_bedrock function to .bashrc
if ! grep -q "source .claude/launch_claude_bedrock.sh" ~/.bashrc; then
    echo "" >> ~/.bashrc
    echo "# Source Claude Bedrock launch function" >> ~/.bashrc
    echo "if [ -f .claude/launch_claude_bedrock.sh ]; then" >> ~/.bashrc
    echo "    source .claude/launch_claude_bedrock.sh" >> ~/.bashrc
    echo "fi" >> ~/.bashrc
    echo "Added Claude Bedrock function sourcing to .bashrc"
else
    echo "Claude Bedrock function sourcing already exists in .bashrc"
fi
