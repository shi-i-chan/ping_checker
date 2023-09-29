import pandas as pd
import plotly.graph_objects as go

from typing import NoReturn


def get_data(fn: str) -> pd.DataFrame:
    df = pd.read_csv(fn, index_col=0)
    df = df.fillna(0)
    df = df.astype({key: 'float32' for key in df.columns if key != 'date'})
    return df


def plot(fn: str) -> NoReturn:
    df = get_data(fn)
    labels = [column for column in df.columns if column != 'date']

    fig = go.Figure()
    for label in labels:
        fig.add_trace(go.Scatter(x=df['date'],
                                 y=df[label].values,
                                 name=label))

    fig.update_layout(
        height=1080,
        width=1920,
    )
    fig.update_xaxes(title_text='Date')
    fig.update_yaxes(title_text='Latency')
    fig.write_image('latency.png')
