# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import dash
import dash_html_components as html
from kap_db_connect import *

# df = pd.read_csv('https://gist.githubusercontent.com/chriddyp/c78bf172206ce24f77d6363a2d754b59/raw/c353e8ef842413cae56ae3920b8fd78468aa4cb2/usa-agricultural-exports-2011.csv')
kapodbc = Kapodbc()
conn, cursor = kapodbc.connect()
sql = "select convert(varchar(10), StdDate, 120) Date, TBS = CAST(TBS*100 as decimal(7,5)), TBT = CAST(TBT*100 as decimal(7,5)), "
sql +=         "TBB = CAST(TBB*100 as decimal(7,5)) , Rsquare = CAST(Rsquare as decimal(4,2)) from BPRPA..H_TB_FACTOR_DECOMP "
sql += "where stddate between '20200615' and '20200630' and modelid = 'KAP030' order by 1"
df = pd.read_sql(sql, conn)


def generate_table(dataframe, max_rows=10):
    return html.Table([
        html.Thead(
            html.Tr([html.Th(col) for col in dataframe.columns])
        ),
        html.Tbody([
            html.Tr([
                html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
            ]) for i in range(min(len(dataframe), max_rows))
        ])
    ])


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(children=[
    html.H4(children='국채 요인 일간 변동치'),
    generate_table(df)
])

if __name__ == '__main__':
    app.run_server(debug=True)