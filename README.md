# Competitor Hiring Intelligence Dashboard

 A strategic analytics dashboard that uncovers hiring trends, regional expansion, and role priorities across five global HR tech competitors. This dashboard helps sales, product, and strategy teams make better decisions by interpreting hiring data as business signals.

> **Live Demo**: [Streamlit App (technical refernce)](https://competitor-hiring-analysis-nvidydztarwnskysxtaur3.streamlit.app/)
> **Live Demo**: [Updated Streamlit App](https://competitor-hiring-analysis-g3jgwogwvzekieccsvnsk8.streamlit.app/#multiplier)
> Worldpay Dashboard: [Worldpay](https://competitor-hiring-analysis-ciiprgkgzpbgkhcscxvjas.streamlit.app/)

---

## Tech Stack

- **Python** + **Pandas** – data wrangling
- **Streamlit** – interactive dashboard
- **Plotly** – visualizations (bar charts, heatmaps)
- **Scikit-learn** – clustering and predictive modeling
- **TF-IDF** – keyword extraction via NLP

---

##  Files

| File | Purpose |
|------|---------|
| `app.py` | Main dashboard logic |
| `data/clustered_jobs.csv` | Cleaned and tagged job data |
| `data/keyword_summary.csv` | TF-IDF keyword scores by company |
| `competitor_hiring_analysis.ipynb` | Exploratory data analysis notebook (temporal, NLP, modeling) |

---

## How to Run Locally

1. **Clone this repo**:
```bash
git clone https://github.com/AtharvaBadhe/competitor-hiring-analysis.git
cd competitor-hiring-analysis

```
2. **Create a virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # or .\venv\Scripts\activate on Windows

```
3. **Install dependencies:**
```bash
pip install -r requirements.txt

```
4. **Run Streamlit app**
```bash
streamlit run streamlit_app.py

```
## Author

**Atharva Badhe**  
Final Year B.E. – AI & DS  
Mumbai University | July 2025  

Feel free to connect or reach out on [LinkedIn](https://www.linkedin.com/in/atharva-badhe/)  



