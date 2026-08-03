# 📊 DataMind AI

**An Intelligent AI-Powered Data Analysis Platform built with Python and Streamlit**

DataMind AI is an end-to-end data analysis platform that helps users validate, clean, analyze, and visualize datasets with minimal manual effort. The application automates common data preprocessing tasks and generates AI-inspired recommendations, making it useful for students, data analysts, and machine learning beginners.

---

# 🚀 Features

### 📁 Dataset Validation

* CSV file validation
* Automatic encoding detection
* Delimiter detection
* File size validation
* Dataset integrity checks

### 📈 Dataset Profiling

* Number of rows and columns
* Missing value statistics
* Duplicate row detection
* Numerical and categorical column identification
* Memory usage analysis
* Potential identifier column detection

### 🧹 Intelligent Data Cleaning

* Missing value analysis
* AI-based cleaning recommendations
* Mean / Median / Mode imputation
* Forward Fill & Backward Fill
* Drop Rows
* Drop Columns
* Duplicate removal

### 📊 Automated Data Visualization

* Histograms
* Bar Charts
* Box Plots
* Correlation Heatmaps

### ❤️ Dataset Health Score

Automatic quality assessment based on:

* Missing values
* Duplicate rows
* Outlier impact
* Dataset completeness

### 🧠 AI Consultant Summary

Automatically generates business-friendly insights such as:

* Critical missing value warnings
* Identifier detection
* Correlation insights
* Data quality observations
* Suggested next steps

### 📄 Report Generation

* Download cleaned dataset
* Export PDF report

---

# 🛠️ Tech Stack

* Python
* Streamlit
* Pandas
* NumPy
* Matplotlib
* FPDF

---

# 📂 Project Structure

```text
app/
│
├── main.py
│
├── services/
│   ├── validation_service.py
│   ├── profile_service.py
│   ├── cleaning_service.py
│   ├── missing_value_service.py
│   ├── duplicate_service.py
│   ├── visualization_service.py
│   ├── health_score_service.py
│   ├── consultant_service.py
│   └── pdf_service.py
│
└── assets/
```

---

# ⚡ Installation

```bash
git clone https://github.com/anchitprojectsml/Datamind-AI.git
```

```bash
cd Datamind-AI
```

```bash
pip install -r requirements.txt
```

```bash
streamlit run app/main.py
```

---

# 🎯 Current Capabilities

✔ Validate uploaded datasets

✔ Generate dataset profile

✔ Detect missing values

✔ Handle missing values interactively

✔ Remove duplicate records

✔ Generate automatic visualizations

✔ Calculate dataset health score

✔ Produce AI consultant summaries

✔ Export cleaned datasets

✔ Generate PDF reports

---

# 🗺️ Roadmap

## ✅ Version 1.0

* Dataset validation
* Data profiling
* Cleaning engine
* Visualizations
* Health score
* AI consultant summary
* PDF export
* Download cleaned dataset

## 🚀 Version 2 (Planned)

* Automatic ML task detection
* Regression models
* Classification models
* Clustering
* Feature importance
* Model evaluation
* Prediction interface
* Download trained models

---

# 👨‍💻 Author

**Anchit**

Passionate about Artificial Intelligence, Data Science, and Machine Learning.

---

# ⭐ Support

If you find this project useful, consider giving it a ⭐ on GitHub.

