import os

import yaml

# 注意，开发环境基本都是dev ，必须在/app/projects/ycgYangguan/env 这个目录下才能读取到配置的env，否则认为是dev


# current_directory = os.getcwd()
# print("-----------------------------current_dir:{}".format(current_directory))
# 暂时写死 todo 不知道如何改造，不能用相对路径，否则scrapyd会报错。最好用环境变量来配置
envFileDir = "/app/projects/ycgYangguan/"

def get_env():
    env_file = envFileDir + "env"
    if os.path.exists(env_file) == False:
        return "dev"
    else:
        with open(env_file, "r", encoding="utf-8") as f:
            env = f.read().strip()
            if env in ['dev','test','beta','prod']:
                return env
            else:
                return 'dev'
env = get_env()

# print("env===============" + env)

if env == "dev":
    # 注意，只有本地开发环境才能读取相对目录，测试、生产环境由于部署环境问题，不能用相对路径
    current_directory = os.path.dirname(os.path.abspath(__file__))
    configFile = current_directory + "/../config/" + env + ".yaml"
else:
    # 服务器环境，目前只能写死绝对路径获取配置文件
    configFile = "/app/projects/ycgYangguan/ycgYangguan/config/" + env + ".yaml"

#configFile = "ycgYangguan/config/dev.yaml"
# configFile = "C:\python_project\gfyx\gfyx-crawl-spider\projects\ycgYangguan\ycgYangguan/config/dev.yaml"


with open(configFile) as file:
    spiderConfig = yaml.load(file, Loader=yaml.FullLoader)