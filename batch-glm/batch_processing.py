import json, os, time
from zhipuai import ZhipuAI

## connection details for glm
API_KEY = os.getenv("API_KEY")
client = ZhipuAI(api_key=API_KEY)
query_interval_time = 20

## data files
data_dir = "data/PST"
xml_dir = f"{data_dir}/paper-xml"

# json array of paper metadata
paper_source_trace_valid_wo_ans = f"{data_dir}/paper_source_trace_valid_wo_ans.json"
paper_json_array_fd = open(paper_source_trace_valid_wo_ans, "r")
paper_json_array = json.load(paper_json_array_fd)

def batch_input_filename(batch_name: str) -> str:
    return f"{batch_name}-input.jsonl"

def batch_output_filename(batch_name: str) -> str:
    return f"{batch_name}-output.jsonl"

def create_batch_file(batch_name: str, system_prompt: str, user_prompt: str):
    batch_file = open(batch_input_filename(batch_name), "a")
    for paper_json in paper_json_array:
        paper_id = paper_json.get('_id')
        xml_paper = f"{xml_dir}/{paper_id}.xml"
        xml_paper_contents = open(xml_paper).read()
        request_json = {
          "custom_id": f"request-{batch_name}-{paper_id}",
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

def create_batch(batch_filename: str) -> str:
    result = client.files.create(
        file=open(batch_filename, "rb"),
        purpose="batch"
    )
    create = client.batches.create(
     input_file_id=str(result.id),
     endpoint="/v1/chat/completions",
     completion_window="24h",
    )
    print(f"{create}\n")
    return create.id

def parse_batch_results(batch_id: str, batch_name: str):
    response = client.batches.retrieve(batch_id)
    while response.status != "completed":
        print(f"{response}\n")
        time.sleep(query_interval_time)
    print(f"Done! - {response}\n")
    print(f"output_file_id = {response.output_file_id}")
    content = client.files.content(str(response.output_file_id))
    content.write_to_file(batch_output_filename(batch_name))

def process_method(batch_name: str, system_prompt: str, user_prompt: str):
    create_batch_file(batch_input_filename(batch_name), system_prompt, user_prompt)
    batch_id = create_batch(batch_input_filename(batch_name))
    parse_batch_results(batch_id, batch_name)
