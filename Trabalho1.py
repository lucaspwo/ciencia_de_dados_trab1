import pandas as pd
import streamlit as st
import pydeck as pdk
import altair as alt

ano_18 = pd.read_csv('ano_18.csv')
ano_19 = pd.read_csv('ano_19.csv')
ano_20 = pd.read_csv('ano_20.csv')

list18 = pd.read_csv('Rio_2018-04-14/listings.csv')
list19 = pd.read_csv('Rio_2019-02-11/listings.csv')
list20 = pd.read_csv('Rio_2020-02-25/listings.csv')
list21 = pd.read_csv('Rio_2021-02-22/listings.csv')

listas = [['abr/2018', list18['reviews_per_month'].mean()],
          ['fev/2019', list19['reviews_per_month'].mean()],
          ['fev/2020', list20['reviews_per_month'].mean()],
          ['fev/2021', list21['reviews_per_month'].mean()]
]

grafico = pd.DataFrame(listas, columns=['periodo', 'media_analises_por_mes'])

st.set_page_config(layout="wide")
col1, col2 = st.beta_columns(2)

col1.title('Impacto da COVID no Airbnb no Rio de Janeiro')

hide_menu_style = """
        <style>
        #MainMenu {visibility: hidden;}
        </style>
        """
st.markdown(hide_menu_style, unsafe_allow_html=True)

ano = col1.slider('Selecione um ano:', 2018, 2020)

qtd = 0
soma = 0
disp_0 = 0

if ano == 2018:
    qtd = len(ano_18)
    dados = ano_18
    soma = ano_18['reviews'].sum()
    disp_0 = (ano_18['availability_365'] == 0).sum()
if ano == 2019:
    qtd = len(ano_19)
    dados = ano_19
    soma = ano_19['reviews'].sum()
    disp_0 = (ano_19['availability_365'] == 0).sum()
if ano == 2020:
    qtd = len(ano_20)
    dados = ano_20
    soma = ano_20['reviews'].sum()
    disp_0 = (ano_20['availability_365'] == 0).sum()

Locais = pdk.Layer(
    'ColumnLayer',
    data=dados,
    get_position=['longitude', 'latitude'],
    get_elevation='reviews',
    auto_highlight=True,
    radius=20,
    pickable=True,
    get_fill_color=(32, 34, 241, 140),
    elevation_scale=10,
    elevation_range=[0,50],
)

tooltip = {
    "html": "ID: <b>{id}</b> </br> Análises no ano: <b>{reviews}</b> </br> Última análise: <b>{last_review}</b> </br> Disponibilidade: <b>{availability_365}</b> dias",
    "style": {"background": "grey", "color": "white", "font-family": '"Helvetica Neue", Arial', "z-index": "10000"},
}

col1.pydeck_chart(pdk.Deck(map_style="mapbox://styles/mapbox/light-v9",  tooltip=tooltip, initial_view_state={'latitude': -22.955785, 'longitude': -43.202340, 'zoom': 11, 'pitch': 35}, layers=[Locais]))

for i in range(8): col2.text('')
col2.text('Quantidade de anúncios: ' + str(qtd))
col2.text('Total de análises: ' + str(soma))
col2.text('Análises/anúncios: ' + str(round(soma/qtd, 2)))
col2.text('Locais indisponíveis: ' + str(disp_0))
col2.text('Porcentagem de locais indisponíveis: ' + str(round(disp_0*100/qtd, 2)) + '%')

for i in range(2): col2.text('')

col2.subheader('Análises no ano por localização:')

c = alt.Chart(dados).mark_circle().encode(
    alt.X('longitude', scale = alt.Scale(domain=(-43.65, -43.05))),
    alt.Y('latitude', scale = alt.Scale(domain=(-23.05, -22.85))),
    size = 'reviews',
    # color = 'reviews',
    tooltip=['id', 'reviews', 'availability_365']
).interactive()

col2.altair_chart(c, use_container_width=True)

st.subheader('Média de análises por mês (cumulativo):')

st.altair_chart(alt.Chart(grafico).mark_bar().encode(
    x=alt.X('periodo'),
    y=alt.Y('media_analises_por_mes'),
    tooltip=['periodo', 'media_analises_por_mes']
).configure_mark(
    opacity=0.6,
    color='blue'
), use_container_width=True)