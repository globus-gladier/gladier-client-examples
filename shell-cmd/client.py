"""
Make sure you are part of the Globus Flows Users group so that you can deploy this flow,
or delete any prior flows before running this example.
"""
from gladier import GladierBaseClient
from gladier.tools.posix import ShellCmdStep
from pprint import pprint


def main():
    flow_input = {
        "input": {
            "globus_compute_endpoint": "4b116d3c-1703-4f8f-9f6f-39921e5864df",
        }
    }
    shell_cmd_client = ShellCmdStep(
        cmd_args="cat /proc/version",
        capture_output=True,
    )

    shell_cmd_client = GladierBaseClient(start_at=shell_cmd_client)

    # Optionally, print the flow definition
    pprint(shell_cmd_client.get_flow_definition())

    # Run the flow
    flow = shell_cmd_client.run_flow(flow_input=flow_input, label="Shell CMD Example")

    # Track the progress
    run_id = flow["run_id"]
    shell_cmd_client.progress(run_id)
    pprint(shell_cmd_client.get_status(run_id))


if __name__ == "__main__":
    main()
