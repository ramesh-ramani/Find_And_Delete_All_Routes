import boto3
import constants
from netaddr import IPNetwork
import sys
import time
import json

routes_before_change = []

def revert_route_change(client):
    print("Going to revert Changes!")
    for i in routes_before_change:
        response = client.create_route(
            DestinationCidrBlock=i[0],
            VpcPeeringConnectionId=i[1],
            RouteTableId=i[3]
        )
    print("Details of revert: ",i)
    print(response)


def delete_routes(client,routes_to_delete_dict):
    for DestinationCidrBlock,RouteTableId in routes_to_delete_dict.items():
        response = client.delete_route(
             DestinationCidrBlock=DestinationCidrBlock,
             RouteTableId=RouteTableId[0])
        print("Route Deleted: ",response)
    print("Routes Deleted!")
    revert_routes_check = input("\nDo do you want to revert your change?(Y/N): ") 
    while True():
        if revert_routes_check[0].lower() == 'n':
           print("Exiting!")
           sys.exit()
        elif revert_routes_check[0].lower() == 'y':
           revert_route_change(client)      
    
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
        print("\n**************\n")
        print("Changes to be made to VPC: ",vpc['Values'])
        print("\n**************\n")
        routes_to_delete_dict={}
        response = client.describe_route_tables(Filters=[vpc])
        #print(response)
        for assoc in response['RouteTables']:
            for route in assoc['Routes']:
                try:
                    bool_list = [IPNetwork(route['DestinationCidrBlock']) == i for i in black_lst_ips]
                    if any(bool_list):
                        continue
                    if (src_ip == IPNetwork(route['DestinationCidrBlock']) or IPNetwork(route['DestinationCidrBlock']) in src_ip):
                        routes_before_change.append([route['DestinationCidrBlock'],route['VpcPeeringConnectionId'],vpc['Values'][0],assoc['RouteTableId']])
                        print("Route before change: ", route, ",VPC ID: ", vpc['Values'][0], ",Route Table ID: ", assoc['RouteTableId'])
                        routes_to_delete_dict[route['DestinationCidrBlock']] = [assoc['RouteTableId']]
                    #print("Route after change: ", route)
                except:
                    continue

        while True:
            if not routes_to_delete_dict:
               print("No changes to make!")
               break
            user_response = input("Are you sure you want to proceed with the change?(Y/N): ")
            if user_response[0].lower() == 'y':
               print("Hold on. Deleting routes!")
               # time is not being imported
               time.sleep(30)
               delete_routes(client,routes_to_delete_dict)
               break
            elif user_response[0].lower() == 'n':
               print("Ok. Not making changes for this VPC")
               break



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
