"""
Make sure you are part of the Globus Flows Users group so that you can deploy this flow,
or delete any prior flows before running this example.
"""
from gladier import GladierBaseClient, GladierBaseTool, generate_flow_definition
from pprint import pprint


class HelloTool(GladierBaseTool):
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
                "ResultPath": "$.Hello"
            }
        },
    }
    required_input = ["echo_string", "sleep_time"]
    flow_input = {
        "sleep_time": 1,
    }


@generate_flow_definition
class HelloClient(GladierBaseClient):
    gladier_tools = [HelloTool]


if __name__ == "__main__":
    # Instantiate the client
    hello_client = HelloClient()

    # Run the flow
    flow_input = {"input": {"echo_string": "Hello World!"}}
    flow = hello_client.run_flow(flow_input=flow_input, label="Hello World Example")

    # Track the progress
    run_id = flow["run_id"]
    hello_client.progress(run_id)
    pprint(hello_client.get_status(run_id))
