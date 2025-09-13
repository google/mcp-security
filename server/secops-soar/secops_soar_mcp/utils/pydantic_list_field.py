from typing import Type
from pydantic import BaseModel, Field
from pydantic.json_schema import GenerateJsonSchema

def PydanticListField(
    model: Type[BaseModel],
    description: str = "",
    default_factory=list,
) -> Field:
    """
    Creates a Pydantic Field for a list of a given BaseModel,
    manually injecting the correct JSON schema to satisfy the Gemini CLI validator.
    """
    # Use Pydantic's own schema generator to build the schema for the model
    model_schema = model.model_json_schema()

    # The schema generator might place definitions in a "$defs" block,
    # so we need to get the actual schema, which might be a reference.
    # This logic handles both simple and complex (referenced) schemas.
    if "$ref" in model_schema:
        ref_key = model_schema["$ref"].split('/')[-1]
        final_schema = model_schema["$defs"][ref_key]
    else:
        final_schema = model_schema

    return Field(
        default_factory=default_factory,
        description=description,
        json_schema_extra={"items": final_schema},
    )