import json
import subprocess

import logic

def snake_case(name):
    return ''.join(['_' + i.lower() if i.isupper() else i for i in name]).lstrip('_')

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

    html_form = logic.generate_html(json_data)
    new_output = open("index.html", "w")
    new_output.write(html_form)
    new_output.close()

    csharp_class = logic.generate_csharp_class(json_data)
    new_output = open(f"{json_data["backend"]["model"]}.cs", "w")
    new_output.write(csharp_class)
    new_output.close()

    print("Form generation completed.")
    start_server()


if __name__ == '__main__':
    main()