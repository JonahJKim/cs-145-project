from batch_processing import *
batch_name = "method3"
system_prompt = f"""
You are an AI assistant to help us identify inspiration-sources.
A reference is considered a inspiration-source if it has significant impact on the xml paper's content.
A paper can have 0, 1 of multiple inspiration-sources,
but most references are not inspiration sources.
You should consider every reference, and discuss why you think it is or is not an inspiration source.
"""
user_prompt = "Discuss all the references for the following paper, and why you believe they are or are not inspiration-sources."
process_method(batch_name, system_prompt, user_prompt)
