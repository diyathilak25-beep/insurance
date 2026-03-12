# Insurance Bias Dashboard

A Streamlit-based tool to detect and visualize bias in health insurance datasets.

## Setup Locally
1. Clone the repo: `git clone <url>`
2. Install requirements: `pip install -r requirements.txt`
3. Run the app: `streamlit run app.py`

## Deploying to Streamlit Cloud
1. Push your code to a public GitHub repository.
2. Go to [share.streamlit.io](https://share.streamlit.io).
3. Connect your GitHub account and select your repository.
4. Click "Deploy".

## Bias Metrics Used
- **DIR (Disparate Impact Ratio):** Measures the ratio of average outcomes between groups. Values < 0.8 or > 1.25 suggest bias.
- **T-Test:** Determines if the difference in means between two groups is statistically significant (p < 0.05).
