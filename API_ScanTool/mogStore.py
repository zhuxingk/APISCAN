import json
import re
from pymongo import MongoClient
from pymongo import InsertOne, UpdateMany
import configparser

# 连接MongoDB数据库
client = MongoClient('mongodb://localhost:27017')

# 选择数据库
db = client['APIInfo']

# 选择集合
collection = db['APICollection']


# 批量插入接口信息
def bulk_insert_interfaces(interface_data_list):
    if len(interface_data_list) > 0:
        try:
            result = collection.insert_many(interface_data_list)
            print('Number of inserted documents:', len(result.inserted_ids))
        except Exception as e:
            print('Error occurred while bulk inserting interface information:', e)



# 批量更新接口信息
def bulk_update_interfaces(update_data_list):
    try:
        bulk_operations = [UpdateMany({'name': data['name']}, {'$set': data}, upsert=True) for data in update_data_list]
        collection.bulk_write(bulk_operations)
        print('接口信息已批量更新')
    except Exception as e:
        print('批量更新接口信息时出错:', e)


# 创建索引
def create_indexes():
    try:
        collection.create_index('name')
        collection.create_index('URL')
        collection.create_index('Method')
        collection.create_index('response(true)')
        collection.create_index('response(false)')
        collection.create_index('Extensions')
        print('索引已创建')
    except Exception as e:
        print('创建索引时出错:', e)

# 从配置文件中读取接口信息

def read_interface_data_from_config(config_file):
    config = configparser.ConfigParser()
    config.read(config_file)

    field_mapping = {
        'name': 'name',
        'URL': 'URL',
        'Method': 'Method',
        'Request': 'Request',
        'Response(TRUE)': 'Response(TRUE)',
        'Response(FALSE)': 'Response(FALSE)',
        'Extensions': 'Extensions'
    }

    interface_data_list = []

    for section in config.sections():
        if re.match('API', section):
            interface_data = {}

            for field in field_mapping:
                interface_data[field] = config.get(section, field_mapping[field])

            # Convert JSON strings to Python dictionaries
            for key in ['Request', 'Response(TRUE)', 'Response(FALSE)', 'Extensions']:
                if key in interface_data:
                    interface_data[key] = json.loads(interface_data[key])

            interface_data_list.append(interface_data)

    return interface_data_list

# def read_interface_data_from_config(config_file):
#     config = configparser.ConfigParser()
#     config.read(config_file)
#
#     field_mapping = {
#         'name': 'name',
#         'URL': 'URL',
#         'Method': 'Method',
#         'Request': 'Request',
#         'Response(TRUE)': 'Response(TRUE)',
#         'Response(FALSE)': 'Response(FALSE)',
#         'Extensions': 'Extensions'
#     }
#
#     interface_data_list = []
#
#     for section in config.sections():
#         if re.match('API', section):
#             interface_data = {}
#
#             for field in field_mapping:
#                 interface_data[field] = config.get(section, field_mapping[field])
#
#             # Convert JSON strings to Python dictionaries
#             for key in ['Request', 'Response(TRUE)', 'Response(FALSE)', 'Extensions']:
#                 if key in interface_data:
#                     interface_data[key] = json.loads(interface_data[key])
#             for field, value in interface_data.items():
#                 interface_data_list.append({field: value})
#             interface_data_list.append(interface_data)
#             # 将不同的section提取到的数据分别存入不同的列表中
#
#     return interface_data_list


# 读取示例配置文件中的接口信息
example_interface_data_list = read_interface_data_from_config('example_interface_config.ini')
print(example_interface_data_list)  # 查看读取的接口信息列表
# 批量插入接口信息
bulk_insert_interfaces(example_interface_data_list)

# 创建索引
create_indexes()

# 读取更新配置文件中的接口信息
updated_interface_data_list = read_interface_data_from_config('updated_interface_config.ini')

# 批量更新接口信息
bulk_update_interfaces(updated_interface_data_list)
