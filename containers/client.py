from gladier import GladierBaseClient, GladierBaseTool, generate_flow_definition
import typing as t
from pprint import pprint


def make_scatter_plot(
    x: t.List[int], y: t.List[int], name: str = "scatter_plot.png", **data
):
    import pathlib
    import plotly.express as px

    # Make the plot
    fig = px.scatter(x=x, y=y)
    fig.write_image(name)

    # Return the filename
    return str(pathlib.Path(name).absolute())


@generate_flow_definition(
    modifiers={
        "make_scatter_plot": {
            "user_endpoint_config": {
                "container_type": "podman",
                "container_uri": "ghcr.io/globus-gladier/gladier-client-examples/containers-example:latest",
            }
        }
    },
)
class ScatterPlotTool(GladierBaseTool):

    action_url = "https://compute.actions.globus.org/v3"
    compute_functions = [make_scatter_plot]
    flow_input = {
        "x": [1, 2, 3, 4, 5],
        "y": [2, 4, 8, 16, 32],
    }


@generate_flow_definition
class ScatterPlotClient(GladierBaseClient):
    gladier_tools = [
        ScatterPlotTool,
    ]


if __name__ == "__main__":
    # Create the client
    csc = ScatterPlotClient()
    pprint(csc.flow_definition)
    flow_input = {
        "input": {
            # The tutorial endpoint won't work unfortunately, you will need your own Compute Endpoint
            # That supports containers.
            # "compute_endpoint": "4b116d3c-1703-4f8f-9f6f-39921e5864df"
        }
    }

    # Run the flow
    flow = csc.run_flow(flow_input=flow_input, label="Create Scatter Plot")

    # Track the progress
    run_id = flow["run_id"]
    csc.progress(run_id)
    pprint(csc.get_status(run_id))
