from flask import Flask, request, render_template, redirect, url_for
import os
import json
from google.api_core.client_options import ClientOptions
from google.cloud import documentai

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = "/home/jaivadula/uploads"
app.config['ALLOWED_EXTENSIONS'] = {'pdf'}

project_id = "document-ai-425507"
location = "us"
processor_id = "7df4cdb10cc9f03b"
processor_version = "rc"

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/')
def upload_file():
    return render_template('upload.html')

@app.route('/uploader', methods=['GET', 'POST'])
def uploader_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = file.filename
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)

            # Process the document
            document = process_document(
                project_id, location, processor_id, processor_version, file_path, "application/pdf"
            )

            # Extract entities
            entities_list = []
            for entity in document.entities:
                entity_dict = get_entity_dict(entity)
                entity_dict['properties'] = [get_entity_dict(prop) for prop in entity.properties]
                entities_list.append(entity_dict)

            output_json_path = os.path.join(app.config['UPLOAD_FOLDER'], 'extracted_entities.json')
            with open(output_json_path, "w") as json_file:
                json.dump(entities_list, json_file, indent=2)

            return render_template('result.html', entities=entities_list)

    return redirect(url_for('upload_file'))

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
    mime_type: str
) -> documentai.Document:
    client = documentai.DocumentProcessorServiceClient(
        client_options=ClientOptions(
            api_endpoint=f"{location}-documentai.googleapis.com"
        )
    )

    name = client.processor_version_path(
        project_id, location, processor_id, processor_version
    )

    with open(file_path, "rb") as image:
        image_content = image.read()

    request = documentai.ProcessRequest(
        name=name,
        raw_document=documentai.RawDocument(content=image_content, mime_type=mime_type)
    )

    result = client.process_document(request=request)
    return result.document

if __name__ == '__main__':
    app.run(debug=True)
