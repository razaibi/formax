import json
import subprocess
from datetime import date
from jinja2 import Environment

environment = Environment()

def generate_html(json_data):
    f = open('template.j2','r')
    content = f.read()
    template = environment.from_string(content)
    rendered_template = template.render(
        form=json_data['form'],
        formHolder=generate_html_form(json_data)
    )
    return rendered_template

def generate_html_form(json_data):
    form_html = f'<form action="{json_data["form"]["action"]}" method="{json_data["form"]["method"]}" onsubmit="formPost(event);">\n'
    for element in json_data["form"]["elements"]:
        form_html += generate_html_element(element)
    form_html += '</form>'
    return form_html

def generate_html_element(element):
    html = ""
    label_style = ""
    if "labelStyle" in element:
            label_style = f'{element["labelStyle"]}'
    element_type = element.get("type")
    if element_type in ["text", "password", "email", "tel", "number", "date", "url", "file", "color"]:
        html += f"""<div class="form-group">
            <label class="form-label {label_style}" for="{element["name"]}">{element["label"]}</label>
            <input class="form-input" type="{element_type}" id="{element["name"]}" """
        if "placeholder" in element:
            html += f' placeholder="{element["placeholder"]}"'
        if "required" in element and element["required"]:
            html += ' required'
        if element_type == "date":
            element_value = date.today().strftime("%Y-%m-%d")
            html += f' value="{element_value}"'
        html += ' ></input>'
        if "hint" in element and element["hint"]:
            html += f'<p class="form-input-hint">{element["hint"]}</p>'
        html += '</div>\n'

    elif element_type == "textarea":
        html += '<div class="form-group">'
        html += f'<label class="form-label {label_style}">{element["label"]}</label>'
        html += f'<textarea class="form-input"\n'
        if "rows" in element and element["rows"]:
            html += f' rows="{element["rows"]}"'
        if "required" in element and element["required"]:
            html += ' required'
        html += ' ></textarea></div>\n'

    elif element_type == "select":
        html += '<div class="form-group">'
        html += f'<label class="form-label {label_style}">{element["label"]}</label>'
        html += f'<select class="form-select"\n'
        if "multiple" in element and element["multiple"]:
            html += ' multiple'
        html += '>'
        for option in element["options"]:
            html += f'<option value="{option["value"]}">{option["label"]}</label>\n'
        html += '</select>\n'
        html += '</div>\n'

    elif element_type == "radio":
        html += f'<div class="form-group">\n'
        html += f'<label class="form-label {label_style}">{element["label"]}</label>\n'
        for option in element["options"]:
            html += f'<label class="form-radio">\n'
            html += f'<input type="radio" name="{element["name"]}" value="{option["value"]}" />\n'
            html += f'<i class="form-icon"></i> {option["label"]}\n'
            html += f'</label>\n'
        html += '</div>\n'

    elif element_type == "checkbox":
        html += f'<div class="form-group">'
        html += f'<label class="form-switch">'
        html += f'<input type="checkbox" >\n'
        html += f'<i class="form-icon"></i> {element["label"]}\n'
        html += f'</label>\n'
        html += '</div>\n'
    return html

def get_python_command():
    """
    Determine if 'python3' or 'python' should be used.
    """
    for cmd in ['python3', 'python']:
        try:
            subprocess.run([cmd, '--version'], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            return cmd
        except (subprocess.CalledProcessError, FileNotFoundError):
            continue
    raise EnvironmentError("Neither 'python3' nor 'python' command is available on this system.")

def start_server():
    command = "-m http.server"
    python_cmd = get_python_command()
    full_command = [python_cmd] + command.split()
    try:
        print("Starting server...")
        result = subprocess.run(full_command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print("Command Output:\n", result.stdout.decode())
    except subprocess.CalledProcessError as e:
        print("Error executing command:\n", e.stderr.decode())

def main():
    f = open(f'data.json')
    json_data = json.load(f)
    html_form = generate_html(json_data)

    new_output = open("index.html", "w")
    new_output.write(html_form)
    new_output.close()
    print("Form generation completed.")
    start_server()


if __name__ == '__main__':
    main()