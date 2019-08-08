import boto3
import json

client = boto3.client('iam')
users = client.list_users()
groups = client.list_groups()
roles = client.list_roles()

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

def get_role_policies(rolename):
    list_policies = client.list_role_policies(RoleName=rolename)
    return list_policies['PolicyNames']

def get_role_policy_doc(rolename, policyname):
    policy_doc = client.get_role_policy(RoleName=rolename, PolicyName=policyname)
    return policy_doc

def get_role_managed_policies(rolename):
    list_policies = client.list_attached_role_policies(RoleName=rolename)
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
            user_dict['Name'] = username
            user_dict['Profile'] = 'user_inline'
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
            user_dict['Name'] = username
            user_dict['Profile'] = 'user_managed'
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
            group_dict['Name'] = groupname
            group_dict['Profile'] = 'group_inline'
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
            group_dict['Name'] = groupname
            group_dict['Profile'] = 'group_managed'
        if group_dict:
            group_list.append(group_dict)
    return group_list

def iam_role_inline_policy():
    role_list = []
    for role in roles['Roles']:
        role_dict = {}
        rolename = role['RoleName']
        list_managed_policies = get_role_policies(rolename)
        if list_managed_policies:
            policy_list = []
            for policy in list_managed_policies:
                policy_dict = {}
                policy_dict['PolicyName'] = policy
                policy_doc = get_role_policy_doc(rolename, policy)
                policydoc_list = []
                for key in policy_doc['PolicyDocument']['Statement']:
                    policydoc_dict = {}
                    policydoc_dict['Action'] = key['Action']
                    policydoc_dict['Resource'] = key['Resource']
                    policydoc_dict['Effect'] = key['Effect']
                    policydoc_list.append(policydoc_dict)
                policy_dict['PolicyDoc'] = policydoc_list
                policy_list.append(policy_dict)
            role_dict['Policy'] = policy_list
            role_dict['Name'] = rolename
            role_dict['Profile'] = 'role_inline'
        if role_dict:
            role_list.append(role_dict)
    return role_list

def iam_role_managed_policy():
    role_list = []
    for role in roles['Roles']:
        role_dict = {}
        rolename = role['RoleName']
        list_managed_policies = get_role_managed_policies(rolename)
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
            role_dict['Policy'] = policy_list
            role_dict['Name'] = rolename
            role_dict['Profile'] = 'role_managed'
        if role_dict:
            role_list.append(role_dict)
    return role_list

def check_action():
    pass

def check_item(item):
    if item == '*' or 's3:' in item:
        return 1
    else:
        return 0

def check_resource(resource):
    number = 0
    if isinstance(resource, list):
        for res in resource:
            number = check_item(res)
            if number == 0:
                continue
            else:
                return number
        return number
    elif isinstance(resource, unicode):
        number = check_item(resource)
        return number
    else:
        return number

def check_action(action, resource):
    number = 0
    if isinstance(action, list):
        for act in action:
            number = check_item(act)
            if number == 0:
                continue
            else:
                number = check_resource(resource)
                return number
        return number
    elif isinstance(action, unicode):
        number = check_item(action)
        if number == 0:
            return number
        else:
            number = check_resource(resource)
            return number
    else:
        return number

def check_policy(total_list):
    for total in total_list:
        number = 0
        list_number = []
        for policy in total['Policy']:
            for doc in policy['PolicyDoc']:
                if doc['Effect'] == 'Deny':
                    continue
                number = check_action(doc['Action'], doc['Resource'])
                list_number.append(number)
        summation = sum(list_number)
        #if summation != 0:
        #    print("%s: %s has permission to Amazon S3 bucket:" % (total['Profile'], total['Name']))
        #    print("%s" % (total['Policy']))

#{'Name': 'cmb-test01', 'Profile': 'User', 'Policy': [ {'PolicyName': 'cmb-ec2all', 'PolicyDoc': [{'Action': u'ec2:*', 'Resource': u'*', 'Effect': u'Allow'}] } ]}


                
if __name__ == '__main__':
    user_list = iam_attached_directly_inline_policy() + iam_attached_directly_managed_policy()
    group_list = iam_attached_from_group_inline_policy() + iam_attached_from_group_managed_policy()
    role_list = iam_role_inline_policy() + iam_role_managed_policy()
    total_list = user_list + group_list + role_list
    #for key in total_list:
    #    print json.dumps(key, sort_keys=True, indent=4, separators=(',', ':'))
    check_policy(total_list)
    

