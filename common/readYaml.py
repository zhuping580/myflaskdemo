import yaml
from configs.common import project_path


class ReadYaml:
    def __init__(self, _filename):
        self.filepath = project_path+"\\yaml\\"+_filename

    def get_yaml_data(self):
        try:
            with open(self.filepath, "r", encoding="utf-8") as f:
                return yaml.load(f, Loader=yaml.FullLoader)
        except IOError:
            print("Error: 没有找到文件或读取文件失败")

    def writer_yaml(self, dict_data):
        with open(self.filepath, 'w', encoding='utf-8') as yaml_file:
            yaml.dump(dict_data, yaml_file, allow_unicode=True)


if __name__ == '__main__':
    # data = ReadYaml("login_data.yml").get_yaml_data()
    # a = data['test_login_data']
    # ids = [x[0] for x in a]
    # print(ids)
    data = ReadYaml("data_model.yml").get_yaml_data()
    print(data)
