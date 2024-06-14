from batch_processing import *
batch_name = "control"
example_format = """
    {
		"example_format_paperid": [
        "first_inspiration-source_id",
        "second_inspiration-source_id",
        "third_inspiration-source_id",
        etc
        ]
	}
"""
system_prompt = f"""
You are a classification AI that evaluates the inspiration-sources for xml formatted research papers.
A reference is considered a inspiration-source if it has significant impact on the xml paper's content.
So, you will read the xml paper to try to find which references are inspiration-sources.
Not all references will be inspiration-sources.
Each paper can have up to 5 inspiration-sources.
Example output format: {example_format}.
Follow the format exactly for the output, it should be a json object.
"""
user_prompt = "Identify the ref-sources."
process_method(batch_name, system_prompt, user_prompt)
