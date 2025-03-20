"""
Make sure you are part of the Globus Flows Users group so that you can deploy this flow,
or delete any prior flows before running this example.
"""

from gladier import GladierBaseClient, GladierBaseTool, generate_flow_definition
from pprint import pprint


def run_experiment(
    experiment_location: str = "my_experiment", iterations: int = 10, **data
) -> int:
    """
    This "experiment" generates a random number between 1 and 10 and writes it to a file.

    Failed experiments are written to the 'errors' directory.

    :param experiment_location: The location to write the experiment file
    :returns: The number of experiments run and the number of errors
    """
    import random
    import pathlib

    # Write the random number between 1 and 10 to a file
    basepath = pathlib.Path(experiment_location)
    errors = basepath / "errors"
    basepath.mkdir(exist_ok=True)
    errors.mkdir(exist_ok=True)
    filename = basepath / f"experiment_{random.randint(1, 10)}.txt"
    for _ in range(iterations):
        if filename.exists():
            (errors / f"{filename.name}").write_text(f"File {filename} already exists")
        else:
            filename.write_text("This is mock data representing an experiment")

    return {
        "num_experiments": len(list(basepath.glob("experiment_*.txt"))),
        "num_errors": len(list(errors.glob("error_*.txt"))),
    }


@generate_flow_definition
class RunExperiment(GladierBaseTool):
    compute_functions = [run_experiment]


class CheckExperiment(GladierBaseTool):
    flow_transition_states = [
        "CheckExperimentReportFailure",
        "CheckExperimentReportSuccess",
    ]
    flow_definition = {
        "Comment": "Determine if experiments should continue",
        "StartAt": "CheckExperimentChoice",
        "States": {
            "CheckExperimentChoice": {
                "Type": "Choice",
                "Choices": [
                    {
                        "Variable": "$.RunExperiment.details.results[0].output.num_errors",
                        "NumericGreaterThan": 2,
                        "Next": "CheckExperimentReportFailure",
                    },
                    {
                        "Variable": "$.RunExperiment.details.results[0].output.num_experiments",
                        "NumericGreaterThan": 5,
                        "Next": "CheckExperimentReportSuccess",
                    },
                ],
                "Default": "CheckExperimentReportFailure",
            },
            "CheckExperimentReportFailure": {
                "Type": "ExpressionEval",
                "Parameters": {
                    "status": "FAILURE",
                },
                "ResultPath": "$.CheckExperimentResults",
                "End": True,
            },
            "CheckExperimentReportSuccess": {
                "Type": "ExpressionEval",
                "Parameters": {
                    "status": "SUCCESS",
                },
                "ResultPath": "$.CheckExperimentResults",
                "End": True,
            },
        },
    }


@generate_flow_definition()
class ExperimentWorkflowClient(GladierBaseClient):
    gladier_tools = [
        RunExperiment,
        CheckExperiment,
    ]


if __name__ == "__main__":
    flow_input = {
        "input": {
            "compute_endpoint": "4b116d3c-1703-4f8f-9f6f-39921e5864df",
        }
    }
    # Instantiate the client
    experiment_workflow_client = ExperimentWorkflowClient()

    # Optionally, print the flow definition
    pprint(experiment_workflow_client.flow_definition)

    # Run the flow
    flow = experiment_workflow_client.run_flow(
        flow_input=flow_input, label="Experiment Workflow Client Example"
    )

    # Track the progress
    run_id = flow["run_id"]
    experiment_workflow_client.progress(run_id)
    pprint(experiment_workflow_client.get_status(run_id))
