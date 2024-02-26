# Desafio Técnico - Cientista de Dados Júnior

## Descrição

Esse repo contém a resolução do desafio em que foi realizado em duas etapas:
1. Análises as perguntas feitas em `perguntas_desafio.md` que estão organizadas em dois notebooks dentro da pasta `notebooks`.
2. Construção de um dashboard que funciona como um balanço diário dos chamados 1746 na cidade. Ele visa dá uma visão geral da quantidade dos chamados, onde estão localidades e os tipos de ocorrências mais solicitadas.

## Como o projeto está organizado

1. A pasta `src/data` contém os scripts com as querys para adquir os dados para resolução do desafio. 
2. A pasta `src/plot` contém o scripts para construção de gráficos com o dashboard.
3. O arquivo `config.toml` contém algumas variáveis de configuração do dashboard e nome do projeto na GCP.
4. O arquivo `dashboard_app.py` contém o script para rodar o dashboard e foi contruído utilizando a lib `streamlit`
5. A pasta `dataset` armazena os dados adquiridos com os scripts e a pasta `notebooks` contém as análises dos dados para a resolução do desafio.

### Conjunto de Dados

Os conjuntos de dados que serão utilizados neste desafio são:

- **Chamados do 1746:** Dados relacionados a chamados de serviços públicos na cidade do Rio de Janeiro. O caminho da tabela é : `datario.administracao_servicos_publicos.chamado_1746`
- **Bairros do Rio de Janeiro:** Dados sobre os bairros da cidade do Rio de Janeiro - RJ. O caminho da tabela é: `datario.dados_mestres.bairro`
- **Ocupação Hoteleira em Grandes Eventos no Rio**: Dados contendo o período de duração de alguns grandes eventos que ocorreram no Rio de Janeiro em 2022 e 2023 e a taxa de ocupação hoteleira da cidade nesses períodos. O caminho da tabela é: `datario.turismo_fluxo_visitantes.rede_hoteleira_ocupacao_eventos`

### Como rodar esse projeto?

1. A conda é utilzada para ser nosso package management, então, é necessário [instala-lá](https://github.com/TalissaMoura/emd-desafio-junior-data-scientist).
2. O arquivo `environment.yml` é que contém as depedências para rodar esse projeto. Execute o comando `conda create env -f environment.yml` para instalar as packages necessárias.
3. Lembre-se de configurar seu projeto na sua conta GCP. O tutorial para isso está [aqui](https://docs.dados.rio/tutoriais/como-acessar-dados/).
4. Para executar o dashboard execute o comando `streamlit run dashboard_app.py`.
5. Em uma primeira execução, para adquir os dados é necessário se autenticar seu acesso. Basta realizar o login no Pydata com sua conta do google.

