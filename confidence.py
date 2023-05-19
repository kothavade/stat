import matplotlib.pyplot as plt
import numpy as np
import scipy.stats as st


class BaseConfidenceInterval:
    def __init__(self, confidence: float):
        self.confidence = confidence

    def plot(self, dist, mean, moe) -> plt.Figure:
        fig, ax = plt.subplots()
        x = np.linspace(dist.ppf(0.001), dist.ppf(0.999), 100)
        ax.plot(x, dist.pdf(x), c="k")
        ax.axvline(mean, c="k", label="mean")
        ax.axvline(mean - moe, c="b", ls="--")
        ax.axvline(mean + moe, c="b", ls="--")
        ax.fill_between(
            x,
            dist.pdf(x),
            where=(x > mean - moe) & (x < mean + moe),
            color="b",
            alpha=0.2,
            label=f"{int(self.confidence * 100)}% confidence interval",
        )
        ax.legend()
        return fig


class MeanConfidenceInterval(BaseConfidenceInterval):
    def __init__(self, data: list[int], confidence: float):
        super().__init__(confidence)
        self.data = data
        self.n = len(data)
        self.m = np.mean(data)
        self.std_err = st.sem(data)
        self.tval = st.t.ppf((1 + confidence) / 2, self.n - 1)
        self.moe = self.std_err * self.tval
        self.df = self.n - 1
        self.x = st.t.interval(confidence, self.df, loc=np.mean(data), scale=st.sem(data))
        self.dist = st.t(self.df, loc=self.m, scale=self.std_err)

    def plot(self) -> plt.Figure:
        return super().plot(self.dist, self.m, self.moe)


class ProportionConfidenceInterval(BaseConfidenceInterval):
    def __init__(self, proportion: float, n: int, confidence: float):
        super().__init__(confidence)
        self.proportion = proportion
        self.n = n
        self.zval = st.norm.ppf((1 + confidence) / 2)
        self.moe = self.zval * np.sqrt((proportion * (1 - proportion)) / n)
        self.std_err = np.sqrt((proportion * (1 - proportion)) / n)
        self.x = st.norm.interval(confidence, loc=proportion, scale=np.sqrt((proportion * (1 - proportion)) / n))
        self.dist = st.norm(loc=proportion, scale=self.std_err)

    def plot(self) -> plt.Figure:
        return super().plot(self.dist, self.proportion, self.moe)
