from config.milvus_config import milvus_config
from process.query_processor.base import NodeBase
from process.query_processor.state import QueryGraphState
from tools.logger import logger
from utils.embedding_utils import generate_embeddings
from utils.json_format_utils import serialize_json


class NodeSearchEmbedding(NodeBase):
    """
   节点功能：基于已确认主体名+改写后的用户问题，执行Milvus向量数据库混合检索
   """

    # 覆盖基类的 name 属性，标识节点名称
    name: str = "node_search_embedding"

    def process(self, state: QueryGraphState) -> QueryGraphState:
        """
        节点逻辑
        :param state: 工作流状态对象
        :return: 更新后的状态对象
        """

        try:
            # 1、用户问题和已确认商品名
            query = state.get("rewritten_query")
            item_names = state.get("item_names")

            # 2、生成向量 (Dense + Sparse)
            embeddings = generate_embeddings([query])
            dense_vec = embeddings.get("dense")[0]
            sparse_vec = embeddings.get("sparse")[0]

            # 3. 获取Milvus的集合
            collection_name = milvus_config.chunks_collection

        except Exception as e:
            logger.exception(f"向量搜索失败: {e}")
            return {}

if __name__ == "__main__":

    init_state = {
        "rewritten_query": "关于brother HAK180烫金机，如何调节转印温度？",
        "item_names": ["BrotherHAK180烫金机", "BrotherHAK-180烫金机"]
    }
    node_search_embedding = NodeSearchEmbedding()
    result = node_search_embedding(init_state)
    logger.info(serialize_json(result, indent=4))