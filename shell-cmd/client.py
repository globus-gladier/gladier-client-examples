"""
Make sure you are part of the Globus Flows Users group so that you can deploy this flow,
or delete any prior flows before running this example.
"""
from gladier import GladierBaseClient, generate_flow_definition
from pprint import pprint


@generate_flow_definition
class ShellCmdClient(GladierBaseClient):
    gladier_tools = [
        "gladier_tools.posix.shell_cmd.ShellCmdTool",
    ]


if __name__ == "__main__":
    flow_input = {
        "input": {
            "args": "cat /proc/version",
            "capture_output": True,
            "funcx_endpoint_compute": "4b116d3c-1703-4f8f-9f6f-39921e5864df",
        }
    }
    # Instantiate the client
    shell_cmd_client = ShellCmdClient()

    # Optionally, print the flow definition
    pprint(shell_cmd_client.flow_definition)

    # Run the flow
    flow = shell_cmd_client.run_flow(flow_input=flow_input, label="Shell CMD Example")

    # Track the progress
    run_id = flow["run_id"]
    shell_cmd_client.progress(run_id)
    pprint(shell_cmd_client.get_status(run_id))
