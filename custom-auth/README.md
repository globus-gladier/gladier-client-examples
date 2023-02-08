## Custom Auth

This example demonstrates a custom auth model. Instead
of Glaider handling auth flows internally, Auth will be fully
controlled by the custom external application. Gladier will
raise events when it requires a login for a new scope.

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
