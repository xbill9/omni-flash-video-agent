#!/bin/bash

# Check if the key file exists
if [ -f "$HOME/gemini.key" ]; then
    GEMINI_API_KEY=$(cat "$HOME/gemini.key")
else
    read -r -p "Enter Gemini KEY: " GEMINI_API_KEY
    echo "$GEMINI_API_KEY" > "$HOME/gemini.key"
fi

# Export GEMINI_API_KEY as primary, and GOOGLE_API_KEY for backward compatibility
export GEMINI_API_KEY
export GOOGLE_API_KEY="$GEMINI_API_KEY"

echo "✅ Environment variables GEMINI_API_KEY and GOOGLE_API_KEY successfully exported."

# Update .agents/mcp_config.json with the absolute path based on the current directory
CURRENT_DIR=$(pwd)
CONFIG_FILE="$CURRENT_DIR/.agents/mcp_config.json"

if [ -f "$CONFIG_FILE" ]; then
    python3 -c "
import json, sys, os
with open('$CONFIG_FILE', 'r') as f:
    data = json.load(f)
if 'mcpServers' in data and 'omni-video-agent' in data['mcpServers']:
    server = data['mcpServers']['omni-video-agent']
    server['args'] = ['$CURRENT_DIR/server.py']
    if 'env' not in server:
        server['env'] = {}
    server['env']['GEMINI_API_KEY'] = os.environ.get('GEMINI_API_KEY', '')
    server['env']['GOOGLE_API_KEY'] = os.environ.get('GOOGLE_API_KEY', '')
with open('$CONFIG_FILE', 'w') as f:
    json.dump(data, f, indent=2)
"
    echo "✅ Updated $CONFIG_FILE with the path and env keys."
else
    echo "⚠️  Could not find $CONFIG_FILE to update."
fi
