# SMART CITY — TRAFFIC & MOBILITY

Dashboard profissional em Streamlit para análise de tráfego urbano, mobilidade e congestionamento a partir da base real `smart_city_traffic_mobility.csv`.

A aplicação foi construída para apresentação acadêmica em tecnologia e ciência de dados, com visual premium em tema escuro, filtros globais, KPIs executivos, gráficos interativos, exploração dos dados e diagnóstico de qualidade.

## Objetivo

Transformar registros horários de mobilidade urbana em uma plataforma de Business Intelligence para apoiar leitura operacional de uma cidade inteligente:

- monitoramento de volume de veículos;
- análise de velocidade média, filas, tempo de espera e congestionamento;
- identificação de zonas e interseções críticas;
- comparação por hora, dia da semana, período de pico, clima, tipo de via e condição da via;
- inspeção da qualidade e estrutura do dataset.

Todas as métricas, gráficos e insights são calculados a partir das colunas existentes no CSV. O dashboard não cria dados fictícios nem inventa relações causais.

## Estrutura do projeto

```text
SMART_CITY_TRAFFIC_MOBILITY/
├── app.py
├── requirements.txt
├── README.md
├── smart_city_traffic_mobility.csv
├── read.ipynb
├── data/
│   └── smart_city_traffic_mobility.csv
└── src/
    ├── __init__.py
    ├── analytics.py
    ├── charts.py
    ├── config.py
    ├── data_cleaning.py
    ├── data_loader.py
    └── insights.py
```

## Tecnologias

- Python
- Streamlit
- Pandas
- NumPy
- Plotly 7+

## Instalação

No terminal, entre na pasta do projeto:

```bash
cd C:\Users\henri\Downloads\SMART_CITY_TRAFFIC_MOBILITY
```

Crie e ative um ambiente virtual, se desejar:

```bash
python -m venv .venv
.venv\Scripts\activate
```

Instale as dependências:

```bash
pip install -r requirements.txt
```

## Execução

Execute o dashboard com:

```bash
streamlit run app.py
```

O Streamlit abrirá a aplicação no navegador. Se isso não ocorrer automaticamente, copie a URL exibida no terminal.

## Páginas do dashboard

### 1. Overview / Visão Geral

Visão executiva com:

- KPIs de veículos observados, velocidade média, congestionamento médio, registros severos, filas e espera;
- evolução diária do volume médio;
- distribuição dos níveis de congestionamento;
- ranking de zonas e tipos de via;
- cards de insights calculados a partir do recorte filtrado.

### 2. Traffic Analytics

Análise operacional do tráfego com:

- evolução temporal de volume, congestionamento e filas;
- volume médio por hora;
- heatmap hora × dia da semana;
- boxplots por período e tipo de via;
- comparação entre `rush_hour` e demais horários.

### 3. Mobility Insights

Página de inteligência urbana com:

- principais observações automáticas do recorte atual;
- ranking de interseções por índice de criticidade;
- mapa das interseções monitoradas quando latitude/longitude estão disponíveis;
- composição observada de veículos;
- matriz de correlação entre variáveis numéricas, com aviso de que correlação não implica causalidade;
- detecção de outliers por IQR.

### 4. Data Explorer

Exploração dos registros filtrados com:

- busca textual em IDs e categorias;
- seleção de colunas exibidas;
- tabela interativa;
- download dos dados filtrados em CSV;
- resumo textual do recorte selecionado.

### 5. Data Quality

Diagnóstico de qualidade dos dados com:

- total de linhas e colunas;
- valores ausentes;
- duplicatas;
- validação do esquema esperado;
- checagens de faixas e flags binárias;
- gráfico de nulos por coluna;
- dicionário de dados;
- cardinalidade e tipos.

## Filtros globais

A sidebar controla toda a aplicação. Todos os KPIs e gráficos respeitam os filtros selecionados.

Filtros disponíveis conforme as colunas do CSV:

- intervalo de datas;
- `city_zone`;
- `road_type`;
- `congestion_level`;
- `peak_period`;
- `weather_condition`;
- `road_condition`;
- `iot_sensor_health`;
- ranges numéricos para `vehicle_count`, `average_speed` e `congestion_score`.

O botão **Limpar filtros** restaura o estado inicial.

## Metodologia de tratamento

O arquivo original é preservado. As transformações são feitas em memória:

- conversão de `timestamp` para datetime;
- criação de `date`, `month`, `week`, `day_name` e `day_name_pt`;
- conversão de categorias e flags binárias;
- criação de métricas derivadas transparentes, como participação de veículos pesados, transporte público, motocicletas, razão de tempo verde, emissão por veículo e desperdício de combustível por veículo;
- validações de qualidade e consistência.

## Variáveis principais da base

A base contém variáveis de localização, tempo, tráfego, composição veicular, clima, infraestrutura e incidentes. Entre as colunas principais:

- `record_id`: identificador único do registro;
- `city_zone`: zona urbana monitorada;
- `road_id`: identificador da via;
- `intersection_id`: identificador da interseção;
- `latitude`, `longitude`: coordenadas do ponto monitorado;
- `road_type`: tipo de via;
- `vehicle_count`: contagem de veículos;
- `average_speed`: velocidade média;
- `traffic_density`: densidade de tráfego;
- `queue_length`: comprimento de fila;
- `average_wait_time`: tempo médio de espera;
- `timestamp`, `hour`, `day_of_week`: variáveis temporais;
- `rush_hour`, `peak_period`: indicação de pico/período;
- `weather_condition`, `rainfall_mm`, `visibility_km`: contexto climático;
- `construction_activity`, `public_event`, `accident_reported`: eventos e condições operacionais;
- `signal_cycle_seconds`, `green_light_duration`: semáforos;
- `congestion_score`, `congestion_level`: congestionamento;
- `emission_estimate`, `fuel_waste_estimate`: impactos ambientais/operacionais estimados.

O dicionário completo está disponível na página **Data Quality**.

## Limitações dos dados

- O dashboard descreve padrões observados; não estima causalidade.
- Correlações indicam associação linear, não explicação causal.
- `traffic_flow_rate` foi identificado como equivalente a `vehicle_count` nos dados inspecionados, portanto o dashboard prioriza `vehicle_count` para evitar duplicidade interpretativa.
- Algumas variáveis, como filas, espera, emissões e desperdício de combustível, podem apresentar distribuições assimétricas; por isso são analisadas com rankings, boxplots e outliers.
- A aplicação depende da presença do CSV real em `data/` ou na raiz do projeto.

## Deploy

Para publicar em Streamlit Community Cloud ou ambiente similar:

1. Suba o projeto para um repositório Git.
2. Garanta que `requirements.txt`, `app.py` e a pasta `src/` estejam no repositório.
3. Inclua o CSV em `data/smart_city_traffic_mobility.csv` se o ambiente permitir armazenar a base no repositório.
4. Configure o arquivo principal como `app.py`.
5. Faça o deploy.

## Melhorias futuras

- Modelos de previsão temporal usando a estrutura horária do dataset.
- Análise espacial mais avançada por clusters de interseções.
- Alertas operacionais automáticos por limiar de congestionamento.
- Simulação de ajustes semafóricos.
- Integração com dados reais de sensores em tempo quase real.
