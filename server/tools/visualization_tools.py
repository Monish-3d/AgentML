import matplotlib.pyplot as plt
import seaborn as sns

def plot_histograms(df):

    numeric = df.select_dtypes(include=["int64","float64"])

    figs = []

    for col in numeric.columns:

        fig, ax = plt.subplots()

        sns.histplot(df[col], kde=True, ax=ax)

        ax.set_title(f"Distribution of {col}")

        figs.append(fig)

    return figs


def plot_correlation(corr):

    fig, ax = plt.subplots(figsize=(8,6))

    sns.heatmap(corr, annot=True, cmap="coolwarm", ax=ax)

    ax.set_title("Correlation Matrix")

    return fig


def plot_pairPlot(df):
    fig, ax = plt.subplots(figsize=(8,6))

    numeric = df.select_dtypes(include=["int64", "float64"])
    figure = sns.pairplot(numeric)

    ax.set_title("Pair Plot")

    return figure.figure