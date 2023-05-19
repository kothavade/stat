import streamlit as str

from confidence import MeanConfidenceInterval, ProportionConfidenceInterval


def main():
    # rename tab

    str.title("Confidence Interval Calculator")
    str.sidebar.title("Caluculator Options")
    str.sidebar.write("This app calculates confidence intervals for means and proportions.")
    str.sidebar.write("Please select the type of confidence interval you would like to calculate.")

    tabs = ["Mean", "Proportion"]
    tab = str.sidebar.radio("Type of Confidence Interval", tabs)

    detail = str.sidebar.checkbox("Show Details", value=False)

    if tab == "Mean":
        str.sidebar.write("Please input the data and confidence level for the mean.")
        data = str.sidebar.text_input("Data", value="12, 12, 13, 13, 14, 15")
        confidence = str.sidebar.slider("Confidence Level", min_value=0.5, max_value=0.99, value=0.95, step=0.01)
        data = [int(i) for i in data.split(",")]
        t = MeanConfidenceInterval(data, confidence)

        if detail:
            str.write("#### Mean ± t-value * Standard Deviation / sqrt(n)")
            str.write(f"{t.m:.4f} ± {t.tval:.4f} * {t.std_err:.4f} / sqrt({t.n})")

            str.write("#### Mean ± t-value * Standard Error")
            str.write(f"{t.m:.4f} ± {t.tval:.4f} * {t.std_err:.4f}")

            str.write("#### Mean ± Margin of Error")
            str.write(f"{t.m:.4f} ± {t.moe:.4f}")
        else:
            str.write(f"{t.m:.4f} ± {t.moe:.4f}")

        str.write(f"{t.x[0]:.4f} < {t.m:.4f} < {t.x[1]:.4f}")

        str.pyplot(t.plot())
    else:  # tab == "Proportion"
        str.sidebar.write("Please input the proportion and sample size for the proportion.")
        prop = str.sidebar.slider("Proportion", min_value=0.01, max_value=0.99, value=0.1, step=0.01)
        n = str.sidebar.slider("Sample Size", min_value=10, max_value=1000, value=100, step=10)
        confidence = str.sidebar.slider("Confidence Level", min_value=0.5, max_value=0.99, value=0.95, step=0.01)
        z = ProportionConfidenceInterval(prop, n, confidence)

        if detail:
            str.write("#### Proportion ± z-value * Standard Deviation / sqrt(n)")
            str.write(f"{z.proportion:.4f} ± {z.zval:.4f} * {z.std_err:.4f} / sqrt({z.n})")

            str.write("#### Proportion ± z-value * Standard Error")
            str.write(f"{z.proportion:.4f} ± {z.zval:.4f} * {z.std_err:.4f}")

            str.write("#### Proportion ± Margin of Error")
            str.write(f"{z.proportion:.4f} ± {z.moe:.4f}")

        else:
            str.write(f"{z.proportion:.4f} ± {z.moe:.4f}")

        str.write(f"{z.x[0]:.4f} < {z.proportion:.4f} < {z.x[1]:.4f}")

        str.pyplot(z.plot())


if __name__ == "__main__":
    main()
