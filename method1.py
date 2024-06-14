from batch_processing import *
batch_name = "method1"
system_prompt = f"""
You are an AI assistant that reads papers and extracts background information.
Your audience are educated in computer science, so point out the topics this paper focuses on,
and which topics this paper was influenced by.
"""
user_prompt = "Provide key background information for this paper."
process_method(batch_name, system_prompt, user_prompt)
