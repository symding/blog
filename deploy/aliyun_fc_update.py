import os
import sys
import base64

from typing import List

from alibabacloud_tea_openapi.client import Client as OpenApiClient
from alibabacloud_tea_openapi import models as open_api_models
from alibabacloud_tea_util import models as util_models


import yaml

# 读取YAML文件


def read_config():
    with open("../config/aliyun_access_key.yml", 'r') as file:
        data = yaml.safe_load(file)
    return data


def zip_base64_string():
    with open("code.zip", "rb") as zip_file:
        encoded_string = base64.b64encode(zip_file.read()).decode()
    return encoded_string


class Sample:
    def __init__(self):
        pass

    @staticmethod
    def create_client():
        """
        使用AK&SK初始化账号Client
        @param access_key_id:
        @param access_key_secret:
        @return: Client
        @throws Exception
        """
        cfg = read_config()
        # 工程代码泄露可能会导致 AccessKey 泄露，并威胁账号下所有资源的安全性。以下代码示例仅供参考。
        # 建议使用更安全的 STS 方式，更多鉴权访问方式请参见：https://help.aliyun.com/document_detail/378659.html。
        config = open_api_models.Config(
            # 必填，请确保代码运行环境设置了环境变量 ALIBABA_CLOUD_ACCESS_KEY_ID。,
            access_key_id=cfg['ALIBABA_CLOUD_ACCESS_KEY_ID'],
            # 必填，请确保代码运行环境设置了环境变量 ALIBABA_CLOUD_ACCESS_KEY_SECRET。,
            access_key_secret=cfg['ALIBABA_CLOUD_ACCESS_KEY_SECRET']
        )
        # Endpoint 请参考 https://api.aliyun.com/product/FC

        # config.endpoint = f'1447920249942443.cn-hangzhou.fc.aliyuncs.com'
        config.endpoint = cfg['ALIBABA_CLOUD_ENDPOINT']
        return OpenApiClient(config)

    @staticmethod
    def create_api_info(
        function_name: str,
    ) -> open_api_models.Params:
        """
        API 相关
        @param path: params
        @return: OpenApi.Params
        """
        params = open_api_models.Params(
            # 接口名称,
            action='UpdateFunction',
            # 接口版本,
            version='2023-03-30',
            # 接口协议,
            protocol='HTTPS',
            # 接口 HTTP 方法,
            method='PUT',
            auth_type='AK',
            style='FC',
            # 接口 PATH,
            pathname=f'/2023-03-30/functions/{function_name}',
            # 接口请求体内容格式,
            req_body_type='json',
            # 接口响应体内容格式,
            body_type='json'
        )
        return params

    @staticmethod
    def main(
        args: List[str],
    ) -> None:
        client = Sample.create_client()
        params = Sample.create_api_info('nginx-blog')
        # body params
        body = {
            'code': {
                'zipFile': zip_base64_string()
            },
            'cpu': 0.05,
            'memorySize': 128
        }
        # runtime options
        runtime = util_models.RuntimeOptions()
        request = open_api_models.OpenApiRequest(
            body=body
        )
        # 复制代码运行请自行打印 API 的返回值
        # 返回值为 Map 类型，可从 Map 中获得三类数据：响应体 body、响应头 headers、HTTP 返回的状态码 statusCode。
        client.call_api(params, request, runtime)


if __name__ == '__main__':
    Sample.main(sys.argv[1:])
