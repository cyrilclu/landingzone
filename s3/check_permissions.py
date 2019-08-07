import boto3
import json

client = boto3.client('iam')
users = client.list_users()
groups = client.list_groups()

def get_inline_policies(username):
    list_policies = client.list_user_policies(UserName=username)
    return list_policies['PolicyNames']
    
def get_policy_doc(username, policyname):
    policy_doc = client.get_user_policy(UserName=username, PolicyName=policyname)
    return policy_doc

def get_managed_policies(username):
    list_policies = client.list_attached_user_policies(UserName=username)
    return list_policies['AttachedPolicies']

def get_group_policies(groupname):
    list_policies = client.list_group_policies(GroupName=groupname)
    return list_policies['PolicyNames']

def get_group_policy_doc(groupname, policyname):
    policy_doc = client.get_group_policy(GroupName=groupname, PolicyName=policyname)
    return policy_doc

def get_group_managed_policies(groupname):
    list_policies = client.list_attached_group_policies(GroupName=groupname)
    return list_policies['AttachedPolicies']

def get_attach_policy(policyarn):
    policy = client.get_policy(PolicyArn=policyarn)
    policy_version = client.get_policy_version(PolicyArn=policyarn, VersionId=policy['Policy']['DefaultVersionId'])
    return policy_version


def iam_attached_directly_inline_policy():
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
    return user_list

def iam_attached_directly_managed_policy():
    user_list = []
    for user in users['Users']:
        user_dict = {}
        username = user['UserName']
        list_managed_policies = get_managed_policies(username)
        if list_managed_policies:
            policy_list = []
            for policy in list_managed_policies:
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
    return user_list

def iam_attached_from_group_inline_policy():
    group_list = []
    for group in groups['Groups']:
        group_dict = {}
        groupname = group['GroupName']
        list_managed_policies = get_group_policies(groupname)
        if list_managed_policies:
            policy_list = []
            for policy in list_managed_policies:
                policy_dict = {}
                policy_dict['PolicyName'] = policy
                policy_doc = get_group_policy_doc(groupname, policy)
                policydoc_list = []
                for key in policy_doc['PolicyDocument']['Statement']:
                    policydoc_dict = {}
                    policydoc_dict['Action'] = key['Action']
                    policydoc_dict['Resource'] = key['Resource']
                    policydoc_dict['Effect'] = key['Effect']
                    policydoc_list.append(policydoc_dict)
                policy_dict['PolicyDoc'] = policydoc_list
                policy_list.append(policy_dict)
            group_dict['Policy'] = policy_list
            group_dict['GroupName'] = groupname
        if group_dict:
            group_list.append(group_dict)
    return group_list

def iam_attached_from_group_managed_policy():
    group_list = []
    for group in groups['Groups']:
        group_dict = {}
        groupname = group['GroupName']
        list_managed_policies = get_group_managed_policies(groupname)
        if list_managed_policies:
            policy_list = []
            for policy in list_managed_policies:
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
            group_dict['Policy'] = policy_list
            group_dict['GroupName'] = groupname
        if group_dict:
            group_list.append(group_dict)
    return group_list

                
if __name__ == '__main__':
    #user_list = iam_attached_directly_inline_policy() + iam_attached_directly_managed_policy()
    #for key in user_list:
    #    print json.dumps(key, sort_keys=True, indent=4, separators=(',', ':'))
    #group_list = iam_attached_from_group_inline_policy() + iam_attached_from_group_managed_policy()
    #for key in group_list:
    #    print json.dumps(key, sort_keys=True, indent=4, separators=(',', ':'))
    

#{'UserName': 'cmb-test01', 'Policy': [ {'PolicyName': 'cmb-ec2all', 'PolicyDoc': [{'Action': u'ec2:*', 'Resource': u'*', 'Effect': u'Allow'}] } ]}
