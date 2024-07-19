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
    form_html = f'<form id="mainForm" name="mainForm" action="{json_data["form"]["action"]}" method="{json_data["form"]["method"]}">\n'
    form_html += '<div class="card-body">'
    for element in json_data["form"]["elements"]:
        form_html += generate_html_element(element)
    form_html += '</div>'
    form_html += """
    <div class="card-footer">
        <button class="btn btn-primary" type="submit">Submit</button>
    </div>
    """
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
            <input class="form-input" type="{element_type}" name="{element["name"]}" id="{element["name"]}" autocomplete="true" """
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
        html += f'<textarea id="{element["name"]}" name="{element["name"]}" class="form-input"\n'
        if "rows" in element and element["rows"]:
            html += f' rows="{element["rows"]}"'
        if "required" in element and element["required"]:
            html += ' required'
        html += ' ></textarea></div>\n'

    elif element_type == "select":
        html += '<div class="form-group">'
        html += f'<label class="form-label {label_style}">{element["label"]}</label>'
        html += f'<select name="{element["name"]}" id="{element["name"]}" class="form-select"\n'
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
            html += f'<input type="radio" id="{element["name"]}" name="{element["name"]}" value="{option["value"]}" />\n'
            html += f'<i class="form-icon"></i> {option["label"]}\n'
            html += f'</label>\n'
        html += '</div>\n'

    elif element_type == "checkbox":
        html += f'<div class="form-group">'
        html += f'<label class="form-switch">'
        html += f'<input type="checkbox" id="{element["name"]}" name="{element["name"]}" >\n'
        html += f'<i class="form-icon"></i> {element["label"]}\n'
        html += f'</label>\n'
        html += '</div>\n'

    elif element_type == "checkbox-tile":
        html += f'<div class="form-group">'
        html += f'<label class="form-label {label_style}">Sample</label>'
        html += f'</div>'
        html += f'<div class="tile-checkbox-container mb-2">'

        for check in element["checks"]:
            html += f'<div class="tile-checkbox mb-2">'
            html += f'    <input type="checkbox" id="{check["value"]}" name="{check["value"]}">'
            html += f'    <label for="{check["value"]}">{check["label"]}</label>'
            html += f'</div>'
        html += '</div>'

    elif element_type == "radio-tile":
        html += f'<div class="form-group">'
        html += f'<label class="form-label {label_style}">{element['label']}</label>'
        html += f'<div class="tile-radio-container mb-2">'
        for option in element["options"]:
            html += f'<div class="tile-radio mb-2 mt-2">'
            html += f'  <input type="radio" id="{option["value"]}" name="{element["name"]}" value="{option["value"]}">'
            html += f'  <label for="{option["value"]}">{option["label"]}</label>'
            html += f'</div>'

        html += '</div>'
        html += '</div>'

    elif element_type == 'list-tile':
        html += f'<div class="form-group">'
        html += f'<label class="form-label {label_style}">{element['label']}</label>'
        html += f'<div class="tile-list-container">'
        for item in element["items"]:
            html += f'<div class="tile-list-item">{item['label']}</div>'
        html += '</div>'
        html += '</div>'

    elif element_type == 'poll':
        
        html += f'<div class="form-group">'
        html += f'<label class="form-label {label_style}">{element['label']}</label>'
        html += f'<div class="tile-list-container">'

        for item in element["items"]:
            percentage = 100 * float(item['count'])/float(element['totalCount'])
            str_percentage = str(percentage) + "%"
            html += f'<div class="tile-list-item-sm">{item['label']}</div>'
            html += f"""<div class="bar bar-sm">
    <div class="bar-item" role="progressbar" style="width:{str_percentage};" aria-valuenow="{str(percentage)}" aria-valuemin="0" aria-valuemax="100"></div>
    </div>"""
        html += '</div>'
        html += '</div>'
    return html