import boto3
region = 'us-west-2'

# assumes spot instances have been / are being terminated
# before running this function - see
# stopEC2Spot function
# get running instances with Stage:prod tag
# shut down all instances that are non-prod


def lambda_handler(event, context):
    ec2 = boto3.client('ec2', region_name=region)

    # get list of instances in a running state
    # that have a Stage:prod key/value pair
    # these instances will not be shut down
    prod_instance_ids = []
    prod_reservations = ec2.describe_instances(
        Filters=[
            {
                'Name': 'instance-state-name',
                'Values': [
                    'running',
                ]
            },
            {
                'Name': 'tag:Stage',
                'Values': [
                    'prod',
                ]
            },
        ],
    ).get('Reservations', [])
    # print(prod_reservations)
    # create a list of instances with the Stage:prod tag
    for prod_reservation in prod_reservations:
        for instance in prod_reservation['Instances']:
            prod_instance_ids.append(instance['InstanceId'])
    # print(prod_instance_ids)

    # get all running instances
    stop_instances = []
    reservations = ec2.describe_instances(
        Filters=[
            {
                'Name': 'instance-state-name',
                'Values': [
                    'running',
                ]
            },
        ],
    ).get('Reservations', [])
    for reservation in reservations:
        for instance in reservation['Instances']:
            if instance['InstanceId'] not in prod_instance_ids:
                stop_instances.append(instance['InstanceId'])
                print(instance['InstanceId'] + " added to stop list")
    # stop non-prod instances
    ec2.stop_instances(InstanceIds=stop_instances)
    print('stopped your instances: ' + str(stop_instances))
