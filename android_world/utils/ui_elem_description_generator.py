import json
import time

from android_world.env import representation_utils
from android_world.agents import m3a_utils
from android_world.agents import infer

LOG_FILE_PATH = r'E:\Desktop\android_world\tmp\ui_log.txt'  # 可以改成你想要的路径


# 初始化：每次运行先清空文件（只运行一次即可）
def init_log_file():
    with open(LOG_FILE_PATH, 'w', encoding='utf-8') as f:
        f.write('')  # 清空内容


# 包装函数：像 print 一样使用
def log_to_file(*args, sep=' ', end='\n'):
    message = sep.join(str(arg) for arg in args) + end
    with open(LOG_FILE_PATH, 'a', encoding='utf-8') as f:
        f.write(message)


init_log_file()


class UI_Elem_Description_Generator:
    """
    A class to generate descriptions for UI elements based on their properties.
    """

    def __init__(self, model_name):
        self.strategy_map = {0: self.generate_ui_elements_description_list_full,
                             1: self.generate_ui_elements_description_list_enhanced_filter,
                             2: self.generate_ui_elements_description_list_llm}
        self.model_name = model_name

    def convert_ui_elements_to_pure_json(
            self,
            ui_elements: list[tuple[int, representation_utils.UIElement]],
    ) -> list[dict]:
        simplified_elements = []

        for idx, elem in ui_elements:
            label = elem.text or elem.content_description or "<no label>"
            hint = elem.hint_text or ""
            combined = f"{label} {hint}".lower()
            class_type = elem.class_name.split('.')[-1] if elem.class_name else "unknown"

            # 猜测可能的字段类型
            likely_field = next(
                (f for f in
                 ['name', 'phone', 'email', 'search', 'contact', 'amount', 'note', 'date', 'time']
                 if f in combined),
                ""
            )

            # 坐标提取（可选）
            bbox = {
                "x_min": elem.bbox_pixels.x_min,
                "x_max": elem.bbox_pixels.x_max,
                "y_min": elem.bbox_pixels.y_min,
                "y_max": elem.bbox_pixels.y_max,
            } if elem.bbox_pixels else None

            element_repr = {
                "index": idx,
                "type": class_type,
                "label": label,
                "content_description": elem.content_description or "",
                "hint": hint,
                "clickable": elem.is_clickable,
                "long_clickable": elem.is_long_clickable,
                "editable": elem.is_editable,
                "checked": elem.is_checked,
                "scrollable": elem.is_scrollable,
                "visible": elem.is_visible,
                "enabled": elem.is_enabled,
                "resource_name": elem.resource_name,
                "position": bbox,
            }
            if likely_field:
                element_repr["likely_field"] = likely_field

            simplified_elements.append(element_repr)

        return simplified_elements

    def generate_general_ui_prompt(self, ui_elements: list[dict], goal: str) -> str:
        """
        构建用于 LLM 分析 UI 屏幕结构的 prompt。

        参数:
            ui_elements: list[dict] - 简化后的 UI 元素列表。

        返回:
            str - 可直接发送给 LLM 的 prompt。
        """
        # prompt_header = """Given the following UI elements in JSON format, summarize in 1–2 sentences what this mobile screen likely shows and how it's structured.
        #
        # JSON:"""

        prompt_header = f"""
        The goal of the current UI task is {goal}.
        You are an expert in analyzing mobile UI structures.
        The following is a list of UI elements on the screen, represented in JSON format.
        Your task is to summarize the visible structure of the screen based on this JSON.
        Focus only on top-level layout, scrollable components, and repeated elements.
        Identify key elements, then focus on analysing their attributes. At the end, describe their possible usage that could be related to the task goal.
        Do not describe every element in detail.

        JSON:"""

        json_content = json.dumps(ui_elements, indent=2, ensure_ascii=False)
        return f"{prompt_header}\n```\n{json_content}\n```"

    def filter_out_invalid_ui_elements(
            self, ui_elements: list[representation_utils.UIElement],
            screen_width_height_px: tuple[int, int],
    ) -> list[representation_utils.UIElement]:
        """
        Filters out invalid UI elements based on their properties.
        """
        return [
            ui_element for ui_element in ui_elements
            if m3a_utils.validate_ui_element(ui_element, screen_width_height_px)
        ]

    def filter_out_useless_ui_elements(self, ui_elements: list[representation_utils.UIElement]) -> \
            list[tuple[int, representation_utils.UIElement]]:
        def is_meaningful(e):
            # 明确排除一些明显无意义的 class
            ignored_classes = {
                'android.widget.ImageView',
                'android.widget.FrameLayout',
                'android.widget.LinearLayout',
                'android.widget.ScrollView',
            }

            # 如果 class 本身是容器/装饰/图标，且不可编辑，就跳过
            if e.class_name in ignored_classes and not (e.is_clickable or e.is_editable):
                return False

            # 去掉通知栏（content_description 有 'notification'）
            if e.content_description and 'notification' in e.content_description.lower():
                return False

            # 保留具备交互性或有语义文本的元素
            return e.is_visible and (
                    e.is_clickable
                    or e.is_editable
                    or e.is_scrollable
                    or e.is_checkable
                    or (e.text and e.text.strip())
                    or (e.content_description and e.content_description.strip())
            )

        for index, e in enumerate(ui_elements):
            if not is_meaningful(e):
                log_to_file(f"Filtered out: index{index} {e}")

        filtered_ui_elements_with_index = [
            (i, e) for i, e in enumerate(ui_elements) if is_meaningful(e)
        ]

        return filtered_ui_elements_with_index

    @staticmethod
    def generate_ui_elements_description_list_full(
            ui_elements: list[representation_utils.UIElement],
            screen_width_height_px: tuple[int, int],
            goal: str = "",
    ) -> str:
        tree_info = ''
        ui_elements = UI_Elem_Description_Generator().filter_out_invalid_ui_elements(
            ui_elements, screen_width_height_px
        )
        log_to_file(f"UI elements: {ui_elements}")
        for index, ui_element in enumerate(ui_elements):
            tree_info += f'UI element {index}: {str(ui_element)}\n'

        return tree_info

    @staticmethod
    def generate_ui_elements_description_list_enhanced_filter(
            ui_elements: list[representation_utils.UIElement],
            screen_width_height_px: tuple[int, int],
            model_name: str,
            goal: str = "",
    ) -> str:
        log_to_file(ui_elements)
        """
        Generates a description of UI elements in a list format.
        """
        # Convert UIElement into str
        ui_elements=json.dumps([str(elem) for elem in ui_elements], indent=2, ensure_ascii=False)
        prompt = UI_Elem_Description_Generator(model_name).generate_general_ui_prompt(ui_elements,
                                                                                      goal)
        llm = infer.GeminiGcpWrapper(model_name)
        summary, _, _ = llm.predict(prompt)
        print("Summary generated for UI Elements: " + summary)

        result_str = f"""## UI Summary
        {summary.strip()}

        ## UI Elements (JSON)
        {json.dumps(ui_elements, indent=2, ensure_ascii=False)}
        """

        # 日志打印或写入文件
        log_to_file(result_str)

        return result_str

    @staticmethod
    def generate_ui_elements_description_list_llm(
            ui_elements: list[representation_utils.UIElement],
            screen_width_height_px: tuple[int, int],
            model_name: str,
            goal: str = "",
    ) -> str:
        filtered_ui_elements = UI_Elem_Description_Generator().filter_out_useless_ui_elements(
            ui_elements)

        original_description = UI_Elem_Description_Generator().convert_ui_elements_to_pure_json(
            filtered_ui_elements)

        prompt = (
            "You are assisting an autonomous agent operating on Android UI.\n"
            f"Task Goal: {goal}\n"
        )

        prompt += (
            "\nThe following is a list of UI elements on screen. Each element has an index and description.\n"
            "Your task: identify and return ONLY the UI elements that are **most relevant to the goal above**.\n"
            "Please do NOT renumber or reorder the indices. Just select the useful ones.\n"
            "Keep the output in the same format.\n\n"
            f"{original_description}\n\n"
            "Now return the filtered list:"
        )
        llm = infer.GeminiGcpWrapper(model_name)

        tree_info, _, _ = llm.predict(prompt)
        if not tree_info:
            tree_info = "No relevant UI elements found."
        log_to_file(f"Original UI elements: {json.dumps(original_description)}")
        log_to_file("UI elements:")
        log_to_file(json.dumps(tree_info, indent=2))
        return tree_info
