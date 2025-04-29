from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)

@app.route('/', methods=['GET'])
def show_booked_alumni():
    df = pd.read_csv('bookings.csv')
    df = df[df['status'] == 'Confirmed']

    search_query = request.args.get('search', '').lower()
    event_filter = request.args.get('event_id', '')

    # Filter by alumni name
    if search_query:
        df = df[df['alumni_id'].str.lower().str.contains(search_query)]

    # Filter by event ID
    if event_filter:
        df = df[df['event_id'].astype(str) == event_filter]

    event_ids = sorted(df['event_id'].unique())
    return render_template('index.html', alumni=df.to_dict(orient='records'), search=search_query, event_filter=event_filter, event_ids=event_ids)

if __name__ == '__main__':
    app.run(debug=True)
