import json

def check_references(gpt_response, paper_json_str):
    gpt_response = gpt_response[gpt_response.find('{'):gpt_response.rfind('}')+1]
    paper_data = json.loads(paper_json_str)
    all_references = paper_data["references"]
    
    default_output = {paper_data["_id"]: [0] * len(all_references)}
    
    try:
        suggested_references = json.loads(gpt_response)
        
        if not isinstance(suggested_references, dict):
            return default_output
        
        for key, ref_list in suggested_references.items():
            if not isinstance(ref_list, list):
                return default_output
        
        output = {}
        for key, ref_list in suggested_references.items():
            reference_flags = [1 if ref in ref_list else 0 for ref in all_references]
            output[key] = reference_flags
        
        return output
    
    except (json.JSONDecodeError, KeyError, TypeError):
        return default_output

gpt_response_valid = """{
    "61dbf1dcd18a2b6e00d9f311": [
        "5b67b45517c44aac1c860876",
        "5e8d8e6d9fced0a24b5d669e",
        "53e9b253b7602d9703cf4028",
        "5736977f6e3b12023e66632b",
        "57aa28de0a3ac518da9896d5"
    ]
}"""

gpt_response_almost_valid = """Hola soy dora this is the almost close to correct output
{
    "61dbf1dcd18a2b6e00d9f311": [
        "5b67b45517c44aac1c860876",
        "5e8d8e6d9fced0a24b5d669e",
        "53e9b253b7602d9703cf4028",
        "5736977f6e3b12023e66632b",
        "57aa28de0a3ac518da9896d5"
    ]
}
yippeeee"""

gpt_response_invalid = """{
    "61dbf1dcd18a2b6e00d9f311": "invalid_format"
}"""

paper_json = """{
    "_id": "61dbf1dcd18a2b6e00d9f311",
    "title": "Automated Unsupervised Graph Representation Learning",
    "references": [
        "58437722ac44360f1082efeb",
        "5b67b45517c44aac1c860876",
        "5e8d8e6d9fced0a24b5d669e",
        "53e9b253b7602d9703cf4028",
        "5736977f6e3b12023e66632b",
        "57aa28de0a3ac518da9896d5",
        "5a260c8117c44a4ba8a30f54",
        "62376b725aee126c0f0a7412",
        "5bdc31b417c44a1f58a0b4e9",
        "5b8c9f4a17c44af36f8b6a96",
        "5d9edc8347c8f76646042a37",
        "5d4d46fb3a55acff992fde2b",
        "603e2f2191e01129ef28fecc",
        "5bdc319c17c44a1f58a0a1b7",
        "558ba88be4b00c3c48ddc0f3",
        "53e9b254b7602d9703cf70bb",
        "6001711bd4150a363c49b450",
        "5d3ed25a275ded87f97deba4",
        "5d3ed25a275ded87f97deb56",
        "5db929b747c8f766461fa94f",
        "53e9b527b7602d970405d9f8",
        "53e9b3fdb7602d9703ef0efb",
        "5e5e18b393d709897ce28ad3",
        "5e5e189a93d709897ce1e760",
        "53e9b3f5b7602d9703ee3407",
        "5cf48a40da56291d582a2f8e",
        "5e9661119fced0a24bb3f157",
        "53e9bd82b7602d9704a283df",
        "605058cc9e795e84274fd10f",
        "53e9b2ffb7602d9703dc29f7",
        "53e9a5afb7602d9702edacce",
        "53e9b6b4b7602d97042394bc",
        "53e9acc4b7602d97036a1037",
        "53e9b108b7602d9703b85b88",
        "58d82fcbd649053542fd67e0",
        "573695fd6e3b12023e511373",
        "57a4e91aac44365e35c97c6e",
        "5cfa5b985ced2477cb3c5175",
        "5b67b47917c44aac1c8637c6",
        "5ce2d032ced107d4c635260c",
        "5da2f8aa3a55ac3402d8c165",
        "5f993af691e011a3fbe2fb01",
        "60bdde338585e32c38af4f97",
        "5f6b5b0f91e011bf6740cc4a",
        "53e9b873b7602d9704442198",
        "5cede10eda562983788eea63",
        "58d82fc8d649053542fd59b8"
    ]
}"""

matched_refs_valid = check_references(gpt_response_valid, paper_json)
print("Valid Response Output:")
print(json.dumps(matched_refs_valid, indent=4))

matched_refs_almost_valid = check_references(gpt_response_almost_valid, paper_json)
print("Almost Valid Response Output:")
print(json.dumps(matched_refs_almost_valid, indent=4))

matched_refs_invalid = check_references(gpt_response_invalid, paper_json)
print("Invalid Response Output:")
print(json.dumps(matched_refs_invalid, indent=4))