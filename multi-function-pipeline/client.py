"""
Make sure you are part of the Globus Flows Users group so that you can deploy this flow,
or delete any prior flows before running this example.
"""
from gladier import GladierBaseClient, GladierBaseTool, generate_flow_definition
from typing import List, Mapping
from pprint import pprint


def generate_numbers(random_numbers: int = 10, **data) -> Mapping:
    import random

    return {"numbers": [random.randint(0, 100) for _ in range(random_numbers)]}


@generate_flow_definition
class GenerateNumbersTool(GladierBaseTool):
    """
    Generate a list of random numbers. Generates 10 by default
    """

    compute_functions = [generate_numbers]
    required_input = ["compute_endpoint"]


def average_numbers(numbers: List[int], **data) -> int:
    return sum(numbers) / len(numbers)


@generate_flow_definition
class AverageNumbersTool(GladierBaseTool):
    """Average a list of numbers"""

    compute_functions = [average_numbers]
    required_input = ["compute_endpoint"]


class ReportResultsTool(GladierBaseTool):
    """
    This tool reports the results from two specific states. Note: the values in 'echo_string' below
    are not checked by Gladier or Flows prior to running. If the state info does not exist, the flow
    will fail. Both $.GenerateNumbers.details.result[0].numbers and $.AverageNumbers.details.result[0]
    must exist as flow state information.
    """

    flow_definition = {
        "StartAt": "ReportResults",
        "States": {
            "ReportResults": {
                "ActionUrl": "https://actions.globus.org/hello_world",
                "Type": "Action",
                "Parameters": {
                    "echo_string.=": "'Result from averaging: ' + "
                    "str(GenerateNumbers.details.results[0].output.numbers) + "
                    "' is equal to ' + str(AverageNumbers.details.results[0].output) ",
                },
                "End": True,
            }
        },
    }


@generate_flow_definition(
    modifiers={"average_numbers": {"payload": "$.GenerateNumbers.details.results[0].output"}}
)
class MultiFunctionClient(GladierBaseClient):
    """
    Generate numbers, average them, then report the results.

    The 'AverageNumbersTool' creates an average by taking the result from the output
    of the 'GenerateNumbersTool'. Both 'GenerateNumbersTool' and 'ReportResultsTool'
    are generic and can be run separately. 'ReportResultsTool' is crafted specifically
    for this flow, and will result in a failure if run without the others.
    """

    gladier_tools = [
        GenerateNumbersTool,
        AverageNumbersTool,
        ReportResultsTool,
    ]


if __name__ == "__main__":
    flow_input = {
        "input": {
            "compute_endpoint": "4b116d3c-1703-4f8f-9f6f-39921e5864df",
        }
    }
    # Instantiate the client
    multi_function_client = MultiFunctionClient()

    # Optionally, print the flow definition
    pprint(multi_function_client.flow_definition)

    # Run the flow
    flow = multi_function_client.run_flow(
        flow_input=flow_input, label="Multi-Function Client Example"
    )

    # Track the progress
    run_id = flow["run_id"]
    multi_function_client.progress(run_id)
    pprint(multi_function_client.get_status(run_id))
