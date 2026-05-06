# Dólar Hoy 💵

Dashboard interactivo que muestra el valor actual del dólar Blue y Oficial en Argentina, junto con un gráfico histórico de su evolución. Los datos se obtienen en tiempo real desde la API de Bluelytics.

## Deploy en vivo

https://dolar-hoy-kejkdeayzv9cfbfxuetqnd.streamlit.app

## ¿Qué muestra?

- Valor actual de compra y venta del dólar Blue y Oficial
- Brecha porcentual entre ambos
- Gráfico interactivo con la evolución histórica (hasta 2 años)
- Tabla con todos los datos históricos

## Librerias

- Python
- Streamlit
- Requests
- Pandas
- Plotly

## Demo en vivo



## Cómo usarlo

1. Clonar el repo:
```
git clone https://github.com/galo9-dev/dolar-hoy.git
```

2. Instalar dependencias:
```
pip install streamlit requests pandas plotly
```

3. Ejecutar:
```
streamlit run dolar_app.py
```

## API

Los datos provienen de [Bluelytics](https://bluelytics.com.ar), una API gratuita con valores actualizados del dólar argentino.