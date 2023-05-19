import json
import re
import pymongo
from pymongo import MongoClient, UpdateOne
# from pymongo import InsertOne, UpdateMany
import configparser


class APIStorage:
    def __init__(self, db_url, db_name, collection_name):
        self.client = MongoClient(db_url)
        self.db = self.client[db_name]
        self.collection = self.db[collection_name]

    # 批量插入接口信息,新增判断，如果接口信息中包含该接口，则不插入；
    def bulk_insert_interfaces(self, interface_data_list):
        if len(interface_data_list) > 0:
            try:
                bulk_operations = []
                for data in interface_data_list:
                    filter = {'name': data['name']}
                    update_doc = {'$set': data}
                    operation = UpdateOne(filter, update_doc, upsert=True)
                    bulk_operations.append(operation)

                result = self.collection.bulk_write(bulk_operations)
                print('Number of inserted documents:', len(result.upserted_ids) + len(result.modified_ids))
            except Exception as e:
                print('Error occurred while bulk inserting interface information:', e)

    # 批量更新接口信息，新增判断条件，若接口参数信息有变化，则更新，否则不更新；
    def bulk_update_interfaces(self, update_data_list):
        try:
            bulk_operations = []
            for data in update_data_list:
                filter = {'name': data['name']}
                existing_doc = self.collection.find_one(filter)

                if existing_doc and existing_doc != data:
                    # 检查接口信息是否有变化,has_changes为True表示有变化,否则无变化;
                    has_changes = False
                    for key in data:
                        # 根据接口参数信息判断接口中的参数是否和数据库中的参数一致，若不一致，则更新；
                        if key != '_id' and key in existing_doc and existing_doc[key] != data[key]:
                            has_changes = True
                            break
                    # 如果存在变化，则更新，upsert=True表示如果不存在则插入
                    if has_changes:
                        update_doc = {'$set': data}
                        operation = UpdateOne(filter, update_doc, upsert=True)
                        bulk_operations.append(operation)

            if bulk_operations:
                self.collection.bulk_write(bulk_operations)
                print('接口信息已批量更新')
            else:
                print('无需进行接口更新')
        except Exception as error:
            print('批量更新接口信息时出错:', error)

    # 优化创建索引的方法，若索引不存在，则创建索引；
    def create_indexes(self):
        # 创建索引
        try:
            # 创建索引，索引名为name，升序排列
            indexes = [
                ('name', pymongo.ASCENDING),
                ('URL', pymongo.ASCENDING),
                ('Method', pymongo.ASCENDING),
                ('response.true', pymongo.ASCENDING),
                ('response.false', pymongo.ASCENDING),
                ('Extensions', pymongo.ASCENDING)
            ]
            # 获取已存在的索引
            existing_indexes = self.collection.index_information()

            # 如果索引不存在，则创建索引
            for index in indexes:
                index_name = index[0]
                if index_name not in existing_indexes:
                    self.collection.create_index([(index[0], index[1])])

            print('索引已创建')
        except Exception as error:
            print('创建索引时出错:', error)

    @staticmethod
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
                # 读取接口信息，初始化为字典
                interface_data = {}

                for field in field_mapping:
                    interface_data[field] = config.get(section, field_mapping[field])

                # Convert JSON strings to Python dictionaries
                for key in ['Request', 'Response(TRUE)', 'Response(FALSE)', 'Extensions']:
                    # 如果接口信息中包含该字段，则将其转换为字典
                    if key in interface_data:
                        interface_data[key] = json.loads(interface_data[key])

                interface_data_list.append(interface_data)

        return interface_data_list

# 使用示例
# if __name__ == '__main__':
#     # 读取接口信息
#     interface_data_list = APIStorage.read_interface_data_from_config('example_interface_config.ini')
#
#     # 创建数据库连接
#     storage = APIStorage('localhost', 'APIInfo', 'APICollection')
#
#     # 批量插入接口信息
#     storage.bulk_insert_interfaces(interface_data_list)

#     # 批量更新接口信息
#     storage.bulk_update_interfaces(interface_data_list)
#
#     # 创建索引
#     storage.create_indexes()


