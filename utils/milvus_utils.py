import json

from pymilvus import MilvusClient

from config.milvus_config import milvus_config


_milvus_client = None


def escape_milvus_string(value: str) -> str:
    """转义用于 Milvus filter 双引号字符串中的值（不包含外层引号）。"""
    if value is None:
        return ""
    return json.dumps(str(value), ensure_ascii=False)[1:-1]


def get_milvus_client():
    """首次使用时连接 Milvus，后续复用客户端。"""
    global _milvus_client
    if _milvus_client is None:
        if not milvus_config.milvus_url:
            raise ValueError("未配置 MILVUS_URL")
        _milvus_client = MilvusClient(uri=milvus_config.milvus_url, timeout=10)
    return _milvus_client
