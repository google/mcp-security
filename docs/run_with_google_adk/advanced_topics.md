# Advanced Topics

### Improving Performance and Optimizing Costs
You can control the number of previous interactions sent to the LLM by setting the `MAX_PREV_USER_INTERACTIONS` variable in your `.env` file. A lower number (default is 3) reduces context size, which can improve performance and lower costs.

### Integrating Custom MCP Servers
This agent can be extended to include your own MCP servers. For a detailed guide and examples, please refer to the `docs/development_guide.md` file.

### Additional Features
The agent supports creating files and generating signed URLs for them via the artifact service. For example, you can ask the agent to "add the summary as markdown to summary_146.md" and then "create a link to file summary_146.md".
