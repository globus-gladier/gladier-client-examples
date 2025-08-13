## Containers

Run Gladier Tool compute functions inside a container. 

### Configuration.

Containers need to be both manually built and the Globus Compute endpoint needs to be configured
to allow containers. See the following documentation for [Configuring a Compute Endpoint](https://globus-compute.readthedocs.io/en/latest/tutorials/dynamic_containers.html).

### Gladier Configuration

Currently, you need to specify two things in a Gladier Tool. The first is using the v3 action provider, which is
done with the `action_provider` attribute on a Gladier Tool class like below:

```
class ScatterPlotTool(GladierBaseTool):

    action_url = "https://compute.actions.globus.org/v3"
```

Second, the apropriate modifiers need to be set. This example uses the following:

```
@generate_flow_definition(
    modifiers={
        "make_scatter_plot": {
            "user_endpoint_config": {
                "container_type": "podman",
                "container_uri": "ghcr.io/globus-gladier/gladier-client-examples/containers-example:latest",
                "container_cmd_options": "-v /tmp:/tmp",
            }
        }
    },
)
```

Note that ``container_type`` and ``container_uri`` are examples chosen by this example, and may differ for your compute endpoint. A comparable configuration would look like this (`user_config_template.yaml.j2`):


```
display_name: My Containerized Endpoint
engine:
  type: GlobusComputeEngine
  container_type: {{ container_type }}
  container_uri: {{ container_uri }}
  container_cmd_options: {{ container_cmd_options|default() }}
```

For more information, see [Compute Container Configuration](https://globus-compute.readthedocs.io/en/latest/tutorials/dynamic_containers.html)

### Setup

Run the following to setup your environment:

```
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Running

To deploy and run the flow, point your python shell at ``client.py``

```
python client.py
```