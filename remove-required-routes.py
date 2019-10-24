import boto3
import constants
from netaddr import IPNetwork

def route_change(client,src_ip):
    """
    Extract the routes and eni information from the AWS API
    """
    for vpc in constants.VPC_FILTER:
    	response = client.describe_route_tables(
        	Filters=constants.VPC_FILTER)

        for assoc in response['RouteTables']:
            for route in assoc['Routes']:
                try:
                    print("Route before change: ",route)
                    if (src_ip in IPNetwork(route['DestinationCidrBlock'])):
                       response = client.delete_route(
                       DestinationCidrBlock=route['DestinationCidrBlock'],
                       RouteTableId=assoc['RouteTableId'])
                    print("Route after change: ",route)
                except: continue
 


def main():
    input_cidr = input("Enter the CIDR block you would need to be removed from the relevant VPCs Route Tables: ")
    while True():
       try:
          src_ip = IPNetwork(input_cidr)
          break
       except:
          continue
    client = boto3.Session(
        profile_name='Riq',
        region_name='us-west-2').client('ec2')
    route_change(client,src_ip)

if __name__ == '__main__':
    main()
