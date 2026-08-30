from time import time_ns
from flask import Flask, request
import html_text
import requests

app = Flask(__name__)

@app.route("/html_to_text", methods=['POST'])
def html_to_text():
    st = time_ns()
    response = {
        "status": {
            "success": False,
            "message": "",
            "duration": None
        },
        "output": ""
    }

    try:
        html = request.get_data(as_text=True)
        text = html_text.extract_text(html)

        response["status"]["success"] = True
        response["status"]["message"] = "Extracted plain text from HTML input."
        response["status"]["duration"] = duration_ms(st)
        response["output"] = text
    except Exception as e:
        response["status"]["success"] = False
        response["status"]["message"] = repr(e)
        response["status"]["duration"] = duration_ms(st)
    return response

def duration_ms(start_ns):
    return str((time_ns() - start_ns) / 1000000)