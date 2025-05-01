import os
from flask import Flask, request, render_template
from google.cloud import storage
from datetime import datetime

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        frase = request.form["frase"]
        filename = datetime.now().strftime("%Y-%m-%d_%H-%M-%S.txt")
        file_path = os.path.join("/tmp", filename)
        steps = ""
        try:
            with open(file_path, "w") as f:
                f.write(frase)

            bucket_name = os.environ.get("GCP_BUCKET_NAME")
            if not bucket_name:
                return "Error: Variable de entorno GCP_BUCKET_NAME no está definida.", 500

            storage_client = storage.Client()
            steps += "Client created. "
            bucket = storage_client.bucket(bucket_name)
            steps += "Connect to bucket. "
            blob = bucket.blob(file_path)
            steps += "Blob created. "
            blob.upload_from_filename(file_path)
            steps += "Filename updated"

            return f"Frase guardada y subida al bucket {bucket_name}"
        except Exception as e:
            return f"Error: {e}. Target bucket: {bucket_name}. Steps: {steps}", 500

    return render_template("index.html"), 200

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
