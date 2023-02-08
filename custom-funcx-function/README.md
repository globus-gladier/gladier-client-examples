## Custom FuncX Function

This module defines a custom FuncX Function to use as part of the flow.
The function can be freely modified between flows, and Glaider will
re-register the function if it detects changes.

See documentatin on writing [Gladier Tools here](https://gladier.readthedocs.io/en/latest/gladier/tools.html).

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
