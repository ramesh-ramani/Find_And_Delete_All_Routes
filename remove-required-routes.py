import boto3
import constants
from netaddr import IPNetwork
import sys
import time


def delete_routes(client,routes_to_delete_dict):
    for DestinationCidrBlock,RouteTableId in routes_to_delete_dict.items():
        response = client.delete_route(
             DestinationCidrBlock=DestinationCidrBlock,
             RouteTableId=RouteTableId)
        print("Route Deleted: ",response)
    print("Routes Deleted! Exiting!")


def route_change(client, src_ip):
    black_lst_ips = [
        IPNetwork("0.0.0.0/0"),
        IPNetwork("10.0.0.0/8")
    ]
    routes_to_delete_dict = {}
 
    """
    Extract the routes and eni information from the AWS API
    """
    
           
    for vpc in constants.VPC_FILTER:
        routes_to_delete_dict={}
        response = client.describe_route_tables(Filters=[vpc])
        #print(response)
        for assoc in response['RouteTables']:
            for route in assoc['Routes']:
                try:
                    bool_list = [IPNetwork(route['DestinationCidrBlock']) == i for i in black_lst_ips]
                    if any(bool_list):
                        continue
                    if (src_ip in IPNetwork(route['DestinationCidrBlock'])):
                        print("Route before change: ", route, ",VPC ID: ", vpc['Values'][0], ",Route Table ID: ", assoc['RouteTableId'])
                        routes_to_delete_dict[route['DestinationCidrBlock']] = [assoc['RouteTableId']]
                    #print("Route after change: ", route)
                except:
                    continue

        while True:
            user_response = input("Are you sure you want to proceed with the change?(Y/N): ")
            if user_response[0].lower() == 'y':
               print("Hold on. Deleting routes!")
               time.wait(30)
               break
            elif user_response[0].lower() == 'n':
               print("Ok. Not making changes for this VPC")
               break
        delete_routes(client,routes_to_delete_dict)



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
