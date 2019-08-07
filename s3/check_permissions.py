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

def get_attach_policy(policyarn):
    policy = client.get_policy(PolicyArn=policyarn)
    policy_version = client.get_policy_version(PolicyArn=policyarn, VersionId=policy['Policy']['DefaultVersionId'])
    return policy_version

def iam_direct_attach_inline_policy():
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

def iam_direct_attach_managed_policy():
    user_list = []
    for user in users['Users']:
        user_dict = {}
        username = user['UserName']
        list_outline_policies = get_outline_policies(username)
        if list_outline_policies:
            policy_list = []
            for policy in list_outline_policies:
                policy_dict = {}
                policy_dict['PolicyName'] = policy['PolicyName']
                policy_doc = get_attach_policy(policy['PolicyArn'])
                policydoc_list = []
                for key in policy_doc['PolicyVersion']['Document']['Statement']:
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
                
if __name__ == '__main__':
    iam_direct_attach_inline_policy()
    iam_direct_attach_managed_policy()

#{'UserName': 'cmb-test01', 'Policy': [ {'PolicyName': 'cmb-ec2all', 'PolicyDoc': [{'Action': u'ec2:*', 'Resource': u'*', 'Effect': u'Allow'}] } ]}
