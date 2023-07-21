"""
Make sure you are part of the Globus Flows Users group so that you can deploy this flow,
or delete any prior flows before running this example.
"""
from gladier import (
    GladierBaseClient,
    GladierBaseTool,
    generate_flow_definition,
    ActionState,
)
from gladier.tools.globus import GlobusComputeStep
from typing import List, Mapping
from pprint import pprint


def generate_numbers(random_numbers: int = 10, **data) -> Mapping:
    import random

    return {"numbers": [random.randint(0, 100) for _ in range(random_numbers)]}


def average_numbers(numbers: List[int], **data) -> float:
    return sum(numbers) / len(numbers)


def create_client():
    generate_numbers_step = GlobusComputeStep(
        state_name="GenerateNumbers", function_to_call=generate_numbers
    )
    average_numbers_step = GlobusComputeStep(
        state_name="AverageNumbers",
        function_to_call=average_numbers,
        function_parameters={
            "numbers": generate_numbers_step.path_to_return_val() + ".numbers"
        },
    )
    report_results_step = ActionState(
        action_url="https://actions.globus.org/hello_world",
        state_name="ReportResults",
        parameters={
            "echo_string.=": (
                "'Result from averaging: ' + "
                f"str({generate_numbers_step.path_to_return_val()[2:]}.numbers) + "
                f"' is equal to ' + str({average_numbers_step.path_to_return_val()[2:]}) "
            ),
        },
    )

    generate_numbers_step.next(average_numbers_step).next(report_results_step)
    client = GladierBaseClient(start_at=generate_numbers_step)
    return client


if __name__ == "__main__":
    flow_input = {
        "input": {
            "globus_compute_endpoint": "4b116d3c-1703-4f8f-9f6f-39921e5864df",
        }
    }
    # Instantiate the client
    multi_function_client = create_client()

    # Optionally, print the flow definition
    pprint(multi_function_client.get_flow_definition())

    # Run the flow
    flow = multi_function_client.run_flow(
        flow_input=flow_input, label="Multi-Function Client Example"
    )

    # Track the progress
    run_id = flow["run_id"]
    multi_function_client.progress(run_id)
    pprint(multi_function_client.get_status(run_id))
