import re
from time import strftime, localtime, mktime, time_ns
from flask import Flask, request
from num2words import num2words

app = Flask(__name__)

@app.route("/prepare", methods=['POST'])
def prepare():
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
        text = request.get_data(as_text=True)
        text_optimized = remove_trash(
            replace_hrules(
                replace_numerals(
                    replace_wattages(
                        replace_dollar_signs(text)
                    )
                )
            )
        )
        response["status"]["success"] = True
        response["status"]["message"] = "Fixed up dollar signs, watt-based units, decimal numbers, and h-rules; removed troublesome Unicode chars."
        response["status"]["duration"] = duration_ms(st)
        response["output"] = text_optimized
    except Exception as e:
        response["status"]["success"] = False
        response["status"]["message"] = repr(e)
        response["status"]["duration"] = duration_ms(st)
    return response

def duration_ms(start_ns):
    return str((time_ns() - start_ns) / 1000000)

# Some Unicode characters choke supertonic. Strip them.
def remove_trash(input_text):
    workpiece = input_text
    re.sub("\u2060", "", workpiece, flags=re.DOTALL)
    return workpiece

def replace_dollar_signs(input_text):
    # Case 1: A $42 billion debt
    workpiece = re.sub(
        "\\b(an?|the)\\s+\\$([0-9]+[0-9.]*)\\s+(million|billion|trillion)",
        "\\1 \\2-\\3 dollar",
        input_text,
        flags=re.DOTALL|re.IGNORECASE)
    input_text = workpiece
    # Case 2: A $5 footlong
    workpiece = re.sub(
        "\\b(an?|the)\\s+\\$([0-9]+[0-9.]*)\\s+(\\w+)",
        "\\1 \\2-dollar \\3",
        input_text,
        flags=re.DOTALL|re.IGNORECASE)
    input_text = workpiece
    # Case 3: It cost $1 million to fix
    workpiece = re.sub(
        "\\$([0-9]+[0-9.]*)\\s+(million|billion|trillion)",
        "\\1 \\2 dollars",
        input_text,
        flags=re.DOTALL|re.IGNORECASE)
    input_text = workpiece
    # Case 4: It cost $5 to fix
    workpiece = re.sub(
        "\\$([0-9]+[0-9.,]*)",
        "\\1 dollars",
        input_text,
        flags=re.DOTALL|re.IGNORECASE)
    return workpiece

def replace_wattages(input_text):
    workpiece = input_text
    workpiece = re.sub(
        "\\b([0-9.]+)\\s*mw\\b",
        "\\1 megawatt",
        workpiece,
        flags=re.DOTALL|re.IGNORECASE
    )
    workpiece = re.sub(
        "\\b([0-9.]+)\\s*mwh\\b",
        "\\1 megawatt-hour",
        workpiece,
        flags=re.DOTALL|re.IGNORECASE
    )
    workpiece = re.sub(
        "\\b([0-9.]+)\\s*gw\\b",
        "\\1 gigawatt",
        workpiece,
        flags=re.DOTALL|re.IGNORECASE
    )
    workpiece = re.sub(
        "\\b([0-9.]+)\\s*gwh\\b",
        "\\1 gigawatt-hour",
        workpiece,
        flags=re.DOTALL|re.IGNORECASE
    )
    return workpiece

def replace_numerals(input_text):
    num_pat = "\\b([0-9]+[0-9.,]*)\\b"
    workpiece = input_text
    num_match = re.search(num_pat, workpiece, re.DOTALL)
    while num_match:
        start_idx = num_match.start()
        end_idx = num_match.end()
        # num2words evidently can't handle embedded commas
        numbers = re.sub(",", "", num_match.group(0))
        # print(f"Replacing '{numbers}' at index {start_idx} – '{workpiece[start_idx-10:end_idx+10]}'")
        words = num2words(numbers)
        workpiece = workpiece[:start_idx] + words + workpiece[end_idx:]
        num_match = re.search(num_pat, workpiece, re.DOTALL)
    return workpiece

def replace_hrules(input_text):
    workpiece = input_text
    workpiece = re.sub("^[=]+$", "Heading:", workpiece, flags=re.MULTILINE)
    workpiece = re.sub("^[-]+$", "Sub-heading:", workpiece, flags=re.MULTILINE)
    return workpiece