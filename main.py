import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# --- Streamlit Sidebar Inputs ----------------------------------------
st.title("Endurance Efficiency Visualizer")

endurance_level = st.slider("Endurance Level", 0, 13, 8)
control = st.slider("Control", 0, 13, 11)
complexity = st.slider("Complexity", 0, 13, 0)
stat_level = st.slider("Stat Level", 1, 13, 13)

# --- LINEAR ENDURANCE POOL --------------------------------------------
min_endurance = 20
max_endurance = 520
endurance_values = np.linspace(min_endurance, max_endurance, 14)
total_endurance_pool = endurance_values[endurance_level]

# --- CONTROL & COMPLEXITY MULTIPLIER ----------------------------------
def control_complexity_multiplier(control, complexity):
    if control >= complexity:
        return 1.0
    else:
        return control / max(1, complexity)  # Prevent divide-by-zero

cc_multiplier = control_complexity_multiplier(control, complexity)

# --- OUTPUT RANGE AND COST CALC ---------------------------------------
output_values = np.linspace(1, stat_level, 300)
execution_costs = output_values
adjusted_pool = total_endurance_pool * cc_multiplier
uses_possible = np.divide(adjusted_pool, execution_costs, out=np.zeros_like(execution_costs), where=execution_costs > 0)

# --- BURST, MID, FADE LOGIC -------------------------------------------
burst_index = np.argmax(output_values >= stat_level * 0.95)
fade_index = np.argmax(output_values >= stat_level * 0.05)
mid_index = (burst_index + fade_index) // 2

sample_indices = [burst_index, mid_index, fade_index]
sample_outputs = [output_values[i] for i in sample_indices]
sample_uses = [uses_possible[i] for i in sample_indices]
sample_labels = ['Burst (High Output)', 'Mid Output', 'Fade (Low Output)']
sample_colors = ['orange', 'green', 'purple']

# --- PLOTTING ---------------------------------------------------------
fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(output_values, uses_possible, label='Uses vs Output', color='crimson', linewidth=2)

# Annotate key points
for i in range(3):
    ax.scatter(sample_outputs[i], sample_uses[i], color=sample_colors[i], s=80,
               label=f'{sample_labels[i]}: {sample_uses[i]:.1f}x @ {sample_outputs[i]:.1f}')

# Compute max use and set Y limit to avoid squashed plots
max_use = np.max(uses_possible)
min_use = np.min(uses_possible)
min_visual_y = 20  # Ensure minimum visual height for clarity
y_limit = max(max_use * 1.1, min_visual_y)
ax.set_ylim(0, y_limit)

# Keep x-axis fixed to full stat range
ax.set_xlim(0, 13)

# Annotation box
ax.text(1, y_limit * 0.85,
        f'Max Uses: {max_use:.1f}x\nMin Uses: {min_use:.1f}x\nAdjusted Pool: {adjusted_pool:.1f}',
        bbox=dict(facecolor='white', alpha=0.8), fontsize=10)

# Labels and layout
ax.set_xlabel('Output Power (Stat Level)')
ax.set_ylabel('Number of Uses (Adjusted)')
ax.set_title(f'Stat={stat_level}, Control={control}, Complexity={complexity}, Endurance={int(total_endurance_pool)}')
ax.grid(True)
ax.legend()
st.pyplot(fig)
