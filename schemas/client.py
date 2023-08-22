"""
Make sure you are part of the Globus Flows Users group so that you can deploy this flow,
or delete any prior flows before running this example.
"""
from gladier import GladierBaseClient
from pprint import pprint


class HelloWorldClient(GladierBaseClient):
    flow_definition = {
        "StartAt": "Hello",
        "States": {
            "Hello": {
                "ActionUrl": "https://actions.globus.org/hello_world",
                "Type": "Action",
                "Parameters": {
                    "echo_string.$": "$.input.echo_string",
                    "sleep_time.$": "$.input.sleep_time",
                },
                "End": True,
            }
        },
    }

    flow_schema = {
        "required": [
            "input"
        ],
        "properties": {
            "input": {
                "type": "object",
                "required": [
                    "echo_string",
                ],
                "properties": {
                    "echo_string": {
                        "type": "string",
                        "title": "A string to echo back",
                        "description": "The echo string can be any string type vaule",
                        "additionalProperties": False
                    },
                    "sleep_time": {
                        "type": "integer",
                        "title": "The amount of time to wait before echoing back the string",
                        "description": "This can be any numeric value",
                        "default": 1,
                        "additionalProperties": False
                    }
                },
                "additionalProperties": False
            }
        },
        "additionalProperties": False
    }


if __name__ == "__main__":
    flow_input = {
        "input": {
            "echo_string": "hello_world",
            "sleep_time": 1
        }
    }
    # Instantiate the client
    hello_world_client = HelloWorldClient()
    hello_world_client.sync_flow()
    url = f'https://app.globus.org/flows/{hello_world_client.get_flow_id()}'
    print(f'You can run the flow from the Globus Webapp here: {url}')

    # Run the flow and track progress.
    # This step may still be done via Gladier.
    flow = hello_world_client.run_flow(flow_input=flow_input, label="Schema Example")
    run_id = flow["run_id"]
    hello_world_client.progress(run_id)
    pprint(hello_world_client.get_status(run_id))
