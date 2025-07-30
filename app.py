from flask import Flask, render_template, request
import csv

app = Flask(__name__)

def load_pests():
    pest_data = {}
    with open('data/pests.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            crop = row['Crop']
            pest = row['Pest']
            advisory = row['Advisory']
            if crop not in pest_data:
                pest_data[crop] = {}
            pest_data[crop][pest] = advisory
    return pest_data

pests = load_pests()

@app.route('/')
def index():
    return render_template('index.html', pests=pests)

@app.route('/result', methods=['POST'])
def result():
    crop = request.form['crop']
    pest = request.form['pest']
    advisory = pests.get(crop, {}).get(pest, "No advisory found.")
    return render_template('result.html', crop=crop, pest=pest, advisory=advisory)

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)



