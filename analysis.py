# 24f1000656@ds.study.iitm.ac.in
import marimo as mo
import seaborn as sns
import matplotlib.pyplot as plt

# Cell 1: data
iris = sns.load_dataset("iris")

# Cell 2: widgets
species = mo.ui.dropdown(["All"] + iris["species"].unique().tolist(), value="All", label="Species")
x = mo.ui.dropdown(iris.select_dtypes("number").columns.tolist(), value="sepal_length", label="X")
y = mo.ui.dropdown(iris.select_dtypes("number").columns.tolist(), value="sepal_width", label="Y")
mo.hstack([species, x, y])

# Cell 3: filter depends on widget values
f = iris if species.value == "All" else iris[iris["species"] == species.value]

# Cell 4: plot depends on filtered data and features
plt.figure(figsize=(6,4))
sns.scatterplot(data=f, x=x.value, y=y.value, hue="species")
plt.title(f"{x.value} vs {y.value}")
mo.show(plt)

# Cell 5: dynamic markdown
mo.md(f"**Species:** {species.value} · **Points:** {len(f)}")
