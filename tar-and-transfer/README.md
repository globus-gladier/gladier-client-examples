## Tar And Transfer

The purpose of this client is to transfer files from a location, create an achive,
then transfer the result to another location. This approach uses existing tools
in the [Gladier Tools](https://gladier.readthedocs.io/en/latest/gladier_tools/index.html)
repository.

The two transfer tools in this flow use _aliases_, which is a Gladier feature for re-using
a tool multiple times in a flow.

### Requirements

**WARNING** This example requires a Compute Endpoint with connected Globus Storage! You will
not be able to complete this example without both of these things setup! See **[Setup Docs](https://gladier.readthedocs.io/en/latest/gladier/setup.html)**.

* A Python Environment with Gladier installed
* A Compute Endpoint with Globus accessible storage

The defaults within the client.py file do not demonstrate an environment where the compute endpoint and collection filesystems are shared. To do so, install [Globus Compute Endpoint](https://funcx.readthedocs.io/en/latest/endpoints.html) and [Globus Connect Personal](https://www.globus.org/globus-connect-personal) or use another environment where you have shell access with Globus accessible files.


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
