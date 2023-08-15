import openai


class Functions:
    @property
    def functions_list(self):
        functions = [
            {
                "name": "search_pubmed",
                "description": "Retrieve biomedicine articles from PubMed.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "Keywords to be retrieved",
                        },
                    },
                    "required": ["query"],
                },
            }
        ]
        return functions


def chat(messages, functions, model, temperature=0):
    chat_res = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        functions=functions,
        temperature=0,
    )
    return chat_res
