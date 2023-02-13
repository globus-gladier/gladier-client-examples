"""
Make sure you are part of the Globus Flows Users group so that you can deploy this flow,
or delete any prior flows before running this example.
"""
from gladier import GladierBaseClient, GladierBaseTool, generate_flow_definition
from pprint import pprint


def compute_sum(a: int, b: int, **data) -> int:
    return a + b


@generate_flow_definition
class ComputeSum(GladierBaseTool):
    """
    Compute two numbers and return the result. Requires the following flow input:

    a: (optional, defaults to 2): first integer to add
    b: second integer to add
    funcx_endpoint_compute: Funcx endpoint used to compute these values
    returns: the computed result
    """

    funcx_functions = [compute_sum]
    required_input = [
        "a",
        "b",
        "funcx_endpoint_compute",
    ]
    # By default, a will have a value of '2' if not specified as input
    flow_input = {"a": 2}


@generate_flow_definition
class ComputeSumClient(GladierBaseClient):
    gladier_tools = [
        ComputeSum,
    ]


if __name__ == "__main__":
    flow_input = {
        "input": {
            # 'a': 3,
            # 'b': 2,
            "funcx_endpoint_compute": "4b116d3c-1703-4f8f-9f6f-39921e5864df",
        }
    }
    # Instantiate the client
    shell_cmd_client = ComputeSumClient()

    # Optionally, print the flow definition
    pprint(shell_cmd_client.flow_definition)

    # Run the flow
    flow = shell_cmd_client.run_flow(
        flow_input=flow_input, label="Custom FuncX Func Example"
    )

    # Track the progress
    run_id = flow["run_id"]
    shell_cmd_client.progress(run_id)
    pprint(shell_cmd_client.get_status(run_id))
