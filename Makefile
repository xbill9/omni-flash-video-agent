# Configuration - Update these or override via environment variables
PROJECT_ID ?= aisprint-491218
REGION ?= us-east4
ZONE ?= $(REGION)-a
BUCKET_NAME ?= $(PROJECT_ID)-bucket
SERVICE_NAME ?= gpu-12b-qat-l4-devops-agent
MODEL_PATH ?= gemma-4-12B-it-qat-w4a16-ct

install:
	pip install -r requirements.txt

run:
	python server.py

test:
	python test_agent.py

lint:
	ruff check .
	ruff format --check .
	mypy .

clean:
	rm -rf __pycache__
	find . -type d -name "__pycache__" -exec rm -rf {} +

# Recommended deployment settings for vLLM on GCP GCE with NVIDIA L4 GPU
deploy-vllm:
	@echo "🚀 Deploying vLLM to GCE instance ($(SERVICE_NAME)) in $(ZONE)..."
	@HF_TOKEN=$$(gcloud secrets versions access latest --secret=hf-token --project=$(PROJECT_ID) 2>/dev/null || echo ''); \
	echo '#!/bin/bash' > startup_script.sh; \
	echo 'if ! command -v docker &> /dev/null; then' >> startup_script.sh; \
	echo '    apt-get update -y && apt-get install -y docker.io' >> startup_script.sh; \
	echo '    systemctl start docker && systemctl enable docker' >> startup_script.sh; \
	echo 'fi' >> startup_script.sh; \
	echo 'docker run -d --name vllm-server \\' >> startup_script.sh; \
	echo '  --gpus all \\' >> startup_script.sh; \
	echo '  --ipc=host \\' >> startup_script.sh; \
	echo '  --restart always \\' >> startup_script.sh; \
	echo '  -p 8080:8080 \\' >> startup_script.sh; \
	echo "  -e HF_TOKEN=\"$$HF_TOKEN\" \\" >> startup_script.sh; \
	echo '  vllm/vllm-openai:nightly \\' >> startup_script.sh; \
	echo '  --model google/$(MODEL_PATH) \\' >> startup_script.sh; \
	echo '  --quantization compressed-tensors \\' >> startup_script.sh; \
	echo '  --dtype bfloat16 \\' >> startup_script.sh; \
	echo '  --max-model-len 32768 \\' >> startup_script.sh; \
	echo '  --disable-chunked-mm-input \\' >> startup_script.sh; \
	echo '  --gpu-memory-utilization 0.95 \\' >> startup_script.sh; \
	echo '  --kv-cache-dtype fp8 \\' >> startup_script.sh; \
	echo '  --tensor-parallel-size 1 \\' >> startup_script.sh; \
	echo '  --max-num-seqs 8 \\' >> startup_script.sh; \
	echo '  --enable-chunked-prefill \\' >> startup_script.sh; \
	echo '  --max-num-batched-tokens 4096 \\' >> startup_script.sh; \
	echo '  --enable-auto-tool-choice \\' >> startup_script.sh; \
	echo '  --tool-call-parser gemma4 \\' >> startup_script.sh; \
	echo '  --reasoning-parser gemma4 \\' >> startup_script.sh; \
	echo '  --async-scheduling \\' >> startup_script.sh; \
	echo '  --limit-mm-per-prompt "{}" \\' >> startup_script.sh; \
	echo '  --host 0.0.0.0 \\' >> startup_script.sh; \
	echo '  --port 8080' >> startup_script.sh
	gcloud compute instances create $(SERVICE_NAME) \
		--project=$(PROJECT_ID) \
		--zone=$(ZONE) \
		--machine-type=g2-standard-4 \
		--accelerator=type=nvidia-l4,count=1 \
		--maintenance-policy=TERMINATE \
		--image-family=common-cu129-ubuntu-2204-nvidia-580 \
		--image-project=deeplearning-platform-release \
		--boot-disk-size=150GB \
		--boot-disk-type=pd-balanced \
		--metadata-from-file=startup-script=startup_script.sh \
		--tags=vllm-server
	-gcloud compute firewall-rules create allow-vllm-8080 \
		--project=$(PROJECT_ID) \
		--allow=tcp:8080 \
		--target-tags=vllm-server \
		--description="Allow port 8080 for vLLM"
	rm -f startup_script.sh

# Deploy the vLLM inference stack
deploy: deploy-vllm

# Destroy the vLLM inference stack
destroy-vllm:
	@echo "🗑️  Destroying GCE instance $(SERVICE_NAME) in $(ZONE)..."
	gcloud compute instances delete $(SERVICE_NAME) \
		--project=$(PROJECT_ID) \
		--zone=$(ZONE) \
		--quiet

destroy: destroy-vllm

# Check status of the GCE instance
status:
	@echo "🔍 Checking status of GCE instance $(SERVICE_NAME) in $(ZONE)..."
	gcloud compute instances describe $(SERVICE_NAME) \
		--project=$(PROJECT_ID) \
		--zone=$(ZONE)

# Get the endpoint URL of the deployed GCE instance
endpoint:
	@gcloud compute instances describe $(SERVICE_NAME) \
		--project=$(PROJECT_ID) \
		--zone=$(ZONE) \
		--format='value(networkInterfaces[0].accessConfigs[0].natIP)'

PROMPT ?= "What is Site Reliability Engineering?"

# Query the vLLM model via the GCE VM external IP
query:
	@echo "🔍 Querying $(SERVICE_NAME) with prompt: \"$(PROMPT)\"..."
	@IP=$$(gcloud compute instances describe $(SERVICE_NAME) --project=$(PROJECT_ID) --zone=$(ZONE) --format='value(networkInterfaces[0].accessConfigs[0].natIP)'); \
	curl -s -X POST "http://$$IP:8080/v1/completions" \
		-H "Content-Type: application/json" \
		-d '{"model": "google/$(MODEL_PATH)", "prompt": "$(PROMPT)", "max_tokens": 128, "temperature": 0.2}' | python3 -m json.tool

.PHONY: install run test clean deploy-vllm deploy destroy-vllm destroy status endpoint query
