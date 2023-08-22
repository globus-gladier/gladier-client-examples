## Schemas

This example demonstrates running a simple flow with a flow schema to aid flow runners
in starting a flow, by documenting and validating input fields as part of a flow. Flow
schemas are optional, but recommended for any flows where new users may not be familiar
with the internals of the flow and/or prefer starting flows from the webapp, which has
extra support for rendering nice schemas.

### Requirements

* A Python Environment with Gladier installed

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
