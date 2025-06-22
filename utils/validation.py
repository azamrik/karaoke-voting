import re


def domain_validation(required_domain:str):
    if not required_domain or (required_domain==''):
        return False
    elif re.fullmatch('@\\w+\\.\\w{1,3}', required_domain):
        return True
    else:
        raise ValueError(f'Domain name "{required_domain}" is not valid. Value must match regex @\w+\.\w{1,3}'.format(required_domain))
