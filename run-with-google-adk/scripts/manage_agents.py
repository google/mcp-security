#!/usr/bin/env python3
"""
Utility to manage (list and delete) remote agents in Google Agent Engine
"""

import argparse
import sys
from typing import List, Optional
import vertexai
from vertexai import agent_engines
from google.cloud import aiplatform
from datetime import datetime
import os

# ANSI color codes for better output
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

def print_header(text):
    print(f"\n{Colors.HEADER}{Colors.BOLD}{'=' * 80}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{text.center(80)}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{'=' * 80}{Colors.ENDC}\n")

def format_timestamp(timestamp):
    """Format timestamp to readable string"""
    if timestamp:
        dt = datetime.fromtimestamp(timestamp)
        return dt.strftime("%Y-%m-%d %H:%M:%S")
    return "N/A"

def initialize_vertexai(project: str, location: str):
    """Initialize Vertex AI with project and location"""
    try:
        vertexai.init(project=project, location=location)
        aiplatform.init(project=project, location=location)
        print(f"{Colors.GREEN}✅ Initialized Vertex AI - Project: {project}, Location: {location}{Colors.ENDC}")
    except Exception as e:
        print(f"{Colors.RED}❌ Failed to initialize Vertex AI: {str(e)}{Colors.ENDC}")
        sys.exit(1)

def list_agents(project: str, location: str, verbose: bool = False) -> List[dict]:
    """List all Agent Engine instances"""
    print_header("Listing Agent Engine Instances")
    
    initialize_vertexai(project, location)
    
    try:
        # Use the vertexai API to list reasoning engines
        from google.cloud.aiplatform_v1beta1 import ReasoningEngineServiceClient
        from google.api_core import client_options
        
        # Create client with regional endpoint
        endpoint = f"{location}-aiplatform.googleapis.com"
        client_opts = client_options.ClientOptions(api_endpoint=endpoint)
        client = ReasoningEngineServiceClient(client_options=client_opts)
        
        parent = f"projects/{project}/locations/{location}"
        agents = client.list_reasoning_engines(parent=parent)
        
        agent_list = []
        agents_list = list(agents)  # Convert to list to get count
        
        if not agents_list:
            print(f"{Colors.YELLOW}No Agent Engine instances found.{Colors.ENDC}")
            return []
        
        print(f"Found {Colors.CYAN}{len(agents_list)}{Colors.ENDC} Agent Engine instance(s):\n")
        
        for i, agent in enumerate(agents_list, 1):
            agent_info = {
                'resource_name': agent.name,
                'display_name': agent.display_name,
                'create_time': agent.create_time,
                'update_time': agent.update_time,
                'state': agent.state.name if hasattr(agent, 'state') else 'UNKNOWN',
            }
            agent_list.append(agent_info)
            
            print(f"{Colors.CYAN}{i}. {agent.display_name}{Colors.ENDC}")
            print(f"   Resource: {agent.name}")
            print(f"   Created: {format_timestamp(agent.create_time.timestamp() if agent.create_time else None)}")
            print(f"   Updated: {format_timestamp(agent.update_time.timestamp() if agent.update_time else None)}")
            
            if verbose:
                print(f"   State: {agent_info['state']}")
                # Try to get additional details
                try:
                    full_agent = agent_engines.get(agent.name)
                    print(f"   Type: {type(full_agent).__name__}")
                except Exception as e:
                    print(f"   {Colors.YELLOW}Could not fetch additional details: {str(e)}{Colors.ENDC}")
            
            print()
        
        return agent_list
        
    except Exception as e:
        print(f"{Colors.RED}❌ Error listing agents: {str(e)}{Colors.ENDC}")
        return []

def delete_agent(resource_name: str, project: str, location: str, force: bool = False) -> bool:
    """Delete a specific Agent Engine instance"""
    print_header("Deleting Agent Engine Instance")
    
    initialize_vertexai(project, location)
    
    try:
        # Get the agent first to confirm it exists
        from google.cloud.aiplatform_v1beta1 import ReasoningEngineServiceClient
        from google.api_core import client_options
        
        # Create client with regional endpoint
        endpoint = f"{location}-aiplatform.googleapis.com"
        client_opts = client_options.ClientOptions(api_endpoint=endpoint)
        client = ReasoningEngineServiceClient(client_options=client_opts)
        
        print(f"Fetching agent: {resource_name}")
        agent = client.get_reasoning_engine(name=resource_name)
        
        print(f"\n{Colors.YELLOW}Agent Details:{Colors.ENDC}")
        print(f"  Name: {agent.display_name}")
        print(f"  Resource: {agent.name}")
        print(f"  Created: {format_timestamp(agent.create_time.timestamp() if agent.create_time else None)}")
        
        if not force:
            confirm = input(f"\n{Colors.RED}Are you sure you want to delete this agent? (yes/no): {Colors.ENDC}")
            if confirm.lower() != 'yes':
                print(f"{Colors.YELLOW}Deletion cancelled.{Colors.ENDC}")
                return False
        
        print(f"\n{Colors.YELLOW}Deleting agent...{Colors.ENDC}")
        # Delete with force=True to remove child resources
        from google.cloud.aiplatform_v1beta1 import DeleteReasoningEngineRequest
        request = DeleteReasoningEngineRequest(
            name=resource_name,
            force=True  # This will delete child resources (sessions, memories)
        )
        client.delete_reasoning_engine(request=request)
        print(f"{Colors.GREEN}✅ Agent deleted successfully!{Colors.ENDC}")
        return True
        
    except Exception as e:
        print(f"{Colors.RED}❌ Error deleting agent: {str(e)}{Colors.ENDC}")
        return False

def delete_agent_by_index(index: int, project: str, location: str, force: bool = False) -> bool:
    """Delete an agent by its index in the list"""
    agents = list_agents(project, location, verbose=False)
    
    if not agents:
        return False
    
    if index < 1 or index > len(agents):
        print(f"{Colors.RED}❌ Invalid index. Please choose between 1 and {len(agents)}{Colors.ENDC}")
        return False
    
    agent = agents[index - 1]
    return delete_agent(agent['resource_name'], project, location, force)

def main():
    parser = argparse.ArgumentParser(
        description="Manage Google Agent Engine instances",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # List all agents in the default project
  python manage_agents.py list
  
  # List agents in a specific project and location
  python manage_agents.py list --project my-project --location us-central1
  
  # List agents with verbose output
  python manage_agents.py list -v
  
  # Delete an agent by resource name
  python manage_agents.py delete --resource projects/123/locations/us-central1/reasoningEngines/456
  
  # Delete an agent by index from the list
  python manage_agents.py delete --index 2
  
  # Force delete without confirmation
  python manage_agents.py delete --index 1 --force
        """
    )
    
    # Get defaults from environment or gcloud config
    default_project = os.getenv('GOOGLE_CLOUD_PROJECT', '')
    if not default_project:
        try:
            import subprocess
            result = subprocess.run(['gcloud', 'config', 'get-value', 'project'], 
                                  capture_output=True, text=True, check=True)
            default_project = result.stdout.strip()
        except:
            default_project = None
    
    default_location = os.getenv('GOOGLE_CLOUD_LOCATION', 'us-central1')
    
    # Global options
    parser.add_argument('--project', '-p', 
                       default=default_project,
                       help=f'Google Cloud project ID (default: {default_project or "from gcloud config"})')
    parser.add_argument('--location', '-l', 
                       default=default_location,
                       help=f'Google Cloud location (default: {default_location})')
    
    # Subcommands
    subparsers = parser.add_subparsers(dest='command', help='Commands')
    
    # List command
    list_parser = subparsers.add_parser('list', help='List all Agent Engine instances')
    list_parser.add_argument('--verbose', '-v', action='store_true', 
                            help='Show verbose output')
    
    # Delete command
    delete_parser = subparsers.add_parser('delete', help='Delete an Agent Engine instance')
    delete_group = delete_parser.add_mutually_exclusive_group(required=True)
    delete_group.add_argument('--resource', '-r', 
                             help='Full resource name of the agent to delete')
    delete_group.add_argument('--index', '-i', type=int,
                             help='Index of the agent from the list to delete')
    delete_parser.add_argument('--force', '-f', action='store_true',
                              help='Force deletion without confirmation')
    
    args = parser.parse_args()
    
    # Check if project is set
    if not args.project:
        print(f"{Colors.RED}❌ Error: No project specified. Use --project or set GOOGLE_CLOUD_PROJECT{Colors.ENDC}")
        sys.exit(1)
    
    # Execute command
    if args.command == 'list':
        list_agents(args.project, args.location, args.verbose)
    elif args.command == 'delete':
        if args.resource:
            success = delete_agent(args.resource, args.project, args.location, args.force)
        else:  # args.index
            success = delete_agent_by_index(args.index, args.project, args.location, args.force)
        
        sys.exit(0 if success else 1)
    else:
        parser.print_help()
        sys.exit(1)

if __name__ == "__main__":
    main()