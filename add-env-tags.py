import boto3

ec2_client_tokyo = boto3.client('ec2', region_name="ap-northeast-1")
ec2_client_other = boto3.client('ec2', region_name="ap-假裝是其他的-1")

instance_id_paris = []
instance_id_other = []

reservations_paris = ec2_client_tokyo.describe_instances()['Reservations']
for res in reservations_paris:
    instances = res['Instances']
    for ins in instances:
        instance_id_paris.append(ins['InstanceId'])


response = ec2_client_tokyo.create_tags(
    Resources=instance_id_paris,
    Tags=[
        {
            'Key': 'environment',
            'Value': 'prod'
        },
    ]
)

#針對其他Region的:
reservations_other = ec2_client_other.describe_instances()['Reservations']
for res in reservations_other:
    instances = res['Instances']
    for ins in instances:
        instance_id_other.append(ins['InstanceId'])


response = ec2_client_other.create_tags(
    Resources=instance_id_other,
    Tags=[
        {
            'Key': 'environment',
            'Value': 'dev'
        },
    ]
)