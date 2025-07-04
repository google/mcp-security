# Makefile for ADK Runbooks project
#

# Environment file is now loaded by the env_manager.py script

# Python executable (use activated venv if available)
PYTHON := python3

# Multi-agent directory
MULTIAGENT_DIR := multi-agent

# Cookiecutter directories
COOKIECUTTER_TEMPLATE := cookiecutter-adk-agent
COOKIECUTTER_BUILDER := cookiecutter-agent-builder

# Agent management script
MANAGE_AGENTS := $(PYTHON) scripts/manage_agents.py

# Environment management script
ENV_FILE_PATH := agents/google_mcp_security_agent/.env
ENV_MANAGER := $(PYTHON) scripts/env_manager.py

.PHONY: help env-setup env-check env-update config-show oauth-client oauth-uri oauth-link oauth-verify oauth-setup docs agents-list agents-delete multi-agent-setup multi-agent-run multi-agent-web cookiecutter-setup cookiecutter-run cookiecutter-new-agent adk-deploy adk-redeploy agentspace-register agentspace-update agentspace-verify agentspace-delete agentspace-url cloudrun-deploy cloudrun-run cloudrun-test cloudrun-logs cloudrun-url cloudrun-delete gcloud-proxy test-agent

# Put it first so that "make" without argument is like "make help".
help:
	@echo "Available targets:"
	@echo ""
	@echo "Environment Management:"
	@echo "  env-setup       - Create .env from .env.sample"
	@echo "  env-check       - Validate required environment variables"
	@echo "  config-show     - Display current configuration (masks secrets)"
	@echo "  env-update      - Update environment variable"
	@echo ""
	@echo "OAuth Management:"
	@echo "  oauth-client    - Guide for creating OAuth client"
	@echo "  oauth-uri       - Generate OAuth authorization URI"
	@echo "  oauth-link      - Link OAuth to AgentSpace"
	@echo "  oauth-verify    - Verify OAuth configuration"
	@echo "  oauth-setup     - Complete OAuth setup workflow"
	@echo ""
	@echo "Agent Management:"
	@echo "  agents-list     - List all deployed Agent Engine instances"
	@echo "  agents-delete   - Delete Agent Engine instance by index"
	@echo "  adk-deploy      - Deploy agent to Agent Engine"
	@echo "  adk-redeploy    - Redeploy agent to existing Agent Engine resource"
	@echo "  test-agent      - Test deployed agent with a message"
	@echo ""
	@echo "AgentSpace Integration:"
	@echo "  agentspace-register - Register agent with AgentSpace"
	@echo "  agentspace-update   - Update existing AgentSpace registration"
	@echo "  agentspace-verify   - Verify AgentSpace integration"
	@echo "  agentspace-delete   - Remove agent from AgentSpace"
	@echo "  agentspace-url      - Get AgentSpace UI URL"
	@echo ""
	@echo "Cloud Run Deployment:"
	@echo "  cloudrun-deploy - Deploy agent to Cloud Run"
	@echo "  cloudrun-run    - Run Cloud Run service locally"
	@echo "  cloudrun-test   - Test deployed Cloud Run service"
	@echo "  cloudrun-logs   - View Cloud Run service logs"
	@echo "  cloudrun-url    - Get Cloud Run service URL"
	@echo "  cloudrun-delete - Delete Cloud Run service"
	@echo ""
	@echo "Development Tools:"
	@echo "  docs            - Build documentation"
	@echo "  gcloud-proxy    - Proxy to Cloud Run service locally"
	@echo ""
	@echo "Multi-Agent System:"
	@echo "  multi-agent-setup - Set up multi-agent environment"
	@echo "  multi-agent-run - Run the manager agent"
	@echo "  multi-agent-web - Run the multi-agent web UI"
	@echo ""
	@echo "Agent Templates:"
	@echo "  cookiecutter-setup - Set up cookiecutter agent builder"
	@echo "  cookiecutter-run - Run the cookiecutter web builder"
	@echo "  cookiecutter-new-agent - Create new agent from template"
	@echo ""
	@echo "Environment variables from .env will be automatically loaded."
	@echo ""
	@echo "Examples:"
	@echo "  make env-check"
	@echo "  make config-show"
	@echo "  make env-update KEY=GOOGLE_CLOUD_PROJECT VALUE=my-project"
	@echo "  make oauth-setup"
	@echo "  make agents-list"
	@echo "  make adk-deploy AGENT_DIR=. DISPLAY_NAME='Security Agent'"
	@echo "  make test-agent MSG='List security tools'"
	@echo "  make agentspace-register"
	@echo "  make agentspace-verify"
	@echo "  make agentspace-url"

# Environment Management targets
env-setup:
	@echo "Creating .env file from example..."
	@if [ -f "agents/google_mcp_security_agent/.env.example" ]; then \
		cp agents/google_mcp_security_agent/.env.example agents/google_mcp_security_agent/.env; \
		echo "✓ .env file created successfully."; \
		echo "Please review and update the values in agents/google_mcp_security_agent/.env"; \
	else \
		echo "Error: agents/google_mcp_security_agent/.env.example not found."; \
		exit 1; \
	fi

env-check:
	@echo "Checking environment configuration..."
	@$(ENV_MANAGER) check --env-file $(ENV_FILE_PATH) --deployment $(or $(DEPLOYMENT),base)


config-show:
	@$(ENV_MANAGER) show --env-file $(ENV_FILE_PATH) $(if $(ALL),--all)

env-update:
ifndef KEY
	@echo "Error: KEY parameter required. Usage: make env-update KEY=VAR_NAME VALUE=var_value"
	@exit 1
endif
ifndef VALUE
	@echo "Error: VALUE parameter required. Usage: make env-update KEY=VAR_NAME VALUE=var_value"
	@exit 1
endif
	@$(ENV_MANAGER) update --env-file $(ENV_FILE_PATH) --key $(KEY) --value "$(VALUE)"

# Validate environment for specific deployment types
env-validate-agent-engine:
	@$(ENV_MANAGER) check --env-file $(ENV_FILE_PATH) --deployment agent_engine

env-validate-agentspace:
	@$(ENV_MANAGER) check --env-file $(ENV_FILE_PATH) --deployment agentspace

env-validate-oauth:
	@$(ENV_MANAGER) check --env-file $(ENV_FILE_PATH) --deployment oauth

# OAuth Management targets
OAUTH_MANAGER := $(PYTHON) scripts/oauth_manager.py --env-file agents/google_mcp_security_agent/.env

oauth-client:
	@echo "Starting OAuth client creation guide..."
	@$(OAUTH_MANAGER) guide

oauth-uri:
	@echo "Generating OAuth authorization URI..."
	@$(OAUTH_MANAGER) generate $(if $(CLIENT_SECRET),--client-secret $(CLIENT_SECRET))

oauth-link: env-validate-oauth
	@echo "Linking OAuth to AgentSpace..."
	@$(OAUTH_MANAGER) link

oauth-verify:
	@echo "Verifying OAuth configuration..."
	@$(OAUTH_MANAGER) verify

oauth-setup: oauth-client
	@echo ""
	@echo "OAuth Setup Workflow:"
	@echo "1. Follow the guide above to create an OAuth client"
	@echo "2. Download client_secret.json to this directory"
	@echo "3. Run: make oauth-uri"
	@echo "4. Open the generated URL and authorize"
	@echo "5. Run: make oauth-link"

# Documentation targets
docs:
	@echo "Building Sphinx documentation..."
	@cd rules-bank && $(MAKE) html

# Agent management targets
agents-list:
	@echo "Listing Agent Engine instances..."
ifdef PROJECT
ifdef LOCATION
	$(MANAGE_AGENTS) --project $(PROJECT) --location $(LOCATION) list $(if $(VERBOSE),-v)
else
	$(MANAGE_AGENTS) --project $(PROJECT) list $(if $(VERBOSE),-v)
endif
else
	$(MANAGE_AGENTS) list $(if $(VERBOSE),-v)
endif

agents-delete:
ifndef INDEX
	@echo "Error: INDEX parameter required. Usage: make agents-delete INDEX=1"
	@exit 1
endif
	@echo "Deleting Agent Engine instance at index $(INDEX)..."
ifdef PROJECT
ifdef LOCATION
	$(MANAGE_AGENTS) --project $(PROJECT) --location $(LOCATION) delete --index $(INDEX) $(if $(FORCE),--force)
else
	$(MANAGE_AGENTS) --project $(PROJECT) delete --index $(INDEX) $(if $(FORCE),--force)
endif
else
	$(MANAGE_AGENTS) delete --index $(INDEX) $(if $(FORCE),--force)
endif

# Multi-agent system targets
multi-agent-setup:
	@echo "Setting up multi-agent environment..."
	@if [ ! -f "$(MULTIAGENT_DIR)/manager/.env" ]; then \
		echo "Creating .env file in $(MULTIAGENT_DIR)/manager/"; \
		echo "GOOGLE_API_KEY=your_api_key_here" > "$(MULTIAGENT_DIR)/manager/.env"; \
		echo "Please edit $(MULTIAGENT_DIR)/manager/.env with your API key"; \
	fi
	@cd $(MULTIAGENT_DIR) && pip install -r ../requirements.txt

multi-agent-run:
	@echo "Running manager agent..."
	@cd $(MULTIAGENT_DIR) && adk run manager

multi-agent-web:
	@echo "Starting multi-agent web UI..."
	@cd $(MULTIAGENT_DIR) && adk web

# Cookiecutter targets
cookiecutter-setup:
	@echo "Setting up cookiecutter agent builder..."
	@if [ ! -d "$(COOKIECUTTER_BUILDER)/venv" ]; then \
		echo "Creating virtual environment for cookiecutter builder..."; \
		cd $(COOKIECUTTER_BUILDER) && python3 -m venv venv; \
	fi
	@echo "Installing dependencies..."
	@cd $(COOKIECUTTER_BUILDER) && \
		source venv/bin/activate && \
		pip install -r requirements.txt && \
		pip install cookiecutter
	@echo "Running migrations..."
	@cd $(COOKIECUTTER_BUILDER) && \
		source venv/bin/activate && \
		python manage.py migrate
	@echo "Cookiecutter builder setup complete!"
	@echo "Run 'make cookiecutter-run' to start the web interface"

cookiecutter-run:
	@echo "Starting cookiecutter agent builder web interface..."
	@echo "Access at http://localhost:8000"
	@cd $(COOKIECUTTER_BUILDER) && \
		source venv/bin/activate && \
		python manage.py runserver

cookiecutter-new-agent:
ifndef NAME
	@echo "Error: NAME parameter required. Usage: make cookiecutter-new-agent NAME=my-agent"
	@exit 1
endif
	@echo "Creating new agent '$(NAME)' from cookiecutter template..."
	@if [ ! -f ~/.local/bin/cookiecutter ] && [ ! -f venv/bin/cookiecutter ]; then \
		echo "Installing cookiecutter..."; \
		pip install cookiecutter; \
	fi
	@cookiecutter $(COOKIECUTTER_TEMPLATE) --no-input project_name="$(NAME)" project_slug="$(NAME)" || \
		cookiecutter $(COOKIECUTTER_TEMPLATE)
	@echo "Agent '$(NAME)' created successfully!"
	@echo "Check the new directory for your agent files."

# ADK deployment targets
adk-deploy:
	@# Use agents/google_mcp_security_agent directory if AGENT_DIR not specified
	$(eval AGENT_DIR := $(or $(AGENT_DIR),agents/google_mcp_security_agent))
	@echo "Deploying agent from directory: $(AGENT_DIR)"
	@if [ ! -d "$(AGENT_DIR)" ]; then \
		echo "Error: Directory $(AGENT_DIR) does not exist"; \
		exit 1; \
	fi
	@# Install markdown
	@echo "Installing markdown..."
	@pip install markdown
	@# Copy libs and server to agent directory for deployment
	@echo "Copying libs to $(AGENT_DIR)..."
	@cp -R libs "$(AGENT_DIR)/"
	@echo "Copying server directory to $(AGENT_DIR)..."
	@if [ -d "../server" ]; then \
		cp -R ../server "$(AGENT_DIR)/"; \
		echo "Server directory copied from ../server"; \
		echo "Removing .venv directories from copied server"; \
		find "$(AGENT_DIR)/server" -name ".venv" -type d -exec rm -rf {} + 2>/dev/null || true; \
	else \
		echo "ERROR: ../server directory not found!"; \
		echo "Expected server at: $$(pwd)/../server"; \
		echo "Available directories:"; \
		ls -la ../; \
		exit 1; \
	fi
	@# Use environment variables with proper fallbacks
	$(eval PROJECT := $(or $(PROJECT),$(shell grep "^GOOGLE_CLOUD_PROJECT=" $(ENV_FILE_PATH) | cut -d= -f2)))
	$(eval REGION := $(or $(REGION),$(shell grep "^GOOGLE_CLOUD_LOCATION=" $(ENV_FILE_PATH) | cut -d= -f2),us-central1))
	$(eval DISPLAY_NAME := $(or $(DISPLAY_NAME),$(AGENT_DISPLAY_NAME),"Google Security Agent"))
	$(eval STAGING_BUCKET := $(or $(STAGING_BUCKET),$(GCS_STAGING_BUCKET)))
	@# Generate staging bucket if not provided
	@BUCKET_TO_USE='$(STAGING_BUCKET)'; \
	if [ -z "$$BUCKET_TO_USE" ]; then \
		BUCKET_TO_USE="gs://agent-deploy-$(PROJECT)-$(shell date +%Y%m%d-%H%M%S)"; \
		echo "Generated staging bucket: $$BUCKET_TO_USE"; \
	fi; \
	echo "Deployment configuration:"; \
	echo "  PROJECT: $(PROJECT)"; \
	echo "  REGION: $(REGION)"; \
	echo "  DISPLAY_NAME: $(DISPLAY_NAME)"; \
	echo "  STAGING_BUCKET: $$BUCKET_TO_USE"; \
	echo "  AGENT_DIR: $(AGENT_DIR)"; \
	echo ""; \
	echo "Deploying agent to Agent Engine..."; \
	adk deploy agent_engine \
		--project $(PROJECT) \
		--region $(REGION) \
		--staging_bucket "$$BUCKET_TO_USE" \
		--display_name '$(DISPLAY_NAME)' \
		$(if $(TRACE),--trace_to_cloud) \
		$(AGENT_DIR);
	@# Clean up copied libs and server
	@echo "Cleaning up copied libs from $(AGENT_DIR)..."
	@rm -rf "$(AGENT_DIR)/libs"
	@echo "Cleaning up copied server from $(AGENT_DIR)..."
	@rm -rf "$(AGENT_DIR)/server"
	@echo ""
	@echo "✓ Agent deployed successfully!"
	@echo ""
	@echo "Next steps:"
	@echo "1. Note the resource name from the output above"
	@echo "2. Update .env with: make env-update KEY=AGENT_ENGINE_RESOURCE_NAME VALUE=<resource-name>"
	@echo "3. Test the agent: make test-agent"
	@echo "4. Register with AgentSpace: make agentspace-register"

# AgentSpace management targets
AGENTSPACE_MANAGER := $(PYTHON) scripts/agentspace_manager.py

agentspace-register: env-validate-agentspace
	@echo "Registering agent with AgentSpace..."
	@$(AGENTSPACE_MANAGER) register --env-file $(ENV_FILE_PATH) $(if $(FORCE),--force)

agentspace-update: env-validate-agentspace
	@echo "Updating AgentSpace registration..."
	@$(AGENTSPACE_MANAGER) update --env-file $(ENV_FILE_PATH)

agentspace-verify:
	@echo "Verifying AgentSpace integration..."
	@$(AGENTSPACE_MANAGER) verify --env-file $(ENV_FILE_PATH)

agentspace-delete:
	@echo "Removing agent from AgentSpace..."
	@$(AGENTSPACE_MANAGER) delete --env-file $(ENV_FILE_PATH) $(if $(FORCE),--force)

agentspace-url:
	@$(AGENTSPACE_MANAGER) url --env-file $(ENV_FILE_PATH)

# Cloud Run deployment targets
cloudrun-deploy: env-check
	@echo "Deploying agent to Cloud Run..."
	@echo "Deployment configuration:"
	@echo "  PROJECT: $$(grep GOOGLE_CLOUD_PROJECT $(ENV_FILE_PATH) | cut -d= -f2)"
	@echo "  REGION: $$(grep GOOGLE_CLOUD_LOCATION $(ENV_FILE_PATH) | cut -d= -f2)"
	@echo "  SERVICE: mcp-security-agent-service"
	@echo ""
	@# Run the deployment script
	@bash ./scripts/cloudrun_deploy_run.sh deploy
	@echo ""
	@echo "✓ Cloud Run deployment complete!"
	@echo ""
	@echo "Next steps:"
	@echo "1. Test the service: make cloudrun-test"
	@echo "2. View logs: make cloudrun-logs"
	@echo "3. Get service URL: make cloudrun-url"

cloudrun-run: env-check
	@echo "Running Cloud Run service locally..."
	@cd .. && bash ./run-with-google-adk/scripts/cloudrun_deploy_run.sh run

cloudrun-test:
	@echo "Testing Cloud Run service..."
	$(eval PROJECT := $(or $(PROJECT),$(GOOGLE_CLOUD_PROJECT)))
	$(eval REGION := $(or $(REGION),$(GOOGLE_CLOUD_LOCATION),us-central1))
	$(eval SERVICE := mcp-security-agent-service)
	@echo "Getting service URL..."
	$(eval SERVICE_URL := $(shell gcloud run services describe $(SERVICE) --project $(PROJECT) --region $(REGION) --format='value(status.url)' 2>/dev/null))
	@if [ -z "$(SERVICE_URL)" ]; then \
		echo "Error: Could not get service URL. Is the service deployed?"; \
		exit 1; \
	fi
	@echo "Service URL: $(SERVICE_URL)"
	@echo ""
	@echo "Testing with curl..."
	@curl -s -X POST $(SERVICE_URL)/health || echo "Note: /health endpoint may not exist"
	@echo ""
	@echo "To test interactively, visit: $(SERVICE_URL)"

cloudrun-logs:
	@echo "Viewing Cloud Run logs..."
	$(eval PROJECT := $(or $(PROJECT),$(shell grep "^GOOGLE_CLOUD_PROJECT=" $(ENV_FILE_PATH) | cut -d= -f2)))
	$(eval REGION := $(or $(REGION),$(shell grep "^GOOGLE_CLOUD_LOCATION=" $(ENV_FILE_PATH) | cut -d= -f2),us-central1))
	$(eval SERVICE := mcp-security-agent-service)
	gcloud logging read "resource.type=cloud_run_revision AND resource.labels.service_name=$(SERVICE)" \
		--project $(PROJECT) \
		--limit 50 \
		--format "table(timestamp,severity,textPayload)"

cloudrun-url:
	$(eval PROJECT := $(or $(PROJECT),$(GOOGLE_CLOUD_PROJECT)))
	$(eval REGION := $(or $(REGION),$(GOOGLE_CLOUD_LOCATION),us-central1))
	$(eval SERVICE := mcp-security-agent-service)
	@echo "Getting Cloud Run service URL..."
	@gcloud run services describe $(SERVICE) \
		--project $(PROJECT) \
		--region $(REGION) \
		--format='value(status.url)' || echo "Service not found. Deploy first with: make cloudrun-deploy"

cloudrun-delete:
	$(eval PROJECT := $(or $(PROJECT),$(GOOGLE_CLOUD_PROJECT)))
	$(eval REGION := $(or $(REGION),$(GOOGLE_CLOUD_LOCATION),us-central1))
	$(eval SERVICE := mcp-security-agent-service)
	@echo "Deleting Cloud Run service..."
	@echo "  SERVICE: $(SERVICE)"
	@echo "  PROJECT: $(PROJECT)"
	@echo "  REGION: $(REGION)"
	@echo ""
	@read -p "Are you sure you want to delete this service? (y/N) " confirm; \
	if [ "$$confirm" = "y" ] || [ "$$confirm" = "Y" ]; then \
		gcloud run services delete $(SERVICE) \
			--project $(PROJECT) \
			--region $(REGION) \
			--quiet && \
		echo "✓ Service deleted successfully"; \
	else \
		echo "Deletion cancelled"; \
	fi

# Cloud Run proxy targets
gcloud-proxy:
ifndef SERVICE
	@echo "Error: SERVICE parameter required. Usage: make gcloud-proxy SERVICE=my-service"
	@exit 1
endif
	@echo "Starting gcloud proxy for Cloud Run service: $(SERVICE)"
	@# Set default values if not provided
	$(eval PROJECT := $(or $(PROJECT),$(shell echo $$GOOGLE_CLOUD_PROJECT || echo $$GCP_PROJECT)))
	$(eval REGION := $(or $(REGION),$(shell echo $$GOOGLE_CLOUD_REGION || echo $$GOOGLE_CLOUD_LOCATION || echo "us-central1")))
	$(eval PORT := $(or $(PORT),8080))
	@echo "Using PROJECT: $(PROJECT)"
	@echo "Using REGION: $(REGION)"
	@echo "Using PORT: $(PORT)"
	@if [ -z "$(PROJECT)" ]; then \
		echo "Error: PROJECT not set. Use PROJECT=your-project or set GOOGLE_CLOUD_PROJECT env var"; \
		exit 1; \
	fi
	@echo "Proxying $(SERVICE) to http://localhost:$(PORT)"
	@echo "Press Ctrl+C to stop the proxy"
	gcloud run services proxy $(SERVICE) \
		--project $(PROJECT) \
		--region $(REGION) \
		--port $(PORT)

# Agent testing targets
test-agent:
	@# Try to use RESOURCE or AGENT_ENGINE_RESOURCE_NAME from env
	$(eval RESOURCE := $(or $(RESOURCE),$(AGENT_ENGINE_RESOURCE_NAME)))
ifndef RESOURCE
	@echo "Error: RESOURCE parameter required. Usage: make test-agent RESOURCE=projects/.../reasoningEngines/..."
	@echo "Get the resource name from 'make agents-list'"
	@echo "Or set AGENT_ENGINE_RESOURCE_NAME in your .env file"
	@exit 1
endif
	@echo "Testing deployed agent..."
	@echo "Agent Resource: $(RESOURCE)"
	$(eval MSG := $(or $(MSG),"List MCP Tools for SOAR and then list SOAR Cases."))
	@echo "Message: $(MSG)"
	@echo "Running test_deployed_agent.py..."
	@AGENT_ENGINE_RESOURCE="$(RESOURCE)" $(PYTHON) scripts/test_deployed_agent.py "$(MSG)"

# Combined workflow targets

deploy: env-check
	@echo "Choose deployment target:"
	@echo "1. Agent Engine (Vertex AI)"
	@echo "2. Cloud Run"
	@echo ""
	@read -p "Enter choice (1 or 2): " choice; \
	if [ "$$choice" = "1" ]; then \
		$(MAKE) adk-deploy; \
	elif [ "$$choice" = "2" ]; then \
		$(MAKE) cloudrun-deploy; \
	else \
		echo "Invalid choice. Use 'make adk-deploy' or 'make cloudrun-deploy'"; \
		exit 1; \
	fi

deploy-and-test: env-validate-agent-engine adk-deploy
	@echo ""
	@echo "Deployment complete! Now test the agent:"
	@echo "1. Copy the resource name from above"
	@echo "2. Run: make test-agent RESOURCE=<resource-name>"

# Utility targets
clean:
	@echo "Cleaning temporary files..."
	@find . -type f -name "*.pyc" -delete
	@find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	@find . -type d -name ".ruff_cache" -exec rm -rf {} + 2>/dev/null || true
	@echo "✓ Cleaned temporary files"

.PHONY: setup-all deploy-and-test clean
