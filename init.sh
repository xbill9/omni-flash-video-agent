#!/bin/bash

# --- Function for error handling ---
handle_error() {
  echo "Error: $1"
  exit 1
}

# --- Part 1: Set Google Cloud Project ID ---



PROJECT_FILE="$HOME/project_id.txt"

echo "--- Setting Google Cloud Project ID File ---"

if [[ -f "$PROJECT_FILE" ]]; then
  user_project_id=$(cat "$PROJECT_FILE")
  echo "Using existing project ID from $PROJECT_FILE: $user_project_id"
else
  read -p "Please enter your Google Cloud project ID: " user_project_id

  if [[ -z "$user_project_id" ]]; then
    handle_error "No project ID was entered."
  fi

  echo "You entered: $user_project_id"
  echo "$user_project_id" > "$PROJECT_FILE"

  if [[ $? -ne 0 ]]; then
    handle_error "Failed saving your project ID: $user_project_id."
  fi
fi


# --- Part 1b: Set Gemini API Key ---

echo "--- Setting Gemini API Key ---"
GEMINI_KEY_FILE="$HOME/gemini.key"

if [[ -f "$GEMINI_KEY_FILE" ]]; then
  export GEMINI_API_KEY=$(cat "$GEMINI_KEY_FILE")
  echo "Using existing Gemini API key from $GEMINI_KEY_FILE"
else
  read -sp "Please enter your Gemini API key: " user_gemini_key
  echo ""

  if [[ -z "$user_gemini_key" ]]; then
    echo "Warning: No Gemini API key was entered. GEMINI_API_KEY not set."
  else
    export GEMINI_API_KEY="$user_gemini_key"
    echo "$user_gemini_key" > "$GEMINI_KEY_FILE"
    if [[ $? -eq 0 ]]; then
      echo "Gemini API key saved to $GEMINI_KEY_FILE"
    else
      echo "Warning: Failed saving your Gemini API key to $GEMINI_KEY_FILE."
    fi
  fi
fi



  if  [[ -z "$CLOUD_SHELL" ]] && curl -s -i metadata.google.internal | grep -q "Metadata-Flavor: Google"; then
     echo "This VM is running on GCP Defaults to Service Account."
  fi 

if [ "$CLOUD_SHELL" = "true" ]; then
  echo "Running in Google Cloud Shell."
else
  if curl -s -i metadata.google.internal | grep -q "Metadata-Flavor: Google"; then
     echo "This VM is running on Google Cloud."
  else
    echo "Not running in Google Cloud VM or Shell."
    # Check if application_default_credentials.json exists
    if [ -f "$HOME/.config/gcloud/application_default_credentials.json" ]; then
      echo "ADC Credentials already set up. Skipping login."
    else
      echo "Setting ADC Credentials"
      gcloud auth application-default login
    fi
  fi
fi

if [ -n "$FIREBASE_DEPLOY_AGENT" ]; then
echo "Running in Firebase Studio terminal"
else
echo "Not running in Firebase Studio terminal"
fi

if [ -d "/mnt/chromeos" ] ; then
     echo "Running on ChromeOS"
else
      echo "Not running on ChromeOS"
fi

export ID_TOKEN=$(gcloud auth print-identity-token)

echo "--- Initial Setup complete ---"

