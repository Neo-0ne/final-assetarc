import os
import json
from flask import Flask, jsonify, request, send_file
from docxtpl import DocxTemplate
import jinja2
import io

app = Flask(__name__)

# Load template manifest from within the app's directory
def load_template_manifest():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    manifest_path = os.path.join(base_dir, 'templates', 'templates.json')
    try:
        with open(manifest_path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        app.logger.error(f"templates.json not found at {manifest_path}!")
        return []
    except json.JSONDecodeError:
        app.logger.error("Failed to decode templates.json!")
        return []

template_manifest = load_template_manifest()
template_lookup = {item['id']: item for item in template_manifest}

@app.route('/')
def index():
    return jsonify({"service": "eng-drafting", "status": "running", "templates_loaded": len(template_manifest)})

@app.route('/doc/render', methods=['POST'])
def render_document():
    data = request.get_json()
    if not data or 'template_id' not in data or 'data' not in data:
        return jsonify({"error": "Missing template_id or data in request"}), 400

    template_id = data['template_id']
    context = data['data']

    template_info = template_lookup.get(template_id)
    if not template_info:
        return jsonify({"error": f"Template with id '{template_id}' not found"}), 404

    # The 'target' path in templates.json is relative to the 'templates' dir.
    base_dir = os.path.dirname(os.path.abspath(__file__))
    template_path = os.path.join(base_dir, 'templates', template_info['target'])

    if not os.path.exists(template_path):
        return jsonify({"error": f"Template file not found at path: {template_path}"}), 500

    try:
        if template_path.endswith('.docx'):
            doc = DocxTemplate(template_path)
            doc.render(context)

            file_stream = io.BytesIO()
            doc.save(file_stream)
            file_stream.seek(0)

            return send_file(
                file_stream,
                as_attachment=True,
                download_name=os.path.basename(template_info['target']),
                mimetype='application/vnd.openxmlformats-officedocument.wordprocessingml.document'
            )

        elif template_path.endswith('.html'):
            template_dir = os.path.dirname(template_path)
            template_name = os.path.basename(template_path)

            template_loader = jinja2.FileSystemLoader(searchpath=template_dir)
            template_env = jinja2.Environment(loader=template_loader, autoescape=True)
            template = template_env.get_template(template_name)
            output_html = template.render(context)

            # Return raw HTML for service-to-service communication
            return output_html, 200, {'Content-Type': 'text/html; charset=utf-8'}

        else:
            return jsonify({"error": "Unsupported template format"}), 400

    except Exception as e:
        app.logger.error(f"Error rendering template {template_id}: {e}")
        return jsonify({"error": f"An error occurred while rendering the template: {str(e)}"}), 500


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
