"""
Make sure you are part of the Globus Flows Users group so that you can deploy this flow,
or delete any prior flows before running this example.
"""
from gladier import GladierBaseClient, GladierBaseTool, generate_flow_definition
from pprint import pprint


def gather_metadata(publishv2, **data) -> dict:
    """
    This step is a custom funcx function to represent collecting
    metadata from 'custom datasets'. In this case, we also create the 'dataset' from
    scratch.
    """
    import pathlib
    import random
    import json
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
    metadata = pathlib.PosixPath(publishv2['metadata_file'])
    metadata.write_text(json.dumps({'project_metadata': {
            'number_of_hellos': num_hellos,
            'number_of_worlds': num_worlds,
        },
    }))


@generate_flow_definition
class GatherMetadata(GladierBaseTool):
    compute_functions = [gather_metadata]
    

def cleanup_files(publishv2, **data) -> dict:
    """Cleanup the files generated under gather_metadata"""
    import pathlib
    dataset = pathlib.PosixPath(publishv2['dataset'])
    (dataset / 'foo.txt').unlink()
    (dataset / 'bar.txt').unlink()
    (dataset / 'metadata.json').unlink()
    dataset.rmdir()


@generate_flow_definition
class CleanupFiles(GladierBaseTool):
    compute_functions = [cleanup_files]



@generate_flow_definition
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
                # This gets replaced by the UUID of the search index being used.
                # Create a new search index using the following:
                # globus search index create "my-index" "An index used for cataloging scientific data"
                'index': 'my-globus-search-index',
                'visible_to': ['public'],
                
                # Ingest and Transfer can be disabled for dry-run testing.
                'publish_enabled': False,
                'transfer_enabled': False,

                'enable_meta_dc': True,
                'enable_meta_files': True,
                # Use this to validate the 'dc' or datacite field metadata schema
                # Requires 'datacite' package
                # 'metadata_dc_validation_schema': 'schema43',
                # Custom metadata can be added here.
                'metadata_file': 'my_test_dataset/metadata.json',
                'metadata': {
                    'dc': {
                        'creators': [{'name': 'Lead Scientist'}],
                        'publisher': 'MyLaboratory',
                        'titles': [{'title': 'Hello World Dataset'}],
                    }
                }
            },
            # FuncX Test endpoint
            'compute_endpoint': '4b116d3c-1703-4f8f-9f6f-39921e5864df',
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
