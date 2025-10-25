# Simple Data Insights App

A lightweight Flask web application that allows users to upload CSV or Excel files and automatically generate **data previews, summary statistics, and modern visual insights**.

---

## 🔹 Features

- Upload **CSV** or **Excel** files.
- Display **data preview** (first few rows).
- Compute **summary statistics** for numeric columns, ignoring ID/Key-like columns.
- Generate **modern histograms** for numeric columns.
- Clean, modern UI with responsive design.

## 🔹 Installation
-1.clone repository
-2. Create virtualenvironment
-3. Install Python libraries
-4. Run the Flask application

## 🔹 Project structure
MyFlaskApp/
├─ app.py                 # Flask app main file
├─ templates/
│   ├─ index.html         # Upload page
│   └─ display.html       # Results page
├─ static/
│   ├─ style.css          # CSS styling
│   └─ chart.png          # Example chart 
├─ uploads/               # Uploaded files 
├─ README.md
