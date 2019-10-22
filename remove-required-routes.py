import boto3
import constants
from netaddr import IPNetwork

def route_change(client):
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
    input_cidr = ("Enter the CIDR block you would be search/replacing: ")
    src_ip = IPNetwork(input_cidr)
    client = boto3.Session(
        profile_name='Riq',
        region_name='us-west-2').client('ec2')
    route_change(client)

if __name__ == '__main__':
    main()
