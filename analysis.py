# 24f1000656@ds.study.iitm.ac.in
# Marimo reactive notebook demonstrating relationships with interactivity.
# Cells are logically separated with comments; variables form the dependency graph.

import marimo as mo
import seaborn as sns
import matplotlib.pyplot as plt

# ---- Cell 1: Load dataset (base source for all downstream cells) ----
iris = sns.load_dataset("iris")

# ---- Cell 2: UI widgets (independent controls) ----
species_selector = mo.ui.dropdown(
    options=["All"] + iris["species"].unique().tolist(),
    value="All",
    label="Species"
)

x_feature = mo.ui.dropdown(
    options=iris.select_dtypes("number").columns.tolist(),
    value="sepal_length",
    label="X Feature"
)

y_feature = mo.ui.dropdown(
    options=iris.select_dtypes("number").columns.tolist(),
    value="sepal_width",
    label="Y Feature"
)

# REQUIRED: Interactive slider widget (controls sampling fraction)
sample_pct = mo.ui.slider(10, 100, value=100, label="Sample %")

# Render the controls in a single row
mo.hstack([species_selector, x_feature, y_feature, sample_pct])

# ---- Cell 3: Filter → Sample (depends on widgets & base data) ----
_filtered = iris if species_selector.value == "All" else iris[iris["species"] == species_selector.value]
_frac = sample_pct.value / 100.0
data_view = _filtered.sample(frac=_frac, random_state=42) if _frac < 1.0 else _filtered

# ---- Cell 4: Visualization (depends on data_view, x_feature, y_feature) ----
plt.figure(figsize=(7, 5))
sns.scatterplot(data=data_view, x=x_feature.value, y=y_feature.value, hue="species")
plt.title(f"{x_feature.value} vs {y_feature.value}  •  {len(data_view)} points (of {len(_filtered)})")
mo.show(plt)

# ---- Cell 5: Dynamic Markdown (reacts to all upstream values) ----
mo.md(f"""
### Current Selection
- **Species:** {species_selector.value}
- **X:** `{x_feature.value}`  •  **Y:** `{y_feature.value}`
- **Sample:** {sample_pct.value}% → **{len(data_view)}** / {len(_filtered)} points
- **Visual meter:** {"🟢" * max(1, sample_pct.value // 10)}
""")
