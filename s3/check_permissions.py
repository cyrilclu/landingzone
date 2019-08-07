import boto3
import json

client = boto3.client('iam')
users = client.list_users()
groups = client.list_groups()
user_list = []

def get_inline_policies(username):
    list_policies = client.list_user_policies(UserName=username)
    return list_policies['PolicyNames']
    
def get_outline_policies(username):
    list_policies = client.list_attached_user_policies(UserName=username)
    return list_policies['AttachedPolicies']

def get_policy_doc(username, policyname):
    policy_doc = client.get_user_policy(UserName=username, PolicyName=policyname)
    return policy_doc

for user in users['Users']:
    user_dict = {}
    username = user['UserName']
    list_inline_policies = get_inline_policies(username)
    if list_inline_policies:
        for policy in list_inline_policies:
            user_dict['PolicyName'] = policy
            policy_doc = get_policy_doc(username, policy)
            #print(json.dumps(policy_doc['PolicyDocument']['Statement'], sort_keys=True, indent=4, separators=(',', ':')))
            policydoc_list = []
            for key in policy_doc['PolicyDocument']['Statement']:
                policydoc_dict = {}
                policydoc_dict['Action'] = key['Action']
                policydoc_dict['Resource'] = key['Resource']
                policydoc_dict['Effect'] = key['Effect']
                policydoc_list.append(policydoc_dict)
            user_dict['PolicyDoc'] = policydoc_list
        user_dict['UserName'] = username
    if user_dict:
        user_list.append(user_dict)
for key in user_list:
    print key
    #list_outline_policies = get_outline_policies(username)
    #for policy in list_outline_policies:
    #    print(policy['PolicyName'])
    #    print(policy['PolicyArn'])

   
