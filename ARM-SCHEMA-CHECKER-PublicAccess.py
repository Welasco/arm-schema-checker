import os
import time
import logging
from openai import AzureOpenAI
import logging
from settings import get_settings

settings = get_settings()

logging.basicConfig(filename='ARM-SCHEMA-CHECKER-PublicAccess.log', level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s')

endpoint = settings.Endpoint
model_name = settings.model
deployment = settings.deployment
subscription_key = settings.api_key
api_version = settings.version

client = AzureOpenAI(
    api_version=api_version,
    azure_endpoint=endpoint,
    api_key=subscription_key,
)

def read_file(file_path):
    with open(file_path, "r", encoding='utf-8') as f:
        content = f.read()
        return content

def save_file(file_path, content):
    with open(file_path, "w") as f:
        f.write(content)
        f.close()

folder_path = "C:\\Local-Projects\\arm-schema-checker\\workingfolder\\schemasToValidate"
response_folder = "C:\\Local-Projects\\arm-schema-checker\\workingfolder\\responsesPublicAccess"
fileTime = time.strftime("%Y%m%d%H%M%S")

system_prompt = """You are analyzing an Azure ARM API schema in JSON format. Your task is to determine whether the resource provider described in the file supports any form of public access control.
Look for properties such as publicNetworkAccess, allowPublicAccess, networkAccess, or any other configuration that enables or restricts public access to the resource.
If such a property exists, return the property name, its location in the schema, and a brief explanation of how it controls public access.
If no such property is found, clearly state that the schema does not appear to support public access control.
Return your findings in this JSON format:
{
  "publicAccessControlSupported": true,
  "propertyPath": "properties.publicNetworkAccess",
  "description": "This property controls whether the resource is accessible over the public internet."
}

Or, if not supported:
{
  "publicAccessControlSupported": false,
  "reason": "No properties related to public access control were found in the schema."
}
"""

user_prompt = """Please analyze the following Azure ARM API schema and determine if it supports form of public access control.
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
        response = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": system_prompt,
                },
                {
                    "role": "user",
                    "content": content_prompt,
                }
            ],
            temperature=1.0,
            top_p=1.0,
            model=deployment
        )
        #print(response.choices[0].message.content)
        save_file(os.path.join(response_folder, file + "-" + fileTime + ".response.txt"), response.choices[0].message.content)
        logging.info(f"--------------------------------------------------")
        #print("--------------------------------------------------")
    except Exception as e:
        logging.error(f"Error processing file {file}: {e}")
        print(f"Error processing file {file}: {e}")
        save_file(os.path.join(response_folder, file + "-" + fileTime + ".error.txt"), str(e))
        #print("--------------------------------------------------")
        logging.info(f"--------------------------------------------------")

