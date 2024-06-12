from batch_processing import *

batch_name = "test"
batch_filename = "test.jsonl"

result = client.files.create(
    file=open(batch_filename, "rb"),
    purpose="batch"
)

batch_id = create_batch(batch_filename)
parse_batch_results(batch_id, batch_name)
