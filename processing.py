import json
from typing import Optional
from google.api_core.client_options import ClientOptions
from google.cloud import documentai

project_id = ""
location = "us"  # Format is "us" or "eu"
processor_id = ""  # Create processor before running sample
processor_version = "rc"  # Refer to https://cloud.google.com/document-ai/docs/manage-processor-versions for more information
file_path = ""
mime_type = ""  # Refer to https://cloud.google.com/document-ai/docs/file-types for supported file types
output_json_path = ""


def process_document_entity_extraction_sample(
    project_id: str,
    location: str,
    processor_id: str,
    processor_version: str,
    file_path: str,
    mime_type: str,
    output_json_path: str
) -> None:
    # Online processing request to Document AI
    document = process_document(
        project_id, location, processor_id, processor_version, file_path, mime_type
    )

    # Extract entities and save to JSON
    entities_list = []
    for entity in document.entities:
        entity_dict = get_entity_dict(entity)
        # Include nested entities
        entity_dict['properties'] = [get_entity_dict(prop) for prop in entity.properties]
        entities_list.append(entity_dict)

    with open(output_json_path, "w") as json_file:
        json.dump(entities_list, json_file, indent=2)

    print(f"Entities have been saved to {output_json_path}")


def get_entity_dict(entity: documentai.Document.Entity) -> dict:
    return {
        "type": entity.type_,
        "text": entity.text_anchor.content,
        "confidence": entity.confidence,
        "normalized_value": entity.normalized_value.text if entity.normalized_value else None
    }


def process_document(
    project_id: str,
    location: str,
    processor_id: str,
    processor_version: str,
    file_path: str,
    mime_type: str,
    process_options: Optional[documentai.ProcessOptions] = None,
) -> documentai.Document:
    # You must set the `api_endpoint` if you use a location other than "us".
    client = documentai.DocumentProcessorServiceClient(
        client_options=ClientOptions(
            api_endpoint=f"{location}-documentai.googleapis.com"
        )
    )

    # The full resource name of the processor version, e.g.:
    # `projects/{project_id}/locations/{location}/processors/{processor_id}/processorVersions/{processor_version_id}`
    # You must create a processor before running this sample.
    name = client.processor_version_path(
        project_id, location, processor_id, processor_version
    )

    # Read the file into memory
    with open(file_path, "rb") as image:
        image_content = image.read()

    # Configure the process request
    request = documentai.ProcessRequest(
        name=name,
        raw_document=documentai.RawDocument(content=image_content, mime_type=mime_type),
        # Only supported for Document OCR processor
        process_options=process_options,
    )

    result = client.process_document(request=request)

    # For a full list of `Document` object attributes, reference this page:
    # https://cloud.google.com/document-ai/docs/reference/rest/v1/Document
    return result.document


# Run the sample
process_document_entity_extraction_sample(
    project_id, location, processor_id, processor_version, file_path, mime_type, output_json_path
)
