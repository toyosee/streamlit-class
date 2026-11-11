import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from statsmodels.tsa.seasonal import seasonal_decompose
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
from datetime import datetime

st.title("Interactive Data Explorer Tool")

# --- File Upload ---
uploaded_file = st.sidebar.file_uploader("Upload your CSV file", type=["csv"])
if uploaded_file:
    df = pd.read_csv(uploaded_file)
    numeric_cols = df.select_dtypes(include=np.number).columns.tolist()

    # --- Tabs Layout ---
    tab1, tab2, tab3, tab4 = st.tabs(["📑 Data", "📈 Charts", "🔍 Analysis", "📥 Reports"])

    # --- Data Tab ---
    with tab1:
        st.subheader("Data Preview")
        st.dataframe(df.head())

        st.subheader("Summary Statistics")
        if st.sidebar.button("Show Summary Statistics"):
            st.info("**Mean:**")
            st.write(df.mean(numeric_only=True))
            st.write("**Median:**")
            st.write(df.median(numeric_only=True))
            st.write("**Correlation Matrix:**")
            st.dataframe(df.corr(numeric_only=True))

    # --- Charts Tab ---
    with tab2:
        st.subheader("Visualization")
        selected_cols = st.sidebar.multiselect("Select columns for visualization", numeric_cols)
        chart_type = st.sidebar.selectbox("Choose chart type", ["Line Chart", "Histogram", "Box Plot", "Scatter Plot", "Pie Chart"])
        if st.sidebar.button("Generate Chart"):
            if selected_cols:
                if chart_type == "Line Chart":
                    st.line_chart(df[selected_cols])
                    fig, ax = plt.subplots()
                    df[selected_cols].plot(ax=ax)
                    fig.savefig("line.png")
                elif chart_type == "Histogram":
                    for col in selected_cols:
                        fig, ax = plt.subplots()
                        sns.histplot(df[col], kde=True, ax=ax)
                        st.pyplot(fig)
                        fig.savefig("histogram.png")
                elif chart_type == "Box Plot":
                    fig, ax = plt.subplots()
                    sns.boxplot(data=df[selected_cols], ax=ax)
                    st.pyplot(fig)
                    fig.savefig("boxplot.png")
                elif chart_type == "Scatter Plot":
                    if len(selected_cols) >= 2:
                        st.scatter_chart(df[selected_cols])
                        fig, ax = plt.subplots()
                        sns.scatterplot(x=df[selected_cols[0]], y=df[selected_cols[1]], ax=ax)
                        fig.savefig("scatter.png")
                    else:
                        st.warning("Select at least 2 columns for scatter plot.")
                elif chart_type == "Pie Chart":
                    col = st.sidebar.selectbox("Select column for Pie Chart", numeric_cols)
                    pie_data = df[col].value_counts()
                    st.write(pie_data)
                    fig, ax = plt.subplots()
                    pie_data.plot.pie(autopct="%1.1f%%", ax=ax)
                    st.pyplot(fig)
                    fig.savefig("pie.png")
    st.divider()

    # --- Analysis Tab ---
    # --- Time Series Analysis ---
    with tab3:
        st.subheader("Time Series Analysis (TSA)")
        if "Date" in df.columns:
            df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
            df = df.set_index("Date")
            tsa_col = st.sidebar.selectbox("Select numeric column for TSA", numeric_cols)
            if st.sidebar.button("Run TSA"):
                try:
                    result = seasonal_decompose(df[tsa_col].dropna(), period=12, model="additive")
                    st.line_chart(result.trend.dropna())
                    st.line_chart(result.seasonal.dropna())
                    st.line_chart(result.resid.dropna())
                    fig = result.plot()
                    fig.savefig("tsa.png")
                except Exception as e:
                    st.error(f"TSA failed: {e}")
        else:
            st.info("No 'Date' column found. TSA requires a datetime index.")
        
       # --- Seasonal ARIMAX Forecast ---
        st.subheader("Seasonal ARIMAX Forecast for Stock Market")

        # Ensure Date column is datetime index
        if "Date" in df.columns:
            df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
            df = df.set_index("Date")

        # Check if index is datetime
        if pd.api.types.is_datetime64_any_dtype(df.index):
            target_col = st.sidebar.selectbox("Select target column (e.g., Close price)", numeric_cols)
            forecast_years = st.sidebar.number_input("Years to forecast", min_value=1, max_value=10, value=2)

            if st.sidebar.button("Predict"):
                try:
                    from statsmodels.tsa.statespace.sarimax import SARIMAX

                    # Set frequency explicitly (adjust 'MS' for month start, 'D' for daily data)
                    df = df.asfreq('MS')

                    # Fit SARIMAX model
                    model = SARIMAX(df[target_col].dropna(), order=(1,1,1), seasonal_order=(1,1,1,12))
                    results = model.fit(disp=False)

                    # Forecast steps
                    steps = forecast_years * 12
                    forecast = results.get_forecast(steps=steps)
                    forecast_mean = forecast.predicted_mean

                    # Build forecast index starting AFTER last historical date
                    forecast_index = pd.date_range(start=df.index[-1] + pd.offsets.MonthBegin(),
                                                periods=steps, freq='MS')
                    forecast_series = pd.Series(forecast_mean.values, index=forecast_index)

                    # Combine historical + forecast
                    combined = pd.concat([df[target_col], forecast_series])

                    # Streamlit chart
                    st.line_chart(combined)

                    # Matplotlib chart
                    fig, ax = plt.subplots()
                    df[target_col].plot(ax=ax, label="Historical")
                    forecast_series.plot(ax=ax, label="Forecast", color="red")
                    ax.legend()
                    ax.set_title(f"Stock Market Forecast ({forecast_years} years)")
                    fig.savefig("stock_forecast.png")
                    st.pyplot(fig)

                    # Plain-language explanation
                    st.markdown("### Forecast Summary")
                    st.write(f"- The model projects {forecast_years} years into the future based on past trends.")
                    st.write("- The red line shows predicted values, connected to the historical series.")
                    st.write("- This forecast assumes seasonal patterns repeat and past relationships continue.")
                except Exception as e:
                    st.error(f"Forecasting failed: {e}")
        else:
            st.info("No datetime index found. Forecasting requires a datetime index.")


        # --- Simple Linear Regression ---
        st.subheader("Simple Linear Regression")
        x_col = st.sidebar.selectbox("Select X (feature)", numeric_cols)
        y_col = st.sidebar.selectbox("Select y (target)", numeric_cols)
        if st.sidebar.button("Run Regression"):
            if x_col and y_col and x_col != y_col:
                X = df[[x_col]].dropna()
                y = df[y_col].dropna()
                if len(X) == len(y):
                    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
                    model = LinearRegression()
                    model.fit(X_train, y_train)
                    y_pred = model.predict(X_test)

                    coef = model.coef_[0]
                    intercept = model.intercept_
                    r2 = r2_score(y_test, y_pred)
                    mse = mean_squared_error(y_test, y_pred)

                    # Technical results
                    st.write("**Coefficient:**", coef)
                    st.write("**Intercept:**", intercept)
                    st.write("**R² Score:**", r2)
                    st.write("**MSE:**", mse)

                    # Visualize actual vs predicted
                    reg_results = pd.DataFrame({"Actual": y_test, "Predicted": y_pred})
                    st.line_chart(reg_results)

                    fig, ax = plt.subplots()
                    ax.scatter(X_test, y_test, label="Actual")
                    ax.plot(X_test, y_pred, color="red", label="Predicted")
                    ax.set_xlabel(x_col)
                    ax.set_ylabel(y_col)
                    ax.legend()
                    fig.savefig("regression.png")
                    st.pyplot(fig)

                    # Plain-language explanation
                    st.markdown("### Explanation/Summary")
                    direction = "increases" if coef > 0 else "decreases"
                    st.write(f"- Every extra unit of **{x_col}** {direction} **{y_col}** by about **{coef:.2f} units**.")
                    st.write(f"- If {x_col} were zero, the baseline {y_col} would be about **{intercept:.2f}**.")
                    st.write(f"- The model explains about **{r2:.0%}** of what drives {y_col}.")
                    st.write(f"- The average prediction error is about **{mse:.2f} units**.")
                else:
                    st.warning("Drop NA values or align data for regression.")


        # --- Multiple Linear Regression ---
        st.subheader("Multiple Linear Regression")
        x_cols = st.sidebar.multiselect("Select multiple X features", numeric_cols)
        y_col_multi = st.sidebar.selectbox("Select target (y)", numeric_cols)
        if st.sidebar.button("Run Multiple Regression"):
            if x_cols and y_col_multi and y_col_multi not in x_cols:
                X = df[x_cols].dropna()
                y = df[y_col_multi].dropna()
                min_len = min(len(X), len(y))
                X = X.iloc[:min_len]
                y = y.iloc[:min_len]

                X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
                model = LinearRegression()
                model.fit(X_train, y_train)
                y_pred = model.predict(X_test)

                # Show coefficients
                coef_dict = dict(zip(x_cols, model.coef_))
                st.write("**Coefficients:**", coef_dict)
                st.write("**Intercept:**", model.intercept_)
                st.write("**R² Score:**", r2_score(y_test, y_pred))
                st.write("**MSE:**", mean_squared_error(y_test, y_pred))

                # Visualize predictor importance
                coef_df = pd.DataFrame.from_dict(coef_dict, orient='index', columns=['Coefficient'])
                st.bar_chart(coef_df)

                # Plain-language summary
                st.markdown("### Summary/Explanation")
                st.write(f"- The model explains about **{r2_score(y_test, y_pred):.0%}** of what drives {y_col_multi}.")
                st.write("- Bigger bars mean stronger influence. Positive bars mean 'more increases the outcome'; negative bars mean 'more decreases the outcome'.")
                for feature, coef in coef_dict.items():
                    direction = "increases" if coef > 0 else "decreases"
                    st.write(f"- Every extra unit of **{feature}** {direction} {y_col_multi} by about **{coef:.2f} units**.")

                # Plot actual vs predicted
                reg_results = pd.DataFrame({"Actual": y_test, "Predicted": y_pred})
                st.line_chart(reg_results)

                fig, ax = plt.subplots()
                ax.scatter(y_test, y_pred)
                ax.set_xlabel("Actual")
                ax.set_ylabel("Predicted")
                ax.set_title("Multiple Regression Results")
                fig.savefig("multi_regression.png")
                st.pyplot(fig)
            else:
                st.warning("Select at least one feature and a different target.")


    # --- Reports Tab ---
    with tab4:
        st.subheader("Download Reports")
        if st.sidebar.button("Download Excel"):
            df.to_excel("report.xlsx", index=False)
            with open("report.xlsx", "rb") as f:
                st.download_button("Download Excel File", f, file_name="report.xlsx")

        if st.sidebar.button("Download PDF"):
            from fpdf import FPDF
            pdf = FPDF()

            # Cover page
            pdf.add_page()
            pdf.set_font("Arial", 'B', 16)
            pdf.cell(200, 20, txt="Data Analysis Report", ln=True, align="C")
            pdf.set_font("Arial", size=12)
            pdf.cell(200, 10, txt=f"Dataset: {uploaded_file.name}", ln=True, align="C")
            pdf.cell(200, 10, txt=f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", ln=True, align="C")

            # Summary stats
            pdf.add_page()
            pdf.set_font("Arial", size=12)
            pdf.cell(200, 10, txt="Summary Statistics", ln=True, align="C")
            pdf.multi_cell(0, 10, df.describe().to_string())

            # Add charts if they exist
            for chart_file, title in [
                ("line.png", "Line Chart"),
                ("histogram.png", "Histogram"),
                ("boxplot.png", "Box Plot"),
                ("scatter.png", "Scatter Plot"),
                ("pie.png", "Pie Chart"),
                ("tsa.png", "Time Series Analysis"),
                ("regression.png", "Simple Regression Plot"),
                ("multi_regression.png", "Multiple Regression Plot"),
            ]:
                try:
                    pdf.add_page()
                    pdf.cell(200, 10, txt=title, ln=True, align="C")
                    pdf.image(chart_file, x=10, y=30, w=180)
                except Exception:
                    pass  # skip if chart not generated

            pdf.output("report.pdf")
            with open("report.pdf", "rb") as f:
                st.download_button("Download PDF File", f, file_name="report.pdf")
