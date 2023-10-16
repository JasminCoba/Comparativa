import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# Load data for each year
df_2021 = pd.read_excel('2021.xlsx')
df_2022 = pd.read_excel('Cantidad de compras por producto 2022.xlsx')
df_2023 = pd.read_excel('Cantidad de compras por producto 2023-1.xlsx')

# Helper function to process the data for plotting
def process_data(df, top_n=5):
    # Select the columns related to months
    month_columns = df.columns[1:13]
    df['Total'] = df[month_columns].sum(axis=1)
    df = df[['Material', 'Total'] + list(month_columns)]
    df = df.iloc[1:-1]
    df = df.sort_values(by='Total', ascending=False)
    top_products = df.head(top_n)
    return df, top_products

# Process data for each year and get the top products
productos_2021, top_products_2021 = process_data(df_2021, top_n=10)
productos_2022, top_products_2022 = process_data(df_2022, top_n=10)
productos_2023, top_products_2023 = process_data(df_2023, top_n=10)

# Create interactive bar plots using Plotly for top 10 products
fig_2021 = px.bar(top_products_2021, x='Total', y='Material', orientation='h', title='10 Productos Top en 2021', labels={'Material': 'Productos', 'Total': 'Ventas'})
fig_2022 = px.bar(top_products_2022, x='Total', y='Material', orientation='h', title='10 Productos Top en2022', labels={'Material': 'Productos', 'Total': 'Ventas'})
fig_2023 = px.bar(top_products_2023, x='Total', y='Material', orientation='h', title='10 Productos Top en 2023', labels={'Material': 'Productos', 'Total': 'Ventas'})

# Create a comparison bar chart using Plotly for top 10 products
fig_comparison = go.Figure(data=[
    go.Bar(name='2021', x=top_products_2021['Material'], y=top_products_2021['Total'], marker_color='blue'),
    go.Bar(name='2022', x=top_products_2022['Material'], y=top_products_2022['Total'], marker_color='green'),
    go.Bar(name='2023', x=top_products_2023['Material'], y=top_products_2023['Total'], marker_color='red')
])

fig_comparison.update_layout(barmode='group', title='Comparison of Top 10 Products (2021-2023)')

# Create line plots for monthly sales for top products
def create_monthly_sales_plot(df, title):
    months = df.columns[2:14]
    fig = go.Figure()
    for index, row in df.iterrows():
        fig.add_trace(go.Scatter(x=months, y=row[2:14], mode='lines+markers', name=row['Material']))
    fig.update_layout(title=title, xaxis_title='Meses', yaxis_title='Ventas')
    return fig

# Create line plots for each year
fig_monthly_2021 = create_monthly_sales_plot(top_products_2021, 'Mas vendido en 2021')
fig_monthly_2022 = create_monthly_sales_plot(top_products_2022, 'Mas vendido en 2022')
fig_monthly_2023 = create_monthly_sales_plot(top_products_2023, 'Mas vendido en 2023')

total_sales = pd.DataFrame({
    'Year': ['2021', '2022', '2023'],
    'Total Sales': [productos_2021['Total'].sum(), productos_2022['Total'].sum(), productos_2023['Total'].sum()]
})

fig_total_sales = px.line(total_sales, x='Year', y='Total Sales', title='Total Sales Over the Years', labels={'Año': 'Year', 'Total de Ventas': 'Total Sales'})

# Now, you can create an interactive dashboard using Dash to display these plots.
import dash
from dash import dcc,html

app = dash.Dash(__name__)
server = app.server
app.layout = html.Div([
    html.H1("CRISP-DM BD COMPRAS"),
    
    dcc.Tabs([
        dcc.Tab(label='2021', children=[
            dcc.Graph(figure=fig_2021),
            dcc.Graph(figure=fig_monthly_2021)
        ]),
        dcc.Tab(label='2022', children=[
            dcc.Graph(figure=fig_2022),
            dcc.Graph(figure=fig_monthly_2022)
        ]),
        dcc.Tab(label='2023', children=[
            dcc.Graph(figure=fig_2023),
            dcc.Graph(figure=fig_monthly_2023)
        ]),
        dcc.Tab(label='Comparacion', children=[
            dcc.Graph(figure=fig_comparison),
            dcc.Graph(figure=fig_total_sales)
        ]),
    ])
])

if __name__ == '__main__':
    app.run_server(debug=True)
