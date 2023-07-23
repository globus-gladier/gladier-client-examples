"""
Make sure you are part of the Globus Flows Users group so that you can deploy this flow,
or delete any prior flows before running this example.
"""
import typing as t
from pprint import pprint

from gladier import ActionState, GladierBaseClient


class HelloState(ActionState):
    action_url: str = "https://actions.globus.org/hello_world"
    echo_string: str = "$.input.echo_string"
    sleep_time: t.Union[str, int] = 1


if __name__ == "__main__":
    # Instantiate the client
    hello_client = GladierBaseClient(start_at=HelloState())

    # Run the flow
    flow_input = {"input": {"echo_string": "Hello World!"}}
    flow = hello_client.run_flow(flow_input=flow_input, label="Hello World Example")

    # Track the progress
    run_id = flow["run_id"]
    hello_client.progress(run_id)
    pprint(hello_client.get_status(run_id))
