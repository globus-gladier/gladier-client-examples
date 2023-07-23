"""
Make sure you are part of the Globus Flows Users group so that you can deploy this flow,
or delete any prior flows before running this example.
"""
from gladier import GladierBaseClient, GladierBaseTool, generate_flow_definition
from gladier.tools.globus import GlobusComputeStep, ComputeFunctionType
from pprint import pprint


def gather_metadata(publishv2, **data) -> dict:
    """
    This step is a custom funcx function to represent collecting
    metadata from 'custom datasets'. In this case, we also create the 'dataset' from
    scratch.
    """
    import pathlib
    import random

    # Create the dataset files used for publication. Also create some interesting
    # unique fields to track within Globus Search.
    dataset = pathlib.PosixPath(publishv2['dataset'])
    dataset.mkdir(exist_ok=True)
    num_hellos, num_worlds = random.randint(1, 100), random.randint(1, 100)
    foo = dataset / 'foo.txt'
    foo.write_text('Hello ' * num_hellos)
    bar = dataset / 'bar.txt'
    bar.write_text('World!' * num_worlds)

    # List the unique 'num_hellos' and 'num_worlds' items within metadata, so it
    # can be catalogued within Globus Search.
    extra_metadata = {
        'project_metadata': {
            'number_of_hellos': num_hellos,
            'number_of_worlds': num_worlds,
        },
    }
    publishv2['metadata'].update(extra_metadata)
    return publishv2


class GatherMetadataStep(GlobusComputeStep):
    function_to_call: ComputeFunctionType = gather_metadata
    
@generate_flow_definition
class GatherMetadata(GladierBaseTool):
    funcx_functions = [gather_metadata]
    

def cleanup_files(publishv2, **data) -> dict:
    """Cleanup the files generated under gather_metadata"""
    import pathlib
    dataset = pathlib.PosixPath(publishv2['dataset'])
    (dataset / 'foo.txt').unlink()
    (dataset / 'bar.txt').unlink()
    dataset.rmdir()


class CleanupFilesStep(GlobusComputeStep):
    function_to_call: ComputeFunctionType = cleanup_files
    
@generate_flow_definition
class CleanupFiles(GladierBaseTool):
    funcx_functions = [cleanup_files]



@generate_flow_definition(modifiers={
    # publishv2_gather_metadata uses funcx_endpoint_non_compute, so our other custom functions
    # will also use this endpoint.
    'gather_metadata': {'endpoint': 'funcx_endpoint_non_compute'},
    'cleanup_files': {'endpoint': 'funcx_endpoint_non_compute'},
    # Make the Publishv2 Tool get its metadata from the result of the custom GatherMetadata
    # function above.
    'publishv2_gather_metadata': {'payload': '$.GatherMetadata.details.result[0]'},
})
class PublicationTestClient(GladierBaseClient):
    gladier_tools = [
        GatherMetadata,
        'gladier_tools.publish.Publishv2',
        CleanupFiles,
    ]


if __name__ == "__main__":
    flow_input = {
        "input": {
            'publishv2': {
                'dataset': '/home/funcx/my_test_dataset',
                'destination': 'my/remote/path',
                'source_collection': 'my-source-collection-uuid',
                'source_collection_basepath': '',
                'destination_collection': 'my-destination-collection-uuid',
                'index': 'my-globus-search-index',
                'visible_to': ['public'],
                
                # Ingest and Transfer are disabled by default for dry-run testing.
                # 'ingest_enabled': True,
                # 'transfer_enabled': True,

                'enable_meta_dc': True,
                'enable_meta_files': True,
                # Use this to validate the 'dc' or datacite field metadata schema
                # Requires 'datacite' package
                # 'metadata_dc_validation_schema': 'schema43',
                # Custom metadata can be added here.
                'metadata': {
                    'dc': {
                        'creators': [{'name': 'Lead Scientist'}],
                        'publisher': 'MyLaboratory',
                        'titles': [{'title': 'Hello World Dataset'}],
                    }
                }
            },
            # FuncX Test endpoint
            'funcx_endpoint_non_compute': '4b116d3c-1703-4f8f-9f6f-39921e5864df',
        }
    }
    # Instantiate the client
    pub_test_client = PublicationTestClient()

    # Optionally, print the flow definition
    pprint(pub_test_client.flow_definition)

    # Run the flow
    flow = pub_test_client.run_flow(
        flow_input=flow_input, label="Publication Test"
    )

    # Track the progress
    run_id = flow["run_id"]
    pub_test_client.progress(run_id)
    pprint(pub_test_client.get_status(run_id))
