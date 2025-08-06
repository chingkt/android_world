from PIL import Image, ImageDraw, ImageFont
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

# First table (from earlier)
#UI Filtering
# table1 = {
#     'easy': {
#         'complex_ui_understanding': 0.11, 'data_edit': 0.33, 'data_entry': 0.14,
#         'game_playing': 0.00, 'information_retrieval': 0.43, 'math_counting': 0.00,
#         'memorization': 0.00, 'multi_app': 0.00, 'parameterized': 0.31,
#         'repetition': 0.00, 'requires_setup': 0.33, 'screen_reading': 0.53,
#         'search': 0.27, 'transcription': 0.33, 'untagged': 0.33, 'verification': 0.52
#     },
#     'medium': {
#         'complex_ui_understanding': 0.08, 'data_edit': 0.05, 'data_entry': 0.04,
#         'game_playing': np.nan, 'information_retrieval': 0.15, 'math_counting': 0.0,
#         'memorization': 0.0, 'multi_app': 0.0, 'parameterized': 0.07,
#         'repetition': 0.0, 'requires_setup': 0.0, 'screen_reading': 0.11,
#         'search': 0.07, 'transcription': 0.0, 'untagged': 0.5, 'verification': np.nan
#     },
#     'hard': {
#         'complex_ui_understanding': 0.2, 'data_edit': 0.0, 'data_entry': 0.0,
#         'game_playing': np.nan, 'information_retrieval': 0.0, 'math_counting': 0.22,
#         'memorization': 0.11, 'multi_app': 0.0, 'parameterized': 0.1,
#         'repetition': 0.0, 'requires_setup': 0.0, 'screen_reading': 0.07,
#         'search': 0.07, 'transcription': 0.0, 'untagged': np.nan, 'verification': np.nan
#     }
# }

# without UI summary
# table1 = {
#     'easy': {
#         'complex_ui_understanding': 0.17, 'data_edit': 0.36, 'data_entry': 0.33,
#         'game_playing': 0.00, 'information_retrieval': 0.14, 'math_counting': 0.00,
#         'memorization': 0.00, 'multi_app': 0.00, 'parameterized': 0.32,
#         'repetition': 0.00, 'requires_setup': 0.67, 'screen_reading': 0.33,
#         'search': 0.45, 'transcription': 0.50, 'untagged': 0.40, 'verification': 0.43
#     },
#     'medium': {
#         'complex_ui_understanding': 0.0, 'data_edit': 0.29, 'data_entry': 0.0,
#         'game_playing': np.nan, 'information_retrieval': 0.0, 'math_counting': 0.0,
#         'memorization': 0.0, 'multi_app': 0.0, 'parameterized': 0.12,
#         'repetition': 0.0, 'requires_setup': 0.0, 'screen_reading': 0.0,
#         'search': 0.0, 'transcription': 0.0, 'untagged': 0.5, 'verification': np.nan
#     },
#     'hard': {
#         'complex_ui_understanding': 0.14, 'data_edit': 0.0, 'data_entry': 0.11,
#         'game_playing': np.nan, 'information_retrieval': 0.0, 'math_counting': 0.0,
#         'memorization': 0.0, 'multi_app': 0.0, 'parameterized': 0.11,
#         'repetition': 0.2, 'requires_setup': 0.0, 'screen_reading': 0.11,
#         'search': 0.0, 'transcription': 0.0, 'untagged': np.nan, 'verification': np.nan
#     }
# }

# All features
baseline = {
    'easy': {
        'complex_ui_understanding': 0.33, 'data_edit': 0.61, 'data_entry': 0.24,
        'game_playing': 0.00, 'information_retrieval': 0.24, 'math_counting': 0.00,
        'memorization': 0.00, 'multi_app': 0.00, 'parameterized': 0.37,
        'repetition': 0.17, 'requires_setup': 0.56, 'screen_reading': 0.61,
        'search': 0.42, 'transcription': 0.33, 'untagged': 0.60, 'verification': 0.76
    },
    'medium': {
        'complex_ui_understanding': 0.2, 'data_edit': 0.1, 'data_entry': 0.03,
        'game_playing': np.nan, 'information_retrieval': 0.19, 'math_counting': 0.22,
        'memorization': 0.0, 'multi_app': 0.0, 'parameterized': 0.12,
        'repetition': 0.07, 'requires_setup': 0.0, 'screen_reading': 0.22,
        'search': 0.13, 'transcription': 0.0, 'untagged': 0.33, 'verification': np.nan
    },
    'hard': {
        'complex_ui_understanding': 0.19, 'data_edit': 0.0, 'data_entry': 0.11,
        'game_playing': np.nan, 'information_retrieval': 0.0, 'math_counting': 0.0,
        'memorization': 0.0, 'multi_app': 0.06, 'parameterized': 0.22,
        'repetition': 0.27, 'requires_setup': 0.0, 'screen_reading': 0.19,
        'search': 0.17, 'transcription': 0.0, 'untagged': np.nan, 'verification': np.nan
    }
}

# without action detail and memory
table1 = {
    'easy': {
        'complex_ui_understanding': 0.17, 'data_edit': 0.36, 'data_entry': 0.33,
        'game_playing': 0.00, 'information_retrieval': 0.29, 'math_counting': 0.00,
        'memorization': 0.00, 'multi_app': 0.00, 'parameterized': 0.36,
        'repetition': 0.50, 'requires_setup': 0.67, 'screen_reading': 0.75,
        'search': 0.55, 'transcription': 0.50, 'untagged': 0.60, 'verification': 0.71
    },
    'medium': {
        'complex_ui_understanding': 0.0, 'data_edit': 0.14, 'data_entry': 0.1,
        'game_playing': np.nan, 'information_retrieval': 0.0, 'math_counting': 0.0,
        'memorization': 0.0, 'multi_app': 0.0, 'parameterized': 0.06,
        'repetition': 0.2, 'requires_setup': 0.0, 'screen_reading': 0.0,
        'search': 0.0, 'transcription': 0.0, 'untagged': 1.0, 'verification': np.nan
    },
    'hard': {
        'complex_ui_understanding': 0.0, 'data_edit': 0.0, 'data_entry': 0.11,
        'game_playing': np.nan, 'information_retrieval': 0.0, 'math_counting': 0.0,
        'memorization': 0.0, 'multi_app': 0.17, 'parameterized': 0.17,
        'repetition': 0.4, 'requires_setup': 0.0, 'screen_reading': 0.11,
        'search': 0.17, 'transcription': 0.0, 'untagged': np.nan, 'verification': np.nan
    }
}

# # without action execution
# table1 = {
#     'easy': {
#         'complex_ui_understanding': 0.44, 'data_edit': 0.55, 'data_entry': 0.36,
#         'game_playing': 0.00, 'information_retrieval': 0.38, 'math_counting': 0.00,
#         'memorization': 0.00, 'multi_app': 0.00, 'parameterized': 0.42,
#         'repetition': 0.00, 'requires_setup': 0.56, 'screen_reading': 0.69,
#         'search': 0.48, 'transcription': 0.50, 'untagged': 0.47, 'verification': 0.86
#     },
#     'medium': {
#         'complex_ui_understanding': 0.2, 'data_edit': 0.14, 'data_entry': 0.07,
#         'game_playing': np.nan, 'information_retrieval': 0.22, 'math_counting': 0.22,
#         'memorization': 0.0, 'multi_app': 0.0, 'parameterized': 0.16,
#         'repetition': 0.13, 'requires_setup': 0.0, 'screen_reading': 0.11,
#         'search': 0.27, 'transcription': 0.0, 'untagged': 0.33, 'verification': np.nan
#     },
#     'hard': {
#         'complex_ui_understanding': 0.05, 'data_edit': 0.0, 'data_entry': 0.0,
#         'game_playing': np.nan, 'information_retrieval': 0.0, 'math_counting': 0.0,
#         'memorization': 0.0, 'multi_app': 0.0, 'parameterized': 0.09,
#         'repetition': 0.2, 'requires_setup': 0.0, 'screen_reading': 0.07,
#         'search': 0.11, 'transcription': 0.0, 'untagged': np.nan, 'verification': np.nan
#     }
# }

# without memory
# table1 = {
#     'easy': {
#         'complex_ui_understanding': 0.33, 'data_edit': 0.61, 'data_entry': 0.40,
#         'game_playing': 0.00, 'information_retrieval': 0.29, 'math_counting': 0.00,
#         'memorization': 0.00, 'multi_app': 0.00, 'parameterized': 0.43,
#         'repetition': 0.00, 'requires_setup': 0.78, 'screen_reading': 0.47,
#         'search': 0.48, 'transcription': 0.17, 'untagged': 0.47, 'verification': 0.71
#     },
#     'medium': {
#         'complex_ui_understanding': 0.13, 'data_edit': 0.10, 'data_entry': 0.13,
#         'game_playing': np.nan, 'information_retrieval': 0.22, 'math_counting': 0.44,
#         'memorization': 0.0, 'multi_app': 0.0, 'parameterized': 0.15,
#         'repetition': 0.07, 'requires_setup': 0.0, 'screen_reading': 0.11,
#         'search': 0.07, 'transcription': 0.0, 'untagged': 0.5, 'verification': np.nan
#     },
#     'hard': {
#         'complex_ui_understanding': 0.10, 'data_edit': 0.0, 'data_entry': 0.11,
#         'game_playing': np.nan, 'information_retrieval': 0.0, 'math_counting': 0.22,
#         'memorization': 0.17, 'multi_app': 0.06, 'parameterized': 0.13,
#         'repetition': 0.27, 'requires_setup': 0.0, 'screen_reading': 0.15,
#         'search': 0.11, 'transcription': 0.0, 'untagged': np.nan, 'verification': np.nan
#     }
# }

# without fill_form
# table1 = {
#     'easy': {
#         'complex_ui_understanding': 0.17, 'data_edit': 0.36, 'data_entry': 0.20,
#         'game_playing': 0.00, 'information_retrieval': 0.14, 'math_counting': 0.00,
#         'memorization': 0.00, 'multi_app': 0.00, 'parameterized': 0.27,
#         'repetition': 0.00, 'requires_setup': 0.33, 'screen_reading': 0.42,
#         'search': 0.27, 'transcription': 0.00, 'untagged': 0.60, 'verification': 0.71
#     },
#     'medium': {
#         'complex_ui_understanding': 0.4, 'data_edit': 0.29, 'data_entry': 0.0,
#         'game_playing': np.nan, 'information_retrieval': 0.11, 'math_counting': 0.33,
#         'memorization': 0.0, 'multi_app': 0.0, 'parameterized': 0.15,
#         'repetition': 0.2, 'requires_setup': 0.0, 'screen_reading': 0.0,
#         'search': 0.2, 'transcription': 0.0, 'untagged': 0.0, 'verification': np.nan
#     },
#     'hard': {
#         'complex_ui_understanding': 0.14, 'data_edit': 0.0, 'data_entry': 0.0,
#         'game_playing': np.nan, 'information_retrieval': 0.0, 'math_counting': 0.0,
#         'memorization': 0.0, 'multi_app': 0.0, 'parameterized': 0.14,
#         'repetition': 0.3, 'requires_setup': 0.0, 'screen_reading': 0.11,
#         'search': 0.08, 'transcription': 0.0, 'untagged': np.nan, 'verification': np.nan
#     }
# }

# Second table
# baseline = {
#     'easy': {
#         'complex_ui_understanding': 0.22, 'data_edit': 0.52, 'data_entry': 0.33,
#         'game_playing': 0.00, 'information_retrieval': 0.17, 'math_counting': 0.00,
#         'memorization': 0.00, 'multi_app': 0.00, 'parameterized': 0.37,
#         'repetition': 0.00, 'requires_setup': 0.67, 'screen_reading': 0.47,
#         'search': 0.57, 'transcription': 0.33, 'untagged': 0.47, 'verification': 0.33
#     },
#     'medium': {
#         'complex_ui_understanding': 0.17, 'data_edit': 0.17, 'data_entry': 0.04,
#         'game_playing': np.nan, 'information_retrieval': 0.33, 'math_counting': 0.33,
#         'memorization': 0.0, 'multi_app': 0.0, 'parameterized': 0.21,
#         'repetition': 0.08, 'requires_setup': 0.0, 'screen_reading': 0.33,
#         'search': 0.33, 'transcription': 0.0, 'untagged': 0.0, 'verification': np.nan
#     },
#     'hard': {
#         'complex_ui_understanding': 0.05, 'data_edit': 0.0, 'data_entry': 0.04,
#         'game_playing': np.nan, 'information_retrieval': 0.0, 'math_counting': 0.0,
#         'memorization': 0.0, 'multi_app': 0.0, 'parameterized': 0.1,
#         'repetition': 0.17, 'requires_setup': 0.0, 'screen_reading': 0.15,
#         'search': 0.03, 'transcription': 0.0, 'untagged': np.nan, 'verification': np.nan
#     }
# }

df1 = pd.DataFrame(table1)
df2 = pd.DataFrame(baseline)

# Comparison DataFrame
def compare_values(v1, v2):
    if np.isnan(v1) and np.isnan(v2):
        return "", "white"
    if v1 == 0.0 and v2 == 0.0:
        return "", "white"
    if pd.isna(v1):
        return "NaN < " + f"{v2:.2f}", "red"
    if pd.isna(v2):
        return f"{v1:.2f} > NaN", "green"
    if v1 > v2:
        return f"{v1:.2f} > {v2:.2f}", "green"
    elif v1 < v2:
        return f"{v1:.2f} < {v2:.2f}", "red"
    else:
        return f"{v1:.2f} = {v2:.2f}", "white"

comparison_df = pd.DataFrame(index=df1.index, columns=df1.columns)
color_df = pd.DataFrame(index=df1.index, columns=df1.columns)

for row in df1.index:
    for col in df1.columns:
        comp, color = compare_values(df1.at[row, col], df2.at[row, col])
        comparison_df.at[row, col] = comp
        color_df.at[row, col] = color

# Calculate Net % Increase row for each difficulty
net_pct_increase = {}
for col in df1.columns:
    vals1 = df1[col]
    vals2 = df2[col]
    pct_increases = []
    for v1, v2 in zip(vals1, vals2):
        if pd.isna(v1) or pd.isna(v2):
            continue
        if v2 == 0:
            continue  # Avoid division by zero
        pct_increases.append((v1 - v2) / v2 * 100)
    net_pct_increase[col] = np.nanmean(pct_increases) if pct_increases else np.nan

# Add Net % Increase row to comparison_df and color_df
comparison_df.loc['Net % Increase'] = [f"{net_pct_increase[col]:.1f}%" if not pd.isna(net_pct_increase[col]) else "NaN" for col in comparison_df.columns]
color_df.loc['Net % Increase'] = ["white"] * len(comparison_df.columns)

# Create image with color-coded cells (including Net % Increase row)
fig, ax = plt.subplots(figsize=(10, 8))
ax.axis('off')
tbl = plt.table(cellText=comparison_df.values,
                rowLabels=comparison_df.index,
                colLabels=["Easy", "Medium", "Hard"],
                cellColours=color_df.replace({
                    "green": "#A8E6A2", "red": "#F4A6A6", "white": "#FFFFFF"
                }).values,
                loc='center',
                cellLoc='center',
                rowLoc='center',
                colLoc='center')

# Highlight Net % Increase row (handle table cell indexing safely)
net_row_idx = list(comparison_df.index).index('Net % Increase')
for col_idx in range(len(comparison_df.columns)):
    cell_key = (net_row_idx + 1, col_idx)  # +1 for header offset
    if cell_key in tbl._cells:
        tbl[cell_key].set_facecolor('#DDEBF7')
        tbl[cell_key].set_fontsize(12)
        tbl[cell_key].set_text_props(weight='bold')

# Save image
output_path = "visualization/vis_wo_action_detail_and_memory_with_avg.png"
plt.savefig(output_path, bbox_inches='tight')
plt.close()

output_path
