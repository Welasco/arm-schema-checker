import os
import time
#from openai import AzureOpenAI
import logging
from huggingface_hub import hf_hub_download
from llama_cpp import Llama

logging.basicConfig(filename='ARM-SCHEMA-CHECKER-SLM.log', level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s')

model_name = "unsloth/phi-4-GGUF"
model_file = "phi-4-Q4_K_M.gguf"

model_path = hf_hub_download(model_name, filename=model_file)

llm = Llama(
    model_path=model_path,
    n_ctx=16000,  # Context length to use
    n_gpu_layers=32       # Number of model layers to offload to GPU
)

def read_file(file_path):
    with open(file_path, "r", encoding='utf-8') as f:
        content = f.read()
        return content

def save_file(file_path, content):
    with open(file_path, "w") as f:
        f.write(content)
        f.close()

#folder_path = "C:\\Local-Projects\\arm-schema-checker\\workingfolder\\schemasToValidate"
folder_path = "C:\\Local-Projects\\arm-schema-checker\\workingfolder\\schemasToValidateTest"
#folder_path = "C:\\Local-Projects\\arm-schema-checker\\workingfolder\\schemasToValidateErrors"
#response_folder = "C:\\Local-Projects\\arm-schema-checker\\workingfolder\\responsesErrors"
response_folder = "C:\\Local-Projects\\arm-schema-checker\\workingfolder\\responsesSLM"
fileTime = time.strftime("%Y%m%d%H%M%S")

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
    logging.info(f"Processing file: {os.path.join(folder_path, file)}")
    print(os.path.join(folder_path, file))

    try:
        content_prompt = user_prompt.replace("[{{json_schema_content}}]", read_file(os.path.join(folder_path, file)))
        content_prompt = user_prompt.replace("[{{json_schema_content}}]", read_file(os.path.join(folder_path, file)))
        response = llm.create_chat_completion(
            messages=[
                {
                    "role": "system",
                    "content": system_prompt,
                },
                {
                    "role": "user",
                    "content": content_prompt,
                },
            ],
            response_format={
                "type": "json_object",
            },
            temperature=0.7,
        )
        #print(response.choices[0].message.content)
        save_file(os.path.join(response_folder, file + "-" + fileTime + ".response.txt"), response["choices"][0]["message"]["content"])
        logging.info(f"--------------------------------------------------")
        #print("--------------------------------------------------")
    except Exception as e:
        logging.error(f"Error processing file {file}: {e}")
        print(f"Error processing file {file}: {e}")
        save_file(os.path.join(response_folder, file + "-" + fileTime + ".error.txt"), str(e))
        #print("--------------------------------------------------")
        logging.info(f"--------------------------------------------------")

