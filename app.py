# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import dash
import dash_core_components as dcc
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
    # 날짜 선택
    dcc.DatePickerRange(
        id='date-picker-range',
        start_date=date(2020, 6, 15),
        end_date_placeholder_text=date(2020, 6, 30)
    ),
    dcc.Checklist(
        options=[
            {'label': '누적', 'value': 'cumu'}
        ],
        value=['MTL', 'SF']
    ),
    generate_table(df),
    dcc.Graph(
        figure=dict(
            data=[
                dict(
                    x=[1995, 1996, 1997, 1998, 1999, 2000, 2001, 2002, 2003,
                       2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012],
                    y=[219, 146, 112, 127, 124, 180, 236, 207, 236, 263,
                       350, 430, 474, 526, 488, 537, 500, 439],
                    name='Rest of world',
                    marker=dict(
                        color='rgb(55, 83, 109)'
                    )
                ),
                dict(
                    x=[1995, 1996, 1997, 1998, 1999, 2000, 2001, 2002, 2003,
                       2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012],
                    y=[16, 13, 10, 11, 28, 37, 43, 55, 56, 88, 105, 156, 270,
                       299, 340, 403, 549, 499],
                    name='China',
                    marker=dict(
                        color='rgb(26, 118, 255)'
                    )
                )
            ],
            layout=dict(
                title='US Export of Plastic Scrap',
                showlegend=True,
                legend=dict(
                    x=0,
                    y=1.0
                ),
                margin=dict(l=40, r=0, t=40, b=30)
            )
        ),
        style={'height': 300},
        id='my-graph'
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)