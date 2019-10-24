import boto3
import constants
from netaddr import IPNetwork
import sys


def route_change(client, src_ip):
    """
    Extract the routes and eni information from the AWS API
    """
    for vpc in constants.VPC_FILTER:
        response = client.describe_route_tables(Filters=vpc)
        print(response)
        for assoc in response['RouteTables']:
            for route in assoc['Routes']:
                try:
                    if (src_ip in IPNetwork(route['DestinationCidrBlock'])):
                        print("Route before change: ", route)
                        print("Route before change: ", route)
                        response = client.delete_route(
                            DestinationCidrBlock=route['DestinationCidrBlock'],
                            RouteTableId=assoc['RouteTableId'])
                    print("Route after change: ", route)
                except BaseException:
                    print("Error extracting route information. Continuing")
                    continue


def main():

    input_cidr = input(
        "Enter the CIDR block you would need to be removed from the relevant VPCs Route Tables: ")

    try:
        src_ip = IPNetwork(input_cidr)
    except BaseException:
        print("Incorrect CIDR Block. Exiting!")
        sys.exit()

    client = boto3.Session(
        profile_name='Riq',
        region_name='us-west-2').client('ec2')
    route_change(client, src_ip)


if __name__ == '__main__':
    main()
