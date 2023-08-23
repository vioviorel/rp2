import yaml
import boto3
from datetime import datetime, time

ec2_client = boto3.client('ec2')
def start_ec2(ec2_instance):
    ec2.start_instances(InstanceIds=ec2_instance)
    return
    #print('started your instances: ' + str(instances))


yaml_data = """
unec2:
    service_type: ec2
    enabled: false
    ec2_instance: ['i-0c90b3bb3dbc26695','i-99999']
    start_time: 4
    end_time: 18
sdfsdf:
    service_type: rds
    enabled: True
    db_cluster_name: ['database-1','database-2']
    start_time: 5
    end_time: 18
 

"""

# 'i-0b65d8de2e0257a75'
# first check type and if value exist.
# sec check if enabled: and value exist
# if type = ecs ( check if include key and value for service  and ecs_cluster_name)
# if type = ec2 ( check if include key instance_id )
# if type = rds ( check if include key db_cluster_name )

# default function will check mandatory like type and enabled.
# to add multiple instance for the same

data = yaml.safe_load(yaml_data)

item_data = yaml.safe_load(yaml_data)

#rrr = data.get([])

# Function to check if 'start_time' is a number between 0 and 10 for an item
def check_start_time(item_data):
    start_time = item_data.get('start_time')
    if isinstance(start_time, (int, float)) and 0 <= start_time <= 24:
        return True
    return False

# Function to check if 'end_time' is a number between 0 and 10 for an item
def check_end_time(item_data):
    end_time = item_data.get('end_time')
    if isinstance(end_time, (int, float)) and 0 <= end_time <= 24:
        return True
    return False


# Function to check if keys 'instance_type' and 'service_type' exist with defined values for an item
def check_keys_and_values(item_data):
    service_type = item_data.get('service_type')
    #enabled = item_data.get('enabled')
    return service_type


# Function to check if keys 'instance_type' and 'service_type' exist with defined values for an item
def check_keys_and_values_db_cluster_name(item_data):
    db_cluster_name = item_data.get('db_cluster_name')
    return db_cluster_name



def is_string(value):
    return isinstance(value, str)

    
# Function to check if 'enabled' is True or False for an item
def is_enabled(item_name):
    enabled = data.get(item_name, {}).get('enabled')
    if isinstance(enabled, bool):
        return enabled
    return None


def is_time_between(start_time, end_time, check_time=None):
    if check_time is None:
        check_time = datetime.now().time()

    return start_time <= check_time <= end_time

# Function to check if 'instance_id' is empty for a given item

rds_client = boto3.client('rds')

#def rds_stop():
#    rds_client = boto3.client('rds')
#    for rds_cluster_id in rds_clusters_to_stop
#    rds_client.stop_db_cluster(DBClusterIdentifier=rds_cluster_id)
 

for item_name, item_data in data.items():
    #cluster_name = item_data.get('cluster_name')
    service_type = item_data.get('service_type')
    enabled = item_data.get('enabled')
    ec2_instance = item_data.get('ec2_instance')
    db_cluster_name = item_data.get('db_cluster_name')

    start_time = item_data.get('start_time')
    end_time = item_data.get('end_time')
    #srv = next(iter(item))
    #service_info = item[srv]
    #service_type = service_info['service_type']
    #cluster_name  = service_info['cluster_name']
    #instance_id = service_info['instance_id']

    # Check for 'instance_type' and 'service_type' with defined values
    # Iterate through items and check keys/values
 
    #if check_keys_and_values(item_data) and check_start_time(item_data):
    if check_keys_and_values(item_data):
        print("aaa")
        # pass checking of service_type and enable fields.
        print(service_type)

        enabled = is_enabled(item_name)
        if enabled is not None:
            if enabled:
                #print(f"'{item_name}' is enabled (True).")
                #print("true",service_type)

                if service_type == "ec2":
                    print("this is ec2")
                    
                    if isinstance(ec2_instance, list):
                        print(f"'{item_name}' has a string value for '{ec2_instance}'.")
                        # if here hour
                        #ec2_client.stop_instances(InstanceIds=asdasd)
                        # Check if the current time is between the specified times
                        # Define the start and end times
                        start_time = time(start_time, 0)  # 9:00 AM
                        end_time = time(end_time, 0)   # 5:00 PM

                        if is_time_between(start_time, end_time):
                            print(ec2_instance)
                            print("The current time is between {} and {}.".format(start_time, end_time))
                            ec2_client.start_instances(InstanceIds=ec2_instance)
                            # check if is running and do nothing if is running # add checkpoint here
                            # add for multiple instances then replicate for rds.
                        else:
                            print("The current time is outside the specified range.")
                            # check if is in shutdown state and shutdown if is not in shutdown state
                            #ec2_client.stop_instances(InstanceIds=[instance_id])
                            try:
                                # Check the state of each instance and stop if it's running
                                for instance_id in ec2_instance:
                                    response = ec2_client.describe_instances(InstanceIds=[instance_id])
                                    instance = response['Reservations'][0]['Instances'][0]
                                    state = instance['State']['Name']

                                    if state == 'running':
                                        print(f"Instance {instance_id} is running.")
                                        print("It's outside of business hours, stopping the instance.")
                                        ec2_client.stop_instances(InstanceIds=[instance_id])
                                    else:
                                        print(f"Instance {instance_id} is not running.")


                            except Exception as e:
                                print(f"Error checking instance {ec2_instance} state: {str(e)}")

                    else:
                        print(f"'{item_name}' does not have a string value for '{ec2_instance}'.")
                        

                rds = boto3.client('rds', region_name='eu-west-1')  # Replace with your region
                if service_type == "rds":
                    #print("this is rds")
                    if check_keys_and_values_db_cluster_name(item_data):
                        print("db cluster name is defined")
                        start_time = time(start_time, 0)  # 9:00 AM
                        end_time = time(end_time, 0)   # 5:00 PM

                        if is_time_between(start_time, end_time):
               
                            print("The current time is between {} and {}.".format(start_time, end_time))
                            try:
                                # aici verifica db_type - cluster or instance

                                # Loop through the list and stop each RDS cluster
                                rds = boto3.client('rds', region_name='eu-west-1')  # Replace with your region
                                for cluster_identifier in db_cluster_name:
                                    response = rds.describe_db_instances(DBInstanceIdentifier=cluster_identifier)
                                    db_instance = response['DBInstances'][0]
                                    print(cluster_identifier)
                                    # Get the instance status
                                    instance_status = db_instance['DBInstanceStatus']
                                    print(instance_status)
                                    if instance_status == 'stopped':
                                        print("The DB instance is stopped. so we start the instance")
                                        response = rds.start_db_instance(
                                            DBInstanceIdentifier=cluster_identifier
                                        )

                                    if instance_status == 'available':
                                        print('DB Instance {0} The DB instance is healthy and available.')
                                        #Error stopping RDS clusters: An error occurred (InvalidDBInstanceState) when calling the StartDBInstance operation: Instance database-1 cannot be started as it is not in one of the following statuses: 'stopped, inaccessible-encryption-credentials-recoverable'.
                                    if instance_status == 'starting':
                                        print('DB Instance {0} The DB instance is starting..')
                                        #Error stopping RDS clusters: An error occurred (InvalidDBInstanceState) when calling the StartDBInstance operation: Instance database-1 cannot be started as it is not in one of the following statuses: 'stopped, inaccessible-encryption-credentials-recoverable'.
                                    if instance_status == 'stopping':
                                        print('DB Instance {} is being stopped right now, please waitx'.format(cluster_identifier))
                                        #Error stopping RDS clusters: An error occurred (InvalidDBInstanceState) when calling the StartDBInstance operation: Instance database-1 cannot be started as it is not in one of the following statuses: 'stopped, inaccessible-encryption-credentials-recoverable'.              
                            except Exception as e:
                                print(f"Error stopping RDS clusters: {str(e)}")
                            # check if is running and do nothing if is running # add checkpoint here
                            # add for multiple instances then replicate for rds.
                        else:
                            print("The current time is outside the specified range1.")
                            # check if is in shutdown state and shutdown if is not in shutdown state
                            #ec2_client.stop_instances(InstanceIds=[instance_id])
                            #rds_client.stop_db_cluster(DBClusterIdentifier=[db_cluster_name])
                            try:
                                # Loop through the list and stop each RDS cluster
                          
                                for cluster_identifier in db_cluster_name:
 
                                    #response = rds.stop_db_instance(DBInstanceIdentifier=cluster_identifier)
                                    response = rds.describe_db_instances(DBInstanceIdentifier=cluster_identifier)
                            
                                    db_instance = response['DBInstances'][0]
                                    # Get the instance status
                                    instance_status = db_instance['DBInstanceStatus']
                                    print(instance_status)
                              

                                    if instance_status == 'stopped':
                                        print("The DB instance is stopped. so we do nothing")

                                    if instance_status == 'available':
                                        print('DB Instance {0} The DB instance is healthy and available. we can shutdown')
                                        response = rds.stop_db_instance(DBInstanceIdentifier=cluster_identifier)

                                        #response = rds.stop_db_instance(
                                        #    DBInstanceIdentifier=cluster_identifier
                                        #)
                                        #Error stopping RDS clusters: An error occurred (InvalidDBInstanceState) when calling the StartDBInstance operation: Instance database-1 cannot be started as it is not in one of the following statuses: 'stopped, inaccessible-encryption-credentials-recoverable'.
                                    if instance_status == 'starting':
                                      
                                        print('DB Instance {} The DB instance is starting..'.format(cluster_identifier))
                                        #Error stopping RDS clusters: An error occurred (InvalidDBInstanceState) when calling the StartDBInstance operation: Instance database-1 cannot be started as it is not in one of the following statuses: 'stopped, inaccessible-encryption-credentials-recoverable'.
                                    if instance_status == 'stopping':
                                        print('DB Instance {} is being stopped right now, please wait'.format(cluster_identifier))
                                        #Error stopping RDS clusters: An error occurred (InvalidDBInstanceState) when calling the StartDBInstance operation: Instance database-1 cannot be started as it is not in one of the following statuses: 'stopped, inaccessible-encryption-credentials-recoverable'.              
         
                                    # Error stopping RDS clusters: An error occurred (InvalidDBInstanceState) when calling the StopDBInstance operation: Instance database-1 is not in available state.
                                    #response = rds.stop_db_cluster(
                                    #    DBInstanceIdentifier=cluster_identifier
                                    #)
                                    #print(f"RDS cluster {cluster_identifier} is being stopped.")
                            except Exception as e:
                                print(f"Error stopping RDS clusters: {str(e)}")


                    else:
                        print("db is name is not defined or existent")

            else:
                print(f"'{item_name}' is disabled (False).")
        else:
            print(f"'{item_name}' does not have a valid 'enabled' value.")


              
 
            








#        print(f"'{item_name}' has 'instance_type' and 'service_type' with defined values.")
#    else:
#        print(f"'{item_name}' does not have 'instance_type' and 'service_type' aaa with defined values.")

 

    #if service_type == "ec2":
    #   print(cluster_name)
    #if service_type == "rds":
    #   print(cluster_name)
       



