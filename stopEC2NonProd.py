import boto3
region = 'us-west-2'

# assumes spot instances have been / are being terminated
# before running this function - see
# stopEC2Spot function
# get running instances without the Stage:prod tag
# shut down all instances that are non-prod


def lambda_handler(event, context):
    ec2 = boto3.client('ec2', region_name=region)

    # get list of instances in a running state
    stop_instances = []
    reservations = ec2.describe_instances(
        Filters=[
            {
                'Name': 'instance-state-name',
                'Values': [
                    'running',
                ],
            },
        ],
    ).get('Reservations', [])

    # get list of instances that do no have
    # the Stage:prod tag
    # these instances will be shutdown
    for reservation in reservations:
        for instance in reservation['Instances']:
            tags = {}
            # check for the case where there are no tags
            if instance.get('Tags') is not None:
                for tag in instance['Tags']:
                    tags[tag['Key']] = tag['Value']
                if ('Stage' not in tags or
                   tags['Stage'] not in ['prod', 'Prod']):
                    print("instance " + instance['InstanceId'] +
                          " does not have a Stage:prod tag")
                    stop_instances.append(instance['InstanceId'])
            # no tags, so add instance to stop list
            else:
                print("instance " + instance['InstanceId'] +
                      " does not have a Stage:prod tag")
                stop_instances.append(instance['InstanceId'])

    # stop non-prod instances
    if not stop_instances:
        print('there are no running non-prod instances')
    else:
        ec2.stop_instances(InstanceIds=stop_instances)
        print('stopped your instances: ' + str(stop_instances))
