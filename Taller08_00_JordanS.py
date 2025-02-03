{
  "nbformat": 4,
  "nbformat_minor": 0,
  "metadata": {
    "colab": {
      "provenance": [],
      "authorship_tag": "ABX9TyOTXOUvilWQtWecbm8NKlhp",
      "include_colab_link": true
    },
    "kernelspec": {
      "name": "python3",
      "display_name": "Python 3"
    },
    "language_info": {
      "name": "python"
    }
  },
  "cells": [
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "view-in-github",
        "colab_type": "text"
      },
      "source": [
        "<a href=\"https://colab.research.google.com/github/Jordan-677/Jordan-677-App_con_ChatGPT/blob/main/Taller08_00_JordanS.py\" target=\"_parent\"><img src=\"https://colab.research.google.com/assets/colab-badge.svg\" alt=\"Open In Colab\"/></a>"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": null,
      "metadata": {
        "id": "sRjZzmWPP6sV"
      },
      "outputs": [],
      "source": [
        "import streamlit as st\n",
        "import pandas as pd\n",
        "import matplotlib.pyplot as plt\n",
        "import geopandas as gpd\n",
        "import scipy.cluster.hierarchy as sch\n",
        "\n",
        "def cargar_datos():\n",
        "    \"\"\"Carga datos desde archivo, URL o archivo de prueba.\"\"\"\n",
        "    opciones = {\n",
        "        \"Subir archivo\": None,\n",
        "        \"Desde URL\": None,\n",
        "        \"Archivo de prueba\": \"https://raw.githubusercontent.com/\"\n",
        "                           \"gabrielawad/programacion-para-ingenieria/\"\n",
        "                           \"refs/heads/main/archivos-datos/aplicaciones/\"\n",
        "                           \"deforestacion.csv\"\n",
        "    }\n",
        "\n",
        "    opcion = st.radio(\n",
        "        \"Selecciona la fuente de datos:\", list(opciones.keys())\n",
        "    )\n",
        "\n",
        "    archivo = st.file_uploader(\"Sube un archivo CSV\", type=[\"csv\"])\n",
        "    url = st.text_input(\"Ingresa la URL del archivo CSV\")\n",
        "\n",
        "    fuente = {\n",
        "        \"Subir archivo\": archivo,\n",
        "        \"Desde URL\": url,\n",
        "        \"Archivo de prueba\": opciones[\"Archivo de prueba\"]\n",
        "    }\n",
        "    return pd.read_csv(fuente[opcion])\n",
        "\n",
        "def limpiar_datos(df):\n",
        "    \"\"\"Rellena valores faltantes mediante interpolación.\"\"\"\n",
        "    return df.interpolate()\n",
        "\n",
        "def graficar_torta(df):\n",
        "    \"\"\"Genera gráfico de torta según tipo de vegetación.\"\"\"\n",
        "    conteo = df[\"Tipo_Vegetacion\"].value_counts()\n",
        "    fig, ax = plt.subplots()\n",
        "    ax.pie(\n",
        "        conteo,\n",
        "        labels=conteo.index,\n",
        "        autopct='%1.1f%%',\n",
        "        startangle=90\n",
        "    )\n",
        "    ax.axis(\"equal\")\n",
        "    st.pyplot(fig)\n",
        "\n",
        "def mostrar_mapa(df, variable):\n",
        "    \"\"\"Muestra mapa de deforestación según variable.\"\"\"\n",
        "    gdf = gpd.GeoDataFrame(\n",
        "        df, geometry=gpd.points_from_xy(df.Longitud, df.Latitud)\n",
        "    )\n",
        "    fig, ax = plt.subplots()\n",
        "    gdf.plot(column=variable, legend=True, cmap='OrRd', ax=ax)\n",
        "    st.pyplot(fig)\n",
        "\n",
        "def analisis_cluster(df):\n",
        "    \"\"\"Realiza análisis de clúster de superficies deforestadas.\"\"\"\n",
        "    matriz_distancia = sch.linkage(\n",
        "        df[[\"Superficie_Deforestada\"]], method='ward'\n",
        "    )\n",
        "    fig, ax = plt.subplots()\n",
        "    sch.dendrogram(matriz_distancia, ax=ax)\n",
        "    st.pyplot(fig)\n",
        "\n",
        "def main():\n",
        "    st.title(\"Análisis de la Deforestación\")\n",
        "    df = limpiar_datos(cargar_datos())\n",
        "    st.write(\"Vista previa de los datos:\")\n",
        "    st.write(df.head())\n",
        "\n",
        "    st.subheader(\"Gráfico de torta según tipo de vegetación\")\n",
        "    graficar_torta(df)\n",
        "\n",
        "    variable = st.selectbox(\n",
        "        \"Selecciona una variable para el mapa\", df.columns[3:]\n",
        "    )\n",
        "    st.subheader(f\"Mapa de deforestación según {variable}\")\n",
        "    mostrar_mapa(df, variable)\n",
        "\n",
        "    st.subheader(\"Análisis de Clúster\")\n",
        "    analisis_cluster(df)\n",
        "\n",
        "if __name__ == \"__main__\":\n",
        "    main()"
      ]
    }
  ]
}