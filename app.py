import json
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/mutate", methods=["POST"])
def mutate():
    request_data = request.get_json()
    pod = request_data["request"]["object"]
    
    # Patch to add label "mutated: true"
    patch = [{
        "op": "add", 
        "path": "/metadata/labels/mutated",
        "value": "true"
    }]
    
    admission_response = {
        "response": {
            "uid": request_data["request"]["uid"],
            "allowed": True,
            "patchType": "JSONPatch",
            "patch": json.dumps(patch).encode("utf-8").decode("utf-8")
        }
    }
    return jsonify(admission_response)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=443, ssl_context=("/certs/tls.crt", "/certs/tls.key"))
