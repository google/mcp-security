# Launching Google Security MCP Servers in Firebase Studio

This guide provides instructions on how to set up and run the Google Security MCP (Model Context Protocol) servers within a [Firebase Studio](https://firebase.studio/) environment using the Cline VSCode extension.

## Table of Contents

- [1. Prerequisites](#1-prerequisites)
- [2. Firebase Studio Workspace Setup](#2-firebase-studio-workspace-setup)
- [3. Project and Repository Setup](#3-project-and-repository-setup)
- [4. Environment Configuration](#4-environment-configuration)
- [5. Cline and MCP Server Configuration](#5-cline-and-mcp-server-configuration)

## 1. Prerequisites

Before you begin, ensure you have the following:

- Access to [Firebase Studio](https://firebase.studio/).
- A Google Account with permissions to use Firebase Studio and the necessary Google Cloud Security services with respective API keys.
- An API Key for your chosen LLM provider or Application Default Credentials (e.g., Google Gemini or Vertex AI).

## 2. Firebase Studio Workspace Setup

First, we will prepare the Firebase Studio environment.

1.  Navigate to [Firebase Studio](https://firebase.studio/) and create a new, empty workspace. Give it a descriptive name like `security-mcp-demo`.
   

2.  Once the environment is built, open the `dev.nix` file from the file explorer.

3.  Modify the `dev.nix` file to include the `cacert` package and set the `SSL_CERT_FILE` environment variable. This is crucial for tools like `uv` to handle SSL/TLS certificates correctly within the containerized environment. Your configuration should look like this:

    ```nix
    { pkgs, ... }: {
      # Which nixpkgs channel to use.
      channel = "stable-24.05"; # or "unstable"
      # Use https://search.nixos.org/packages to find packages
      packages = [
        pkgs.cacert
        # pkgs.go
        # pkgs.python311
        # pkgs.python311Packages.pip
        # pkgs.nodejs_20
        # pkgs.nodePackages.nodemon
      ];
      # Sets environment variables in the workspace
      env = {
        SSL_CERT_FILE = "${pkgs.cacert}/etc/ssl/certs/ca-bundle.crt";
      };
      idx = {
        # ...
    ```

4.  After saving the changes to `dev.nix`, click the **Rebuild environment** button that appears in the bottom right of the editor.

## 3. Project and Repository Setup

With the workspace configured, you can now set up your project directory and clone the repository.

1.  Open a terminal in VSCode (`Ctrl` + \`).

2.  Create a project directory and navigate into it.

    ```bash
    # Replace 'tier1-demo' with your desired project directory name
    install -d -m 755 tier1-demo
    cd tier1-demo
    ```

3.  Clone the `mcp-security` repository from GitHub.

    ```bash
    git clone https://github.com/google/mcp-security.git
    cd mcp-security
    ```

## 4. Environment Configuration

Next, you need to configure environment variables for the MCP servers and install necessary tools.

1.  Create a `.env` file in the root of the `mcp-security` directory.

    ```bash
    # Make sure you are in the 'mcp-security' directory
    install -m 644 /dev/null .env
    ```

2.  Run `echo $SSL_CERT_FILE` in the terminal and copy the full output path (e.g., `/nix/store/...-cacert-.../etc/ssl/certs/ca-bundle.crt`). You will need this for the next step.

3.  Open the newly created `.env` file and populate it with the necessary credentials and configuration. Replace the placeholder values with your actual values and the `SSL_CERT_FILE` path from the previous step.

    ```dotenv
    # Chronicle SecOps SIEM
    CHRONICLE_PROJECT_ID=your-google-cloud-project-id
    CHRONICLE_CUSTOMER_ID=your-chronicle-customer-id
    CHRONICLE_REGION=us

    # Chronicle SecOps SOAR
    SOAR_URL=your-soar-url
    SOAR_APP_KEY=your-soar-app-key

    # Google Threat Intelligence (VirusTotal)
    VT_APIKEY=your-gti-api-key

    # SSL Certificate Path
    SSL_CERT_FILE=/path/copied/from/previous/step
    ```
   

4.  Install `uv`, the Python package manager, and then use it to install the latest version of Python.

    ```bash
    # Install uv
    curl -LsSf https://astral.sh/uv/install.sh | sh
    
    # Add uv to the current session's PATH
    source $HOME/.local/bin/env
    
    # Install Python
    uv python install
    ```

## 5. Cline and MCP Server Configuration

Finally, install and configure the Cline VSCode extension to run the MCP servers.

> 🪧 **NOTE:**
> You should already be authenticated with your Google credentials in Firebase Studio. If you encounter permissions issues, ensure you are logged in with the correct account in the top-right corner of the IDE.

1.  In the VSCode Activity Bar, go to **Extensions**, search for "Cline", and click **Install**.

2.  Open Cline from the Activity Bar and configure it with your LLM provider information.

3.  In Cline's settings, it is recommended to disable both "Anonymous usage collection" and "Enable Rich MCP Display" for this use case to prevent potentially malicious domain names from resolving.

4.  Navigate to the MCP server configuration section in Cline (the server icon) and click **Configure MCP Servers**. This will open a `cline_mcp_settings.json` file.

5.  Copy the content from the `cline_mcp_settings.json.example` file provided in this directory and replace the placeholders:

    > ⚠️ **CAUTION:**
    > Replace `YOUR-WORKSPACE-NAME` with your Firebase Studio workspace name (from step 2.1) and `YOUR-PROJECT-DIR` with your project directory name (from step 3.2) in all paths. You can verify the path to `uv` by running `which uv` in the terminal.

    For example:
    - If your workspace is named `security-mcp-demo` and your project directory is `tier1-demo`, you would replace:
      - `/home/user/YOUR-WORKSPACE-NAME/YOUR-PROJECT-DIR/mcp-security/...`
      - with: `/home/user/security-mcp-demo/tier1-demo/mcp-security/...`

    The configuration file contains settings for four MCP servers:
    - **secops**: Security Operations (Chronicle SIEM)
    - **secops-soar**: SOAR platform integration
    - **gti**: Google Threat Intelligence (VirusTotal)
    - **scc-mcp**: Security Command Center

6.  Save the `cline_mcp_settings.json` file. The MCP servers will begin to initialize in Cline. This may take a few minutes as their dependencies are installed for the first time.

7.  Once complete, the servers will show a green status light, and you can expand each one to see the available tools. You are now fully set up to use the Security MCP servers in Firebase Studio. ✅

   

## License

This project is licensed under the Apache 2.0 License. See the [LICENSE](LICENSE) file for details.
