# Vertex AI Integration

This document describes the available tools for the Google Cloud Vertex AI integration within the SecOps SOAR MCP Server. Vertex AI provides access to Google's generative AI models.

## Configuration

Ensure the Vertex AI integration is configured in the SOAR platform, likely requiring Google Cloud project details and appropriate permissions for the SOAR service account to access Vertex AI services.

## Available Tools

### vertex_ai_execute_prompt
- **Description:** Execute individual text prompts using a specified Vertex AI model (e.g., Gemini).
- **Args:**
    - `case_id` (str, required): The ID of the case.
    - `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
    - `text_prompt` (str, required): The text instructions to include in the prompt.
    - `model_id` (str, optional): The ID of the model to use (e.g., "gemini-1.5-flash-002"). Defaults to None (likely uses a default configured model).
    - `temperature` (str, optional): Float value (0.0-1.0) controlling randomness. Higher values increase creativity. Defaults to None (uses model default).
    - `candidate_count` (str, optional): Number of response variations to return. Defaults to None (likely 1).
    - `response_mime_type` (List[str], optional): Output MIME type (e.g., ["application/json"]). Available for gemini-1.5 models. Defaults to None.
    - `response_schema` (str, optional): OpenAPI schema for the response structure. Requires `response_mime_type`. Available for gemini-1.5 models. Defaults to None.
    - `max_input_tokens` (str, optional): Maximum input tokens allowed. Fails if exceeded. Defaults to None (no limit).
    - `max_output_tokens` (str, optional): Maximum output tokens to generate per response. Defaults to None (uses model default).
    - `target_entities` (List[TargetEntity], optional): Specific target entities (Identifier, EntityType) to run the action on. Defaults to empty list.
    - `scope` (str, optional): Defines the scope for the action (e.g., "All entities"). Defaults to "All entities". Used if `target_entities` is empty.
- **Returns:** (dict) A dictionary containing the generated response(s) from the Vertex AI model.

### vertex_ai_describe_entity
- **Description:** (Preview) Summarize information about entities using Vertex AI. Works with all entity types, submitting each individually. Caches results based on input hash and refresh interval.
- **Args:**
    - `case_id` (str, required): The ID of the case.
    - `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
    - `refresh_after_days` (str, required): Days before refreshing the summary if inputs haven't changed.
    - `model_id` (str, optional): The ID of the model to use (e.g., "gemini-1.5-flash-002"). Defaults to None.
    - `temperature` (str, optional): Float value controlling randomness. Defaults to None.
    - `exclude_fields` (str, optional): Comma-separated list of entity metadata fields to exclude from the summary input. Defaults to None.
    - `force_refresh` (bool, optional): If selected, ignore cache and regenerate summary. Defaults to None.
    - `max_output_tokens` (str, optional): Maximum output tokens per entity summary. Defaults to None.
    - `target_entities` (List[TargetEntity], optional): Specific target entities (Identifier, EntityType) to run the action on. Defaults to empty list.
    - `scope` (str, optional): Defines the scope for the action (e.g., "All entities"). Defaults to "All entities". Used if `target_entities` is empty.
- **Returns:** (dict) A dictionary containing the generated summary for the entity/entities.

### vertex_ai_ping
- **Description:** Test connectivity to the Vertex AI service using the configured credentials and project settings.
- **Args:**
    - `case_id` (str, required): The ID of the case.
    - `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
    - `target_entities` (List[TargetEntity], optional): Specific target entities (Identifier, EntityType) to run the action on. Defaults to empty list.
    - `scope` (str, optional): Defines the scope for the action (e.g., "All entities"). Defaults to "All entities". Used if `target_entities` is empty.
- **Returns:** (dict) A dictionary containing the result of the connectivity test.

### vertex_ai_analyze_eml
- **Description:** (Preview) Analyze EML files using Vertex AI. Submits each file individually.
- **Args:**
    - `case_id` (str, required): The ID of the case.
    - `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
    - `files_to_analyze` (str, required): Comma-separated list of EML file paths (accessible by the SOAR server) to submit.
    - `model_id` (str, optional): The ID of the model to use (e.g., "gemini-1.5-flash-002"). Defaults to None.
    - `temperature` (str, optional): Float value controlling randomness. Defaults to None.
    - `max_output_tokens` (str, optional): Maximum output tokens per file analysis. Defaults to None.
    - `target_entities` (List[TargetEntity], optional): Specific target entities (Identifier, EntityType) to run the action on. Defaults to empty list.
    - `scope` (str, optional): Defines the scope for the action (e.g., "All entities"). Defaults to "All entities". Used if `target_entities` is empty.
- **Returns:** (dict) A dictionary containing the analysis results for the submitted EML files.

### vertex_ai_transform_data
- **Description:** (Preview) Perform data transformations on a JSON object using Vertex AI based on a text prompt.
- **Args:**
    - `case_id` (str, required): The ID of the case.
    - `alert_group_identifiers` (List[str], required): Identifiers for the alert groups.
    - `text_prompt` (str, required): The text instructions for the transformation.
    - `json_object` (Union[str, dict], required): The JSON object (as a string or dict) to transform.
    - `max_output_tokens` (str, required): Maximum output tokens for the transformed data.
    - `model_id` (str, optional): The ID of the model to use (e.g., "gemini-1.5-flash-002"). Defaults to None.
    - `temperature` (str, optional): Float value controlling randomness. Defaults to None.
    - `target_entities` (List[TargetEntity], optional): Specific target entities (Identifier, EntityType) to run the action on. Defaults to empty list.
    - `scope` (str, optional): Defines the scope for the action (e.g., "All entities"). Defaults to "All entities". Used if `target_entities` is empty.
- **Returns:** (dict) A dictionary containing the transformed data as returned by the Vertex AI model.
