import json, os, time
import settings
import xml.etree.ElementTree as ET
from zhipuai import ZhipuAI

## connection details for glm
API_KEY = os.getenv("API_KEY")
client = ZhipuAI(api_key=API_KEY)

def batch_input_filename(batch_name: str) -> str:
    return f"{batch_name}-input.jsonl"

def batch_output_filename(batch_name: str) -> str:
    return f"{batch_name}-output.jsonl"

def create_batch_file(batch_name: str, system_prompt: str, user_prompt: str):
    print("Creating batch file...")
    ## data files
    data_dir = "../data/PST"
    xml_dir = f"{data_dir}/paper-xml"
    # json array of paper metadata
    paper_source_trace_valid_wo_ans = f"{data_dir}/paper_source_trace_valid_wo_ans.json"
    paper_json_array_fd = open(paper_source_trace_valid_wo_ans, "r")
    paper_json_array = json.load(paper_json_array_fd)
    if os.path.exists(batch_input_filename(batch_name)):
        os.remove(batch_input_filename(batch_name))
    batch_file = open(batch_input_filename(batch_name), "a")
    for paper_json in paper_json_array:
        paper_id = paper_json.get('_id')
        xml_paper = f"{xml_dir}/{paper_id}.xml"
        xml_paper_contents = open(xml_paper).read()
        request_json = {
          "custom_id": f"{paper_id}",
          "method": "POST",
          "url": "/v4/chat/completions",
          "body": {
            "model": "glm-4",
            "messages": [
              {
                "role": "system",
                "content": f"{system_prompt}"
              },
              {
                "role": "user",
                "content": f"{user_prompt} xml-paper: \n { xml_paper_contents }\n\n json: { paper_json }"
              }
            ]
          }
        }
        json_string = json.dumps(request_json, ensure_ascii=False, separators=(',', ':'))
        batch_file.write(json_string + '\n')
    print("Writing batch file...")
    print("Batch file finished building...")

def create_batch(batch_filename: str) -> str:
    print("Creating batch...")
    result = client.files.create(
        file=open(batch_filename, "rb"),
        purpose="batch"
    )
    print("Submitting batch...")
    create = client.batches.create(
     input_file_id=str(result.id),
     endpoint="/v4/chat/completions",
     completion_window="24h",
    )
    print(f"{create}\n")
    return create.id

def get_batch_results(batch_id: str, batch_name: str):
    query_interval_time = 20
    response = client.batches.retrieve(batch_id)
    while response.status != "completed":
        print(f"{response}\n")
        time.sleep(query_interval_time)
    print(f"Done! - {response}\n")
    print(f"output_file_id = {response.output_file_id}")
    content = client.files.content(str(response.output_file_id))
    content.write_to_file(batch_output_filename(batch_name))

def process_jsonl_file(file_path):
    with open(file_path, 'r') as file:
        for line_number, line in enumerate(file, start=1):
            try:
                json_object = json.loads(line)
                id = json_object.get('custom_id')
                choices = json_object.get('response', {}).get('choices', [])
                new_data = choices[0].get('message', {}).get('content')
                xml_paper = f"{settings.DATA_DIR}/{id}.xml"
                ## FIXME: @sam idk what the correct directories are for this stuff
                # write new_data to body section of xml
                if os.path.exists(xml_paper):
                    tree = ET.parse(xml_paper)
                    root = tree.getroot()
                    body = root.find('.//body')
                    if body is not None:
                        if body.text:
                            body.text += f"\n{new_data}"
                        else:
                            body.text = new_data
                        tree.write(xml_paper, encoding='utf-8', xml_declaration=True)
                        print(f"Updated XML file: {xml_paper}")
                    else:
                        print(f"No body section found in XML file: {xml_paper}")
                else:
                    print(f"XML file not found: {xml_paper}")

            except json.JSONDecodeError as e:
                print(f"Error decoding JSON on line {line_number}: {e}")

def process_method(batch_name: str, system_prompt: str, user_prompt: str):
    create_batch_file(batch_name, system_prompt, user_prompt)
    batch_id = create_batch(batch_input_filename(batch_name))
    get_batch_results(batch_id, batch_name)
