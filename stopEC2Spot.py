iimport boto3
region = 'us-west-2'

# find spot instances
# these have to be terminated not stopped


def lambda_handler(event, context):
    ec2 = boto3.client('ec2', region_name=region)
    spot_instances = []
    spot_reservations = ec2.describe_instances(
        Filters=[
            {
                'Name': 'instance-lifecycle',
                'Values': [
                    'spot',
                ]
            },
        ]
    ).get('Reservations', [])
    for spot_reservation in spot_reservations:
        for instance in spot_reservation['Instances']:
            spot_instances.append(instance['InstanceId'])
            print('ID:' + instance['InstanceId'])

    # terminate instances
    if not spot_instances:
        print('there are no running spot instances')
    else:
        ec2.terminate_instances(InstanceIds=spot_instances)
        print('terminated your instances: ' + str(spot_instances))
