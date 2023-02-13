# Gladier Client Examples

A set of standalone examples for completing common tasks in Gladier.

Each folder contains its own self-contained example with instructions on how to use it. The list of topics includes: 

* shell-cmd -- A simple example flow running a shell command on a remote funcx endpoint
* custom-funcx-function -- An example for using a flow with a custom funcx function
* tar-and-transfer -- A three step flow for transferring and tarring files with aliased inputs
* custom-tool-flow-definition -- An example for writing tools with custom flow definitions
* multi-function-pipeline -- Constructing flows where one step depends on another
* custom-auth -- A guide to running Gladier clients with external auth

### Deployment Restrictions

By default, Flows only allows one flow deployed per-user. Each of the examples above will attempt to
deploy a separate flow, and will raise an error on the second deployment. Two solutions exist:

1. Request access to the [Globus Flows Users](https://app.globus.org/groups/cdd90ec0-7030-11e9-948c-0ef301d936cc/about) group to deploy more than one at a time.
2. Delete your existing flow with `globus-automate flow list` and `globus-automate flow delete FLOW_ID`
