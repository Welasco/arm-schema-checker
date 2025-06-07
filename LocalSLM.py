## Imports
from huggingface_hub import hf_hub_download
from llama_cpp import Llama

## Download the GGUF model
#model_name = "microsoft/phi-4-gguf"
#model_file = "phi-4-Q4_K.gguf" # this is the specific model file we'll use in this example. It's a 4-bit quant, but other levels of quantization are available in the model repo if preferred

model_name = "unsloth/phi-4-GGUF"
model_file = "phi-4-Q4_K_M.gguf"

model_path = hf_hub_download(model_name, filename=model_file)

## Instantiate model from downloaded file
# llm = Llama(
#     model_path=model_path,
#     n_ctx=16000,  # Context length to use
#     n_threads=32,            # Number of CPU threads to use
#     n_gpu_layers=32       # Number of model layers to offload to GPU
# )

llm = Llama(
    model_path=model_path,
    n_ctx=16000,  # Context length to use
    n_gpu_layers=32       # Number of model layers to offload to GPU
)

# llm = Llama(
#     model_path=model_path
# )

# ## Generation kwargs
# generation_kwargs = {
#     "max_tokens":20000,
#     "stop":["</s>"],
#     "echo":False, # Echo the prompt in the output
#     "top_k":1 # This is essentially greedy decoding, since the model will always return the highest-probability token. Set this value > 1 for sampling decoding
# }

# ## Run inference
# prompt = "The meaning of life is "
# res = llm(prompt, **generation_kwargs) # Res is a dictionary

# ## Unpack and the generated text from the LLM response dictionary and print it
# print(res["choices"][0]["text"])
# # res is short for result

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

[{
  "id": "https://schema.management.azure.com/schemas/2023-03-01/Microsoft.AlertsManagement.json#",
  "title": "Microsoft.AlertsManagement",
  "description": "Microsoft AlertsManagement Resource Types",
  "$schema": "http://json-schema.org/draft-04/schema#",
  "resourceDefinitions": {
    "prometheusRuleGroups": {
      "description": "Microsoft.AlertsManagement/prometheusRuleGroups",
      "properties": {
        "apiVersion": {
          "enum": [
            "2023-03-01"
          ],
          "type": "string"
        },
        "location": {
          "description": "The geo-location where the resource lives",
          "type": "string"
        },
        "name": {
          "description": "The name of the rule group.",
          "oneOf": [
            {
              "pattern": "^[^:@/#{}%&+*<>?]+$",
              "type": "string"
            },
            {
              "$ref": "https://schema.management.azure.com/schemas/common/definitions.json#/definitions/expression"
            }
          ]
        },
        "properties": {
          "description": "The Prometheus rule group properties of the resource.",
          "oneOf": [
            {
              "$ref": "#/definitions/PrometheusRuleGroupProperties"
            },
            {
              "$ref": "https://schema.management.azure.com/schemas/common/definitions.json#/definitions/expression"
            }
          ]
        },
        "tags": {
          "description": "Resource tags.",
          "oneOf": [
            {
              "additionalProperties": {
                "type": "string"
              },
              "properties": {},
              "type": "object"
            },
            {
              "$ref": "https://schema.management.azure.com/schemas/common/definitions.json#/definitions/expression"
            }
          ]
        },
        "type": {
          "enum": [
            "Microsoft.AlertsManagement/prometheusRuleGroups"
          ],
          "type": "string"
        }
      },
      "required": [
        "name",
        "properties",
        "apiVersion",
        "type"
      ],
      "type": "object"
    }
  },
  "definitions": {
    "PrometheusRule": {
      "description": "An Azure Prometheus alerting or recording rule.",
      "properties": {
        "actions": {
          "description": "Actions that are performed when the alert rule becomes active, and when an alert condition is resolved.",
          "oneOf": [
            {
              "items": {
                "$ref": "#/definitions/PrometheusRuleGroupAction"
              },
              "type": "array"
            },
            {
              "$ref": "https://schema.management.azure.com/schemas/common/definitions.json#/definitions/expression"
            }
          ]
        },
        "alert": {
          "description": "Alert rule name.",
          "type": "string"
        },
        "annotations": {
          "description": "The annotations clause specifies a set of informational labels that can be used to store longer additional information such as alert descriptions or runbook links. The annotation values can be templated.",
          "oneOf": [
            {
              "additionalProperties": {
                "type": "string"
              },
              "properties": {},
              "type": "object"
            },
            {
              "$ref": "https://schema.management.azure.com/schemas/common/definitions.json#/definitions/expression"
            }
          ]
        },
        "enabled": {
          "description": "Enable/disable rule.",
          "oneOf": [
            {
              "type": "boolean"
            },
            {
              "$ref": "https://schema.management.azure.com/schemas/common/definitions.json#/definitions/expression"
            }
          ]
        },
        "expression": {
          "description": "The PromQL expression to evaluate. https://prometheus.io/docs/prometheus/latest/querying/basics/. Evaluated periodically as given by 'interval', and the result recorded as a new set of time series with the metric name as given by 'record'.",
          "type": "string"
        },
        "for": {
          "description": "The amount of time alert must be active before firing.",
          "type": "string"
        },
        "labels": {
          "description": "Labels to add or overwrite before storing the result.",
          "oneOf": [
            {
              "additionalProperties": {
                "type": "string"
              },
              "properties": {},
              "type": "object"
            },
            {
              "$ref": "https://schema.management.azure.com/schemas/common/definitions.json#/definitions/expression"
            }
          ]
        },
        "record": {
          "description": "Recorded metrics name.",
          "type": "string"
        },
        "resolveConfiguration": {
          "description": "Defines the configuration for resolving fired alerts. Only relevant for alerts.",
          "oneOf": [
            {
              "$ref": "#/definitions/PrometheusRuleResolveConfiguration"
            },
            {
              "$ref": "https://schema.management.azure.com/schemas/common/definitions.json#/definitions/expression"
            }
          ]
        },
        "severity": {
          "description": "The severity of the alerts fired by the rule. Must be between 0 and 4.",
          "oneOf": [
            {
              "type": "integer"
            },
            {
              "$ref": "https://schema.management.azure.com/schemas/common/definitions.json#/definitions/expression"
            }
          ]
        }
      },
      "required": [
        "expression"
      ],
      "type": "object"
    },
    "PrometheusRuleGroupAction": {
      "description": "An alert action. Only relevant for alerts.",
      "properties": {
        "actionGroupId": {
          "description": "The resource id of the action group to use.",
          "type": "string"
        },
        "actionProperties": {
          "description": "The properties of an action group object.",
          "oneOf": [
            {
              "additionalProperties": {
                "type": "string"
              },
              "properties": {},
              "type": "object"
            },
            {
              "$ref": "https://schema.management.azure.com/schemas/common/definitions.json#/definitions/expression"
            }
          ]
        }
      },
      "type": "object"
    },
    "PrometheusRuleGroupProperties": {
      "description": "An Azure Prometheus rule group.",
      "properties": {
        "clusterName": {
          "description": "Apply rule to data from a specific cluster.",
          "type": "string"
        },
        "description": {
          "description": "Rule group description.",
          "type": "string"
        },
        "enabled": {
          "description": "Enable/disable rule group.",
          "oneOf": [
            {
              "type": "boolean"
            },
            {
              "$ref": "https://schema.management.azure.com/schemas/common/definitions.json#/definitions/expression"
            }
          ]
        },
        "interval": {
          "description": "The interval in which to run the Prometheus rule group represented in ISO 8601 duration format. Should be between 1 and 15 minutes",
          "type": "string"
        },
        "rules": {
          "description": "Defines the rules in the Prometheus rule group.",
          "oneOf": [
            {
              "items": {
                "$ref": "#/definitions/PrometheusRule"
              },
              "type": "array"
            },
            {
              "$ref": "https://schema.management.azure.com/schemas/common/definitions.json#/definitions/expression"
            }
          ]
        },
        "scopes": {
          "description": "Target Azure Monitor workspaces resource ids. This api-version is currently limited to creating with one scope. This may change in future.",
          "oneOf": [
            {
              "items": {
                "type": "string"
              },
              "type": "array"
            },
            {
              "$ref": "https://schema.management.azure.com/schemas/common/definitions.json#/definitions/expression"
            }
          ]
        }
      },
      "required": [
        "scopes",
        "rules"
      ],
      "type": "object"
    },
    "PrometheusRuleResolveConfiguration": {
      "description": "Specifies the Prometheus alert rule configuration.",
      "properties": {
        "autoResolved": {
          "description": "Enable alert auto-resolution.",
          "oneOf": [
            {
              "type": "boolean"
            },
            {
              "$ref": "https://schema.management.azure.com/schemas/common/definitions.json#/definitions/expression"
            }
          ]
        },
        "timeToResolve": {
          "description": "Alert auto-resolution timeout.",
          "type": "string"
        }
      },
      "type": "object"
    }
  }
}]
"""

response = llm.create_chat_completion(
    messages=[
        {
            "role": "system",
            "content": system_prompt,
        },
        {
            "role": "user",
            "content": user_prompt,
        },
    ],
    response_format={
        "type": "json_object",
    },
    temperature=0.7,
)

print(response["choices"][0]["message"]["content"])
