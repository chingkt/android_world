from android_world.env.json_action import (
    CLICK,
    SCROLL,
    INPUT_TEXT,
    FILL_FORM,
    NAVIGATE_HOME,
    NAVIGATE_BACK,
    KEYBOARD_ENTER,
    OPEN_APP,
    STATUS,
    WAIT,
    LONG_PRESS,
    ANSWER,
)


PROMPT_CLICK_ACTION = (
    'You have selected the `click` action. Now construct the JSON for this action.\n'
    'Format: {"action_type": "click", "index": <target_index>}\n'
    'Guidelines:\n'
    '- The index must correspond to a visible and interactable UI element on the screen.\n'
    '- The agent should simulate a real tap: the click will be performed at the center of the element\'s bounding box.\n'
    '- Do not click on elements that are disabled, hidden, or overlapped by other UI elements.\n'
    '- Do not click on decorative or non-interactive elements (such as icons or separators).\n'
    '- If multiple elements have similar text, use the index that matches the intended target in the UI list.\n'
    '- Only include the "index" key, do not add extra fields.\n'
    'Common mistakes:\n'
    '- Using an index that is not present in the current UI element list.\n'
    '- Using an index for an element that is not visible or interactable (e.g., off-screen, covered, or grayed out).\n'
    '- Clicking on a label or static text instead of a button or input field.\n'
    '- Adding unnecessary keys or fields to the JSON.\n'
    '- Failing to update the index if the UI changes after a previous action.\n'
    'Example: {"action_type": "click", "index": 2}'
)

PROMPT_LONG_PRESS_ACTION = (
    'You have selected the `long_press` action. Now construct the JSON for this action.\n'
    'Format: {"action_type": "long_press", "index": <target_index>}\n'
    'Guidelines:\n'
    '- The index must correspond to a visible and interactable UI element on the screen.\n'
    '- The agent should simulate a real long press: the press will be performed at the center of the element\'s bounding box and held for a longer duration.\n'
    '- Do not long press on elements that are disabled, hidden, overlapped, or non-interactive (such as icons, separators, or static text).\n'
    '- If multiple elements have similar text, use the index that matches the intended target in the UI list.\n'
    '- Only include the "index" key, do not add extra fields.\n'
    'Common mistakes:\n'
    '- Using an index that is not present in the current UI element list.\n'
    '- Using an index for an element that is not visible or interactable (e.g., off-screen, covered, or grayed out).\n'
    '- Long pressing on a label or static text instead of a button, input field, or selectable item.\n'
    '- Adding unnecessary keys or fields to the JSON.\n'
    '- Failing to update the index if the UI changes after a previous action.\n'
    'Example: {"action_type": "long_press", "index": 1}'
)

PROMPT_INPUT_TEXT_ACTION = (
    'You have selected the `input_text` action. Now construct the JSON for this action.\n'
    'Format: {"action_type": "input_text", "text": <text_input>, "index": <target_index>}\n'
    'Guidelines:\n'
    '- "text" is the exact string to type into the field.\n'
    '- "index" must correspond to a visible and editable text field on the screen.\n'
    '- The agent should simulate a real user: first focus (click) the field, then type the text, and finally press enter.\n'
    '- Do not use indices for non-editable or decorative elements.\n'
    '- Do not include extra keys or fields.\n'
    '- If multiple fields are similar, use the index that matches the intended target in the UI list.\n'
    'Common mistakes:\n'
    '- Omitting either "text" or "index".\n'
    '- Using an index for an element that is not visible, not editable, or not a text field.\n'
    '- Typing into a label, button, or static text instead of an input field.\n'
    '- Adding unnecessary keys or fields to the JSON.\n'
    '- Failing to update the index if the UI changes after a previous action.\n'
    'Example: {"action_type": "input_text", "text": "hello", "index": 3}'
)

PROMPT_FILL_FORM_ACTION = (
    'You have selected the `fill_form` action. Now construct the JSON for this action.\n'
    'Format: {"action_type": "fill_form", "form": [\n'
    '  {"text": <text_input_1>, "index": <target_index_1>},\n'
    '  {"text": <text_input_2>, "index": <target_index_2>}\n'
    ']}\n'
    'Guidelines:\n'
    '- Do not click on a dropdown menu or a non-editable field.\n'
    '- Each item in "form" must have "text" and "index".\n'
    '- The agent should simulate a real user: for each field, first focus (click) the field (by index), then type the text, and finally press enter.\n'
    '- Only use indices for visible and **editable** text fields.\n'
    '- Do not add extra keys or fields.\n'
    '- If multiple fields are similar, use the index that match the intended target in the UI list.\n'
    '- The order of fields in the form should match the logical order of filling the form on the screen.\n'
    'Common mistakes:\n'
    '- Clicking the dropdown menu, which is not editable, instead of the input field.\n'
    '- Omitting either "text" or the field location ("index").\n'
    '- Using an index for an element that is not visible, not editable, or not a text field.\n'
    '- Typing into a label, button, or static text instead of an input field.\n'
    '- Adding unnecessary keys or fields to the JSON.\n'
    '- Failing to update the index if the UI changes after a previous action.\n'
    '- Using out-of-range indices that do not correspond to any UI element.\n'
    'Example: {"action_type": "fill_form", "form": [{"text": "John", "index": 2}, {"text": "Doe", "index": 3}]}'
)

PROMPT_ANSWER_ACTION = (
    'You have selected the `answer` action. Now construct the JSON for this action.\n'
    'Format: {"action_type": "answer", "text": <answer_text>}\n'
    'Guidelines:\n'
    '- "text" should be a clear, concise, and direct answer to the user\'s question or request.\n'
    '- The answer should be relevant and factually correct based on the information available on the device.\n'
    '- Do not include extra keys or fields.\n'
    '- If the answer is not known or cannot be determined, state so clearly in the text.\n'
    '- If the answer is a list or multiple items, format it as a single string (e.g., comma-separated or bulleted).\n'
    'Common mistakes:\n'
    '- Forgetting the "text" key.\n'
    '- Providing an answer that is not relevant to the user\'s request.\n'
    '- Including UI element indices, JSON, or code in the answer text.\n'
    '- Adding unnecessary keys or fields to the JSON.\n'
    '- Using vague or incomplete answers (e.g., just saying "done" or "okay").\n'
    'Example: {"action_type": "answer", "text": "You have no events today."}'
)

PROMPT_STATUS_ACTION = (
    'You have selected the `status` action. Now construct the JSON for this action.\n'
    'Format: {"action_type": "status", "goal_status": <complete|infeasible>}\n'
    'Guidelines:\n'
    '- Use "complete" if the task is done, "infeasible" if it cannot be done.\n'
    '- Only use the allowed values for "goal_status".\n'
    '- Do not add extra keys or fields.\n'
    'Common mistakes:\n'
    '- Misspelling "goal_status" or using an invalid value.\n'
    '- Adding unnecessary keys or fields to the JSON.\n'
    'Example: {"action_type": "status", "goal_status": "complete"}'
)

PROMPT_KEYBOARD_ENTER_ACTION = (
    'You have selected the `keyboard_enter` action. Now construct the JSON for this action.\n'
    'Format: {"action_type": "keyboard_enter"}\n'
    'Guidelines:\n'
    '- No extra keys or fields.\n'
    '- Use this action only when you want to simulate pressing the Enter key on the keyboard.\n'
    'Common mistakes:\n'
    '- Adding unnecessary keys or fields to the JSON.\n'
    'Example: {"action_type": "keyboard_enter"}'
)

PROMPT_NAVIGATE_HOME_ACTION = (
    'You have selected the `navigate_home` action. Now construct the JSON for this action.\n'
    'Format: {"action_type": "navigate_home"}\n'
    'Guidelines:\n'
    '- No extra keys or fields.\n'
    '- Use this action only to return to the home screen.\n'
    'Common mistakes:\n'
    '- Adding unnecessary keys or fields to the JSON.\n'
    'Example: {"action_type": "navigate_home"}'
)

PROMPT_NAVIGATE_BACK_ACTION = (
    'You have selected the `navigate_back` action. Now construct the JSON for this action.\n'
    'Format: {"action_type": "navigate_back"}\n'
    'Guidelines:\n'
    '- No extra keys or fields.\n'
    '- Use this action only to simulate pressing the back button.\n'
    'Common mistakes:\n'
    '- Adding unnecessary keys or fields to the JSON.\n'
    'Example: {"action_type": "navigate_back"}'
)

PROMPT_SCROLL_ACTION = (
    'You have selected the `scroll` action. Now construct the JSON for this action.\n'
    'Format: {"action_type": "scroll", "direction": <up|down|left|right>, "index": <optional_target_index>}\n'
    'Guidelines:\n'
    '- "direction" must be one of up, down, left, right.\n'
    '- "index" is optional; omit if scrolling the whole screen.\n'
    '- Only use indices for visible and scrollable UI elements.\n'
    '- Do not add extra keys or fields.\n'
    '- Make sure the direction matches the intended scroll (e.g., "down" to see content below).\n'
    'Common mistakes:\n'
    '- Misspelling direction or using an invalid value.\n'
    '- Using an index for a non-scrollable or invisible element.\n'
    '- Adding unnecessary keys or fields to the JSON.\n'
    'Example: {"action_type": "scroll", "direction": "down", "index": 2}'
)

PROMPT_OPEN_APP_ACTION = (
    'You have selected the `open_app` action. Now construct the JSON for this action.\n'
    'Format: {"action_type": "open_app", "app_name": <name>}\n'
    'Guidelines:\n'
    '- "app_name" must be the exact name of the app as it appears on the device.\n'
    '- No extra keys or fields.\n'
    '- Use this action only to open an app directly.\n'
    'Common mistakes:\n'
    '- Misspelling the app name or using an unofficial name.\n'
    '- Adding unnecessary keys or fields to the JSON.\n'
    'Example: {"action_type": "open_app", "app_name": "Calendar"}'
)

PROMPT_WAIT_ACTION = (
    'You have selected the `wait` action. Now construct the JSON for this action.\n'
    'Format: {"action_type": "wait"}\n'
    'Guidelines:\n'
    '- No extra keys or fields.\n'
    '- Use this action to wait for the screen to update or for a process to complete.\n'
    'Common mistakes:\n'
    '- Adding unnecessary keys or fields to the JSON.\n'
    'Example: {"action_type": "wait"}'
)

ACTION_EXECUTION_PROMPT_TEMPLATE = (
        '{prompt_for_selected_action}'
        + '\nThe current user goal/request is: {goal}'
        + '\n\nHere is a history of what you have done so far:\n{history}'
        + '\n\nHere is a list of descriptions for some UI elements on the current'
          ' screen:\n{ui_elements_description}\n'
        + '{additional_guidelines}'
        + '\n\nNow output the action details in the correct JSON format,'
          ' following the reason why you do that. Your answer should look like:\n'
          'Reason: ...\nAction: {{"action_type":...}}\n\n'
          'Your Answer:\n'
)

ACTION_KEY_TO_PROMPT = {
    CLICK: PROMPT_CLICK_ACTION,
    LONG_PRESS: PROMPT_LONG_PRESS_ACTION,
    INPUT_TEXT: PROMPT_INPUT_TEXT_ACTION,
    FILL_FORM: PROMPT_FILL_FORM_ACTION,
    ANSWER: PROMPT_ANSWER_ACTION,
    STATUS: PROMPT_STATUS_ACTION,
    KEYBOARD_ENTER: PROMPT_KEYBOARD_ENTER_ACTION,
    NAVIGATE_HOME: PROMPT_NAVIGATE_HOME_ACTION,
    NAVIGATE_BACK: PROMPT_NAVIGATE_BACK_ACTION,
    SCROLL: PROMPT_SCROLL_ACTION,
    OPEN_APP: PROMPT_OPEN_APP_ACTION,
    WAIT: PROMPT_WAIT_ACTION,
}

__all__ = [ACTION_KEY_TO_PROMPT, ACTION_EXECUTION_PROMPT_TEMPLATE]
