import os
import tiktoken

def num_tokens_from_string(prompt: str, encoding_name: str) -> int:
    encoding = tiktoken.get_encoding(encoding_name)
    num_tokens = len(encoding.encode(prompt))
    return num_tokens

def read_file(file_path):
    with open(file_path, "r", encoding='utf-8') as f:
        content = f.read()
        return content

folder_path = "C:\\Local-Projects\\arm-schema-checker\\workingfolder\\schemasToValidate"
#folder_path = "C:\\Local-Projects\\arm-schema-checker\\workingfolder\\schemasToValidateErrors"

system_prompt = """You are evaluating an Azure ARM API schema in JSON format.
Your task is to determine whether the resource provider described in the file supports IP address-based access control (e.g., IP allowlists, firewall rules, network ACLs).
The property names and structure may vary between services. Search for any properties or configurations that suggest IP filtering, network rules, or access control based on IP addresses.
If found, identify the relevant property name(s), their location in the schema, and describe how they enable IP-based access control.
If no such functionality is found, clearly state that the schema does not appear to support IP-based access control.
Return your findings in a structured format like this:
{
  "ipAccessControlSupported": true,
  "propertyPath": "properties.networkAcls.ipRules",
  "description": "This property allows defining IP rules to restrict access to the service."
}

Or, if not supported:
{
  "ipAccessControlSupported": false,
  "reason": "No properties related to IP filtering or network access control were found in the schema."
}
"""
user_prompt = """Please analyze the following Azure ARM API schema and determine if it supports IP address-based access control.
If it does, provide details on the relevant properties and their purpose.

JSON Schema:
------------

[{{json_schema_content}}]
"""

for file in os.listdir(folder_path):
    print(os.path.join(folder_path, file))
    content_user_prompt = user_prompt.replace("[{{json_schema_content}}]", read_file(os.path.join(folder_path, file)))
    num_tokens_system = num_tokens_from_string(system_prompt, "o200k_base")
    num_tokens_user = num_tokens_from_string(content_user_prompt, "o200k_base")
    total_tokens = num_tokens_system + num_tokens_user
    print(f"File: {file}, System Prompt Tokens: {num_tokens_system}, User Prompt Tokens: {num_tokens_user}, Total Tokens: {total_tokens}")

#print(num_tokens_from_string("Hello world, let's test tiktoken.", "o200k_base"))