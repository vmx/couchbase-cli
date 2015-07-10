# -- FILE: features/steps/example_steps.py
from behave import given, when, then, step

from codify import Control


@given('we have {number:d} nodes running')
def step_impl(context, number):
    print("check if {} nodes are running".format(number))

@when('we initialized a single node on "{node}"')
def step_impl(context, node):
    user = 'Administrator'
    password = 'asdasd'
    ssl = False
    host, port = node.split(':')
    context.control = Control(host, int(port), user, password, ssl)

    ramsize_data = 512
    ramsize_index = 512
    services = 'data'
    context.control.cluster_init(ramsize_data, ramsize_index, services)

@then('we add node "{node}" to the cluster')
def step_impl(context, node):
    server = {node: {'services': 'data'}}
    context.control.server_add(server)

@then('we rebalance the cluster')
def step_impl(context):
    context.control.rebalance()

@then('we load the "{dataset}" dataset')
def step_impl(context, dataset):
    print("vmx: dataset: {}".format(dataset))
    context.control.load_sample_data('travel-sample')

@then('we remove node "{node}" from the cluster')
def step_impl(context, node):
    context.control.server_remove([node])
