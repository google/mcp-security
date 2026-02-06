import json
import os

def main():
    env_file = '.env'
    json_file = 'gemini-extension.json'

    if not os.path.exists(env_file):
        print(f"Error: {env_file} not found.")
        return

    if not os.path.exists(json_file):
        print(f"Error: {json_file} not found.")
        return

    # Read .env file
    env_vars = {}
    with open(env_file, 'r') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#'):
                key, value = line.split('=', 1)
                env_vars[key.strip()] = value.strip()

    # Read gemini-extension.json
    with open(json_file, 'r') as f:
        data = json.load(f)

    # Update defaultValue in settings
    if 'settings' in data:
        for setting in data['settings']:
            env_var_name = setting.get('envVar')
            if env_var_name and env_var_name in env_vars:
                setting['defaultValue'] = env_vars[env_var_name]
                print(f"Updated {env_var_name} to {env_vars[env_var_name]}")

    # Write back to gemini-extension.json
    with open(json_file, 'w') as f:
        json.dump(data, f, indent=2)
        f.write('\n') # Add trailing newline

    print("Successfully updated gemini-extension.json")

if __name__ == "__main__":
    main()
