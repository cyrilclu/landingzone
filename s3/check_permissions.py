import boto3
import json

def get_inline_policies(username):
    list_policies = iam.list_user_policies(UserName=username)
    return list_policies['PolicyNames']
    
def get_policy_doc(username, policyname):
    policy_doc = iam.get_user_policy(UserName=username, PolicyName=policyname)
    return policy_doc

def get_managed_policies(username):
    list_policies = iam.list_attached_user_policies(UserName=username)
    return list_policies['AttachedPolicies']

def get_group_policies(groupname):
    list_policies = iam.list_group_policies(GroupName=groupname)
    return list_policies['PolicyNames']

def get_group_policy_doc(groupname, policyname):
    policy_doc = iam.get_group_policy(GroupName=groupname, PolicyName=policyname)
    return policy_doc

def get_group_managed_policies(groupname):
    list_policies = iam.list_attached_group_policies(GroupName=groupname)
    return list_policies['AttachedPolicies']

def get_role_policies(rolename):
    list_policies = iam.list_role_policies(RoleName=rolename)
    return list_policies['PolicyNames']

def get_role_policy_doc(rolename, policyname):
    policy_doc = iam.get_role_policy(RoleName=rolename, PolicyName=policyname)
    return policy_doc

def get_role_managed_policies(rolename):
    list_policies = iam.list_attached_role_policies(RoleName=rolename)
    return list_policies['AttachedPolicies']

def get_attach_policy(policyarn):
    policy = iam.get_policy(PolicyArn=policyarn)
    policy_version = iam.get_policy_version(PolicyArn=policyarn, VersionId=policy['Policy']['DefaultVersionId'])
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

def check_item(item, bucketname):
    if item == '*' or 's3:*' in item or bucketname in item:
        return 1
    else:
        return 0

def check_resource(resource, bucketname):
    number = 0
    if isinstance(resource, list):
        for res in resource:
            number = check_item(res, bucketname)
            if number == 0:
                continue
            else:
                return number
        return number
    elif isinstance(resource, unicode):
        number = check_item(resource, bucketname)
        return number
    else:
        return number

def check_action(action, resource, bucketname):
    number = 0
    if isinstance(action, list):
        for act in action:
            number = check_item(act, bucketname)
            if number == 0:
                continue
            else:
                number = check_resource(resource, bucketname)
                return number
        return number
    elif isinstance(action, unicode):
        number = check_item(action, bucketname)
        if number == 0:
            return number
        else:
            number = check_resource(resource, bucketname)
            return number
    else:
        return number

def check_policy(total_list, bucketname):
    for total in total_list:
        number = 0
        list_number = []
        for policy in total['Policy']:
            for doc in policy['PolicyDoc']:
                if doc['Effect'] == 'Deny':
                    continue
                number = check_action(doc['Action'], doc['Resource'], bucketname)
                list_number.append(number)
        summation = sum(list_number)
        if summation != 0:
            print("%s(%s) has permission to Amazon S3 bucket: %s" % (total['Name'], total['Profile'], bucketname))

def get_s3_bucket_policy(bucketname):
    policy_dict = {}
    try:
        bucket_policy = s3cli.get_bucket_policy(Bucket=bucketname)
    except Exception as e:
        return policy_dict
    else:
        policy = eval(bucket_policy['Policy'])
        statement = policy['Statement']
        policy_dict['Name'] = bucketname
        policy_dict['Profile'] = "s3_bucket"
        policydoc_list = []
        for key in statement:
            policydoc_dict = {}
            policydoc_dict['Action'] = key['Action']
            policydoc_dict['Effect'] = key['Effect']
            policydoc_dict['Principal'] = key['Principal']
            policydoc_dict['Resource'] = key['Resource']
            policydoc_list.append(policydoc_dict)
        policy_dict['Policy'] = policydoc_list
        return policy_dict

def s3_bucket_policy(mybucketname):
    bucket_list = []
    for bucket in buckets['Buckets']:
        bucketname = bucket['Name']
        if mybucketname == bucketname:
            bucket_dict = get_s3_bucket_policy(bucketname)
            if bucket_dict:
                bucket_list.append(bucket_dict)
    return bucket_list

def analyze_user_role(principal_aws):
    if ':user/' in principal_aws:
        return principal_aws.rsplit('/', 1)[-1], "user_s3"
    elif ':role/' in principal_aws:
        return principal_aws.rsplit('/', 1)[-1], "role_s3"
    else:
        print("Principal: %s" % principal_aws)
        return None, None

def analyze_principal_aws(principal_aws):
    principal_list = []
    if isinstance(principal_aws, list):
        for pa in principal_aws:
            principal_dict = {}
            principal_name, principal_profile = analyze_user_role(pa)
            if principal_name:
                principal_dict['principal_name'] = principal_name
                principal_dict['principal_profile'] = principal_profile
                principal_list.append(principal_dict)
    elif isinstance(principal_aws, str):
        principal_dict = {}
        principal_name, principal_profile = analyze_user_role(principal_aws)
        if principal_name:
            principal_dict['principal_name'] = principal_name
            principal_dict['principal_profile'] = principal_profile
            principal_list.append(principal_dict)
    return principal_list

def analyze_principal(principal):
    if isinstance(principal, dict):
        principal_aws = principal['AWS']
        user_role_list = analyze_principal_aws(principal_aws)
        return user_role_list
    else:
        return None

def check_s3_policy(s3_bucket_list):
    s3_permission_allow_list = []
    for bucket in s3_bucket_list:
        for policy in bucket['Policy']:
            s3_permission_dict = {}
            if policy['Effect'] == 'Allow':
                principal = policy['Principal']
                if analyze_principal(principal):
                    s3_permission_dict['IAMProfile'] = analyze_principal(principal)
                    s3_permission_dict['BucketName'] = bucket['Name']
                else:
                    print("Is %s a public S3 Bucket?" % s3_permission_dict['BucketName'])
                s3_permission_allow_list.append(s3_permission_dict)
    for key in s3_permission_allow_list:
        for profile in key['IAMProfile']:
            print("%s: %s has permission to Amazon S3 bucket: %s" % (profile['principal_profile'], profile['principal_name'], key['BucketName']))

#{'Name': 'cmb-test01', 'Profile': 'User', 'Policy': [ {'PolicyName': 'cmb-ec2all', 'PolicyDoc': [{'Action': u'ec2:*', 'Resource': u'*', 'Effect': u'Allow'}] } ]}
#{'Name': 'cmb-bucket01', 'Profile': 'S3 Bucket', 'Policy': [{'Action': 'S3:*', 'Resource': '*', 'Effect': 'Allow', 'Principal': '*'}] }
                
if __name__ == '__main__':
    iam = boto3.client('iam')
    users = iam.list_users()
    groups = iam.list_groups()
    roles = iam.list_roles()
    s3cli = boto3.client('s3')
    buckets = s3cli.list_buckets()
    bucketname = ''
    while not bucketname or bucketname.isspace():
        bucketname = raw_input("Enter your S3 bucket name: ")
    print("==============================================")
    s3res = boto3.resource('s3')
    if s3res.Bucket(bucketname) not in s3res.buckets.all():
        print("Your S3 bucket %s is not exist." % bucketname)
    else:
        user_list = iam_attached_directly_inline_policy() + iam_attached_directly_managed_policy()
        group_list = iam_attached_from_group_inline_policy() + iam_attached_from_group_managed_policy()
        role_list = iam_role_inline_policy() + iam_role_managed_policy()
        iam_list = user_list + group_list + role_list
        check_policy(iam_list, bucketname)
        s3_bucket_list = s3_bucket_policy(bucketname)
        check_s3_policy(s3_bucket_list)
