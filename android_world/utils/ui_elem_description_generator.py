from android_world.env import representation_utils
from android_world.agents import m3a_utils
from android_world.agents import infer


class UI_Elem_Description_Generator:
    """
    A class to generate descriptions for UI elements based on their properties.
    """

    def __init__(self):
        self.strategy_map = {0: self.generate_ui_elements_description_list_full,
                             1: self.generate_ui_elements_description_list_enhanced_filter,
                             2: self.generate_ui_elements_description_list_llm}

    def convert_ui_elements_to_description(
            self,
            ui_elements: list[tuple[int, representation_utils.UIElement]],
    ) -> str:
        description_lines = []
        for original_idx, elem in ui_elements:
            # 构造交互性标签
            tags = []
            if elem.is_clickable:
                tags.append("clickable")
            if elem.is_editable:
                tags.append("editable (text input field)")
            if elem.is_scrollable:
                tags.append("scrollable")

            tag_str = " / ".join(tags) if tags else "non-interactive"

            # 提取文本信息
            label = elem.text or elem.content_description or "<no label>"
            hint = elem.hint_text or ""
            label_info = f"label '{label}'"
            if hint:
                label_info += f" and hint '{hint}'"

            # 推测字段含义
            field_hint = ""
            combined_text = f"{label} {hint}".lower()
            for field in ['name', 'phone', 'email', 'search', 'contact']:
                if field in combined_text:
                    field_hint = f"(likely field: {field})"
                    break

            # 附加 class 类型（可选）
            class_type = elem.class_name.split('.')[-1] if elem.class_name else "unknown"

            # 构造自然语言描述
            line = (
                f"UI element {original_idx}: This is a {tag_str} UI element "
                f"with {label_info} {field_hint}. Type: {class_type}."
            )

            description_lines.append(line.strip())

        description_lines.insert(0,
                                 "Each UI element is indexed. Use this index directly when choosing elements to interact with. (Indices refer to the original UI layout.)")

        return "\n".join(description_lines)

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
                    or (e.text and e.text.strip())
                    or (e.content_description and e.content_description.strip())
            )

        for index, e in enumerate(ui_elements):
            if not is_meaningful(e):
                print(f"Filtered out: index{index} {e}")

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
        print(f"Before filtering, number of UI elements: {len(ui_elements)}")
        tree_info = ''
        ui_elements = UI_Elem_Description_Generator().filter_out_invalid_ui_elements(
            ui_elements, screen_width_height_px
        )
        print(f"After filtering, number of UI elements: {len(ui_elements)}")
        print(ui_elements)
        for index, ui_element in enumerate(ui_elements):
            tree_info += f'UI element {index}: {str(ui_element)}\n'

        return tree_info

    @staticmethod
    def generate_ui_elements_description_list_enhanced_filter(
            ui_elements: list[representation_utils.UIElement],
            screen_width_height_px: tuple[int, int],
            goal: str = "",
    ) -> str:
        """
        Generates a description of UI elements in a list format.
        """
        print(f"Before filtering, number of UI elements: {len(ui_elements)}")
        filtered_ui_elements = UI_Elem_Description_Generator().filter_out_useless_ui_elements(
            ui_elements)
        print(f"After filtering, number of UI elements: {len(filtered_ui_elements)}")

        tree_info = UI_Elem_Description_Generator().convert_ui_elements_to_description(
            filtered_ui_elements)

        # tree_info = ''
        # for original_index, ui_element in filtered_ui_elements:
        #     tree_info += f'UI element {original_index}: {str(ui_element)}\n'
        print(tree_info)
        return tree_info

    @staticmethod
    def generate_ui_elements_description_list_llm(
            ui_elements: list[representation_utils.UIElement],
            screen_width_height_px: tuple[int, int],
            goal: str = "",
    ) -> str:
        print(f"Before filtering, number of UI elements: {len(ui_elements)}")
        filtered_ui_elements = UI_Elem_Description_Generator().filter_out_useless_ui_elements(
            ui_elements)
        print(f"After filtering, number of UI elements: {len(filtered_ui_elements)}")

        original_description = UI_Elem_Description_Generator().convert_ui_elements_to_description(
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
        llm = infer.GeminiGcpWrapper('gemini-1.5-pro-latest')

        tree_info, _, _ = llm.predict(prompt)
        if not tree_info:
            tree_info = "No relevant UI elements found."
        print(tree_info)
        return tree_info
