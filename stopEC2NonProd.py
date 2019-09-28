from __future__ import print_function
import json
import boto3
from botocore.exceptions import ClientError
region = 'us-west-2'
ec2 = boto3.resource('ec2', region_name=region)

# runs daily to check for instances that should
# be shut down to save money
# terminates spot instances
# stops running instances without the Stage:prod tag


def lambda_handler(event, context):
    print("Received event: " + json.dumps(event, indent=2))
    main()


def terminate_instance(instance_id):
    # terminates spot instances
    instance = ec2.Instance(instance_id)
    print('terminating instance: ' + instance_id)
    response = instance.terminate()
    print(response)
    return


def stop_instance(instance_id):
    instance = ec2.Instance(instance_id)
    print('stopping instance: ' + instance_id)
    response = instance.stop()
    print(response)
    return


# def lambda_handler(event, context):
def search_instances():
    try:
        # get instances in the running state
        # 1: look for spot instaances
        # 2: instances that aren't tagged in Stage:prod
        for instance in ec2.instances.all():
            if instance.state['Name'] == 'running':
                print('checking id: {0}'.format(instance.id))
                if instance.instance_lifecycle == 'spot':
                    print('spot instance ID: ' + instance.instance_id)
                    terminate_instance(instance.instance_id)
                else:
                    # check tags and shutdown if not Stage:prod
                    prod = {'Key': 'Stage', 'Value': 'prod'}
                    if prod not in instance.tags:
                        print('not tagged in Stage:prod')
                        print(instance.tags)
                        stop_instance(instance.id)
                    else:
                        # passes checks
                        print('passes checks - keep running')

    except ClientError as e:
        print(e)


def main():
    search_instances()


if __name__ == "__main__":
    main()
