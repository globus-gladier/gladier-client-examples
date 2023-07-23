"""
Make sure you are part of the Globus Flows Users group so that you can deploy this flow,
or delete any prior flows before running this example.
"""
from gladier import (
    GladierBaseClient,
    JSONObject,
)
from gladier.tools.globus import GlobusComputeStep, ComputeFunctionType
from pprint import pprint
import typing as t


def compute_sum(a: int, b: int, **data) -> int:
    return a + b


class ComputeSumStep(GlobusComputeStep):
    function_to_call: ComputeFunctionType = compute_sum
    a: t.Union[
        str, int
    ] = 2  # By default, a will have a value of '2' if not specified as input
    b: t.Union[str, int] = "$.input.b"

    def get_flow_definition(self) -> JSONObject:
        # The model parameters a and b will be passed as arguments to the
        # function to invoke
        self.set_call_params_from_self_model(["a", "b"])
        return super().get_flow_definition()


if __name__ == "__main__":
    flow_input = {
        "input": {
            # 'a': 3,
            "b": 4,
            "globus_compute_endpoint": "4b116d3c-1703-4f8f-9f6f-39921e5864df",
        }
    }

    compute_sum_step = ComputeSumStep()

    # Instantiate the client
    compute_sum_client = GladierBaseClient(start_at=compute_sum_step)

    # Optionally, print the flow definition
    pprint(compute_sum_client.get_flow_definition())

    # Run the flow
    flow = compute_sum_client.run_flow(
        flow_input=flow_input, label="Custom Globus Compute Func Example"
    )

    # Track the progress
    run_id = flow["run_id"]
    compute_sum_client.progress(run_id)
    pprint(compute_sum_client.get_status(run_id))
