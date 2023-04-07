## Publish

The Publish tooling is used for cataloging data on a Globus Collection into Globus Search
for easy access. This is typically used in cases where data has just been processed, and
needs to be moved into a location where it can be viewed by others.

This client examples takes the common use-case, where directories are published from a
staging collection to another collection for sharing with collaborators. The high level
logic happens in three steps:

* Gather metadata on dataset
* Publish dataset
* Cleanup dataset on staging collection

The Gather and Cleanup steps are defined within client.py. Publish is contained within the
`gladier_tools.publish.Publishv2` tool.

See documentatin on writing [Gladier Tools here](https://gladier.readthedocs.io/en/latest/gladier/tools.html).

### Requirements

* A Python Environment with Gladier installed

#### Optional Dependencies

* `datacite` -- For validating the 'dc' or datacite metadata block, if desired
* `puremagic` -- An alternative for more reliable mimetype detection


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
