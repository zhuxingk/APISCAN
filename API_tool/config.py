import configparser

config = configparser.ConfigParser()
config.add_section('Section1')
config.set('Section1', 'params', 'param1=value1\nparam2=value2')
config.set('Section1', 'headers', 'Content-Type=application/json\nAuthorization=Bearer xxxxxxx')
config.set('Section1', 'checks', 'status_code=200\ncontent_type=application/json')

with open('config.ini', 'w') as f:
    config.write(f)
