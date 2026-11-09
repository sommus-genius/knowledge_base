import json
import logging
from pathlib import Path

from process.import_process.base import BaseNode, setup_logging
from process.import_process.exceptions import StateFieldError, ValidationError, FileProcessingError
from process.import_process.state import ImportGraphState


class NodeEntry(BaseNode):
    """
       入口节点：任务分发
    """

    name = "node_entry"

    def process(self, state: ImportGraphState):

        # 1.state中获取文件的绝对路径
        import_file_path = state.get("import_file_path")
        # 判断是否为空
        if not import_file_path:
            raise StateFieldError(
                field_name="import_file_path",
                message="文件路径不能为空",
                expected_type= str,
            )
        # 2.转换path对象
        import_file_path_obj = Path(import_file_path)

        if not import_file_path_obj.exists():
            raise FileProcessingError(
                message=f"文件{import_file_path_obj.name}不存在"
            )
        # 3.判断文件的扩展名是pdf还是md
        if import_file_path_obj.suffix == ".pdf":
            state["is_pdf_read_enabled"] = True
            state["is_md_read_enabled"] = False
            state["pdf_path"] = import_file_path
        elif import_file_path_obj.suffix == ".md":
            state["is_md_read_enabled"] = True
            state["is_pdf_read_enabled"] = False
            state["md_path"] = import_file_path
        else:
            raise ValidationError(
                message=f"不支持的文件类型{import_file_path_obj.suffix}",
            )

        # 4.获取文件名作为标题
        state["file_title"] = import_file_path_obj.stem

        return state


if __name__ == "__main__":
    setup_logging()

    init_state = {"import_file_path": r"D:\doc\安全手册.pdf"}
    node_entry = NodeEntry()
    result = node_entry(init_state)

    logging.getLogger().info(json.dumps(result, ensure_ascii=False, indent=4))
