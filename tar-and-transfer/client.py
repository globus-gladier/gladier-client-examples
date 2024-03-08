"""
Make sure you are part of the Globus Flows Users group so that you can deploy this flow,
or delete any prior flows before running this example.
"""
from gladier import GladierBaseClient, generate_flow_definition
from pprint import pprint


@generate_flow_definition
class TarAndTransfer(GladierBaseClient):
    gladier_tools = [
        "gladier_tools.globus.Transfer:FromSource",
        "gladier_tools.posix.Tar",
        "gladier_tools.globus.Transfer:ToDestination",
    ]


if __name__ == "__main__":
    flow_input = {
        "input": {
            # Transfer input files
            "from_source_transfer_source_endpoint_id": "0121789b-df0e-43fb-b9f0-d0cd1b0ced7d",
            "from_source_transfer_destination_endpoint_id": "0121789b-df0e-43fb-b9f0-d0cd1b0ced7d",
            "from_source_transfer_source_path": "/source_files",
            "from_source_transfer_destination_path": "/staging_files",
            "from_source_transfer_recursive": True,
            # Tar the transferred input files
            "tar_input": "test",
            "compute_endpoint": "4b116d3c-1703-4f8f-9f6f-39921e5864df",
            # Transfer the resulting tarfile
            "to_destination_transfer_source_endpoint_id": "0121789b-df0e-43fb-b9f0-d0cd1b0ced7d",
            "to_destination_transfer_destination_endpoint_id": "0121789b-df0e-43fb-b9f0-d0cd1b0ced7d",
            "to_destination_transfer_source_path": "/staging_files",
            "to_destination_transfer_destination_path": "/destination_files",
            "to_destination_transfer_recursive": True,
        }
    }
    # Instantiate the client
    tar_and_transfer = TarAndTransfer()

    # Optionally, print the flow definition
    pprint(tar_and_transfer.flow_definition)

    # Run the flow
    flow = tar_and_transfer.run_flow(
        flow_input=flow_input, label="Tar And Transfer Example"
    )

    # Track the progress
    run_id = flow["run_id"]
    tar_and_transfer.progress(run_id)
    pprint(tar_and_transfer.get_status(run_id))
