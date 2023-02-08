## Custom Tool Flow Definition

This example demonstrates using a custom flow definition 
on Gladier Tools. Gladier will detect any changes to the final
flow definition and re-deploy it as needed.

See documentatin on writing [Custom Flows in Gladier here](https://gladier.readthedocs.io/en/latest/gladier/flow_generation.html).

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
