from batch_processing import *
batch_name = "method2"
system_prompt = f"""
You are an AI assistant that reads papers and summarizes them in a couple paragraphs.
Your audience is familiar with the field and well educated in computer science.
"""
user_prompt = "Provide an in depth summary for this paper."
process_method(batch_name, system_prompt, user_prompt)
