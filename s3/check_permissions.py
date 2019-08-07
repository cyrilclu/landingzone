import boto3
import json

client = boto3.client('iam')
users = client.list_users()
groups = client.list_groups()

def get_inline_policies(username):
    list_policies = client.list_user_policies(UserName=username)
    return list_policies['PolicyNames']
    
def get_outline_policies(username):
    list_policies = client.list_attached_user_policies(UserName=username)
    return list_policies['AttachedPolicies']

def get_policy_doc(username, policyname):
    policy_doc = client.get_user_policy(UserName=username, PolicyName=policyname)
    return policy_doc

user_list = []
for user in users['Users']:
    user_dict = {}
    username = user['UserName']
    list_inline_policies = get_inline_policies(username)
    if list_inline_policies:
        policy_list = []
        for policy in list_inline_policies:
            policy_dict = {}
            policy_dict['PolicyName'] = policy
            policy_doc = get_policy_doc(username, policy)
            policydoc_list = []
            for key in policy_doc['PolicyDocument']['Statement']:
                policydoc_dict = {}
                policydoc_dict['Action'] = key['Action']
                policydoc_dict['Resource'] = key['Resource']
                policydoc_dict['Effect'] = key['Effect']
                policydoc_list.append(policydoc_dict)
            policy_dict['PolicyDoc'] = policydoc_list
            policy_list.append(policy_dict)
        user_dict['Policy'] = policy_list
        user_dict['UserName'] = username
        if user_dict:
            user_list.append(user_dict)
for key in user_list:
    print json.dumps(key, sort_keys=True, indent=4, separators=(',', ':'))
    #list_outline_policies = get_outline_policies(username)
    #for policy in list_outline_policies:
    #    print(policy['PolicyName'])
    #    print(policy['PolicyArn'])
#{'UserName': 'cmb-test01', 'Policy': [ {'PolicyName': 'cmb-ec2all', 'PolicyDoc': [{'Action': u'ec2:*', 'Resource': u'*', 'Effect': u'Allow'}] } ]}
