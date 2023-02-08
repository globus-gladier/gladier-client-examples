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
            "from_source_transfer_source_endpoint_id": "ddb59aef-6d04-11e5-ba46-22000b92c6ec",
            "from_source_transfer_destination_endpoint_id": "9032dd3a-e841-4687-a163-2720da731b5b",
            "from_source_transfer_source_path": "/share/godata",
            "from_source_transfer_destination_path": "/nicks/godata",
            "from_source_transfer_recursive": True,
            # Tar the transferred input files
            "tar_input": "~/godata",
            "funcx_endpoint_compute": "553e7b64-0480-473c-beef-be762ba979a9",
            # Transfer the resulting tarfile
            "to_destination_transfer_source_endpoint_id": "9032dd3a-e841-4687-a163-2720da731b5b",
            "to_destination_transfer_destination_endpoint_id": "ddb59aef-6d04-11e5-ba46-22000b92c6ec",
            "to_destination_transfer_source_path": "/nicks/godata.tgz",
            "to_destination_transfer_destination_path": "~/godata.tgz",
            "to_destination_transfer_recursive": False,
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
