## Multi-Function Pipeline

Sometimes it can be useful to chain functions, using the output from one FuncX function
as the input to another. Globus Flows allows doing so by selecting input from the desired
location in the flow to be used by other flow states.

Input is passed between states in two different ways:

* Using Gladier 'modifiers' to dynamically change the flow definition of a funcx function
* Manually, by crafting a flow_definition which assumes state information on a flow

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
