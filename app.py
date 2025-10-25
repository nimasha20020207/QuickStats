from flask import Flask,render_template,request
import pandas as pd
import matplotlib.pyplot as plt
import os
import seaborn as sns

##creating the flask app
app=Flask(__name__)
app.config['UPLOAD_FOLDER']='uploads'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/test')
def test():
    return "Flask is working!"


@app.route('/upload', methods=['POST'])
def upload_file():

    ##checking whether a fie is uploaded
    if 'file' not in request.files:
        return "No file uploaded",400
    file=request.files['file']
    if file.filename=='':
        return "No file selected",400
    
    ##saving the file to uploads folder
    filepath=os.path.join(app.config['UPLOAD_FOLDER'],file.filename)
    file.save(filepath)

    #detecting filtype
    file_ext=os.path.splitext(file.filename)[1].lower()

    ##reading data using pandas
    #df=pd.read_csv(filepath)

    try:
        if file_ext=='.csv':
            try:
                df = pd.read_csv(filepath, encoding='utf-8')
            except UnicodeDecodeError:
                df = pd.read_csv(filepath, encoding='latin1')

        elif file_ext in ['.xls','.xlsx']:
            df = pd.read_excel(filepath)
            
        else:
            return "unsupported file format. Please upload CSV or Excel files.",400
    except Exception as e:
        return f"Error reading fie: {e}",500

    #filtering and excluding ID like and Key like columns
    df_filtered=df.copy()
    exclude_keywords=['id', 'key', 'code', 'number']
    numeric_cols=[
        col for col in df.select_dtypes(include='number').columns
        if not any(keyword in col.lower() for keyword in exclude_keywords)
    ]

    #falling back to all numeric columns ifall numeric columns are excluded
    if not numeric_cols:
        numeric_cols=df.select_dtypes(include='number').columns

    #creating summary and preview
    preview=df.head().to_html(classes='table table-bordered')
    stats=df[numeric_cols].describe().to_html(classes='table table-bordered')

    #drawing a simple chart
    # --- Draw modern histogram for the first numeric column ---
    if len(numeric_cols) > 0:
        col = numeric_cols[0]  # Pick first numeric column

        plt.figure(figsize=(8, 5))
        sns.set_style("whitegrid")  # clean modern background
        sns.histplot(df[col], bins=15, kde=True, color="#007bff")  # histogram + KDE line

        plt.title(f"Distribution of {col}", fontsize=16, weight='bold')
        plt.xlabel(col, fontsize=12)
        plt.ylabel("Frequency", fontsize=12)
        plt.xticks(fontsize=10)
        plt.yticks(fontsize=10)

        plt.tight_layout()  # avoids overlapping labels

        chart_path = os.path.join(app.root_path, 'static', 'chart.png')
        plt.savefig(chart_path)
        plt.close()

    cat_cols = df.select_dtypes(include='object').columns
    if len(cat_cols) > 0:
        top_cat = cat_cols[0]
        top_values = df[top_cat].value_counts().head(5)
        plt.figure(figsize=(6,4))
        sns.barplot(x=top_values.index, y=top_values.values, palette="Set2")
        plt.title(f"Top 5 Categories in {top_cat}")
        plt.ylabel("Count")
        plt.xticks(rotation=30)
        plt.tight_layout()
        plt.savefig(os.path.join(app.root_path, 'static/chart_cat.png'))
        plt.close()



    return render_template('display.html',preview=preview, stats=stats, chart_path=chart_path)

if __name__=='__main__':
    app.run(debug=True)