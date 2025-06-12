# AeroGuard - Monitor de Tráfego Aéreo

AeroGuard é uma aplicação de desktop para visualização de tráfego aéreo em tempo real. Utilizando dados da API OpenSky Network, a ferramenta plota a posição das aeronaves em uma área geográfica específica sobre um mapa interativo, atualizando suas posições periodicamente.

A aplicação é construída com uma arquitetura cliente-servidor local:
* **Backend:** Um servidor Flask (Python) responsável por se autenticar na API da OpenSky, buscar os dados das aeronaves e fornecê-los através de um endpoint local.
* **Frontend:** Uma interface de mapa construída com HTML, CSS e Leaflet.js.
* **Container Desktop:** Uma janela de aplicação PyQt5 (Python) que encapsula e exibe o frontend, proporcionando uma experiência de aplicativo nativo.

---

### Funcionalidades

* **Visualização em Tempo Real:** Acompanhe a movimentação de aeronaves em um mapa interativo.
* **Dados Detalhados:** Ao clicar em uma aeronave, veja informações como o código de chamada (callsign) e o ICAO24.
* **Rotação dos Ícones:** Os ícones das aeronaves giram para indicar a direção do voo (proa).
* **Área de Cobertura Específica:** Monitora uma área geográfica pré-definida (Bounding Box).
* **Interface Limpa:** Foco total no mapa para uma visualização sem distrações.

---

### Demonstração

*Aqui você pode colocar um print da sua aplicação funcionando.*

![Imagem do AeroGuard em funcionamento](https://placehold.co/800x600/333/FFF?text=AeroGuard+em+A%C3%A7%C3%A3o)

---

### Como Executar o Projeto

Siga os passos abaixo para configurar e rodar o AeroGuard em sua máquina local.

#### Pré-requisitos

* [Python 3.7+](https://www.python.org/downloads/)
* [Git](https://git-scm.com/downloads)
* Uma conta e credenciais de API do [OpenSky Network](https://opensky-network.org/apidoc/rest.html#authentication).

#### 1. Clonar o Repositório

Abra seu terminal ou prompt de comando e clone este repositório:
```bash
git clone <URL_DO_SEU_REPOSITORIO_GIT>
cd <NOME_DA_PASTA_DO_PROJETO>
```

#### 2. Criar e Ativar o Ambiente Virtual

É uma boa prática usar um ambiente virtual para isolar as dependências do projeto.

**No Windows:**
```bash
python -m venv venv
.\venv\Scripts\activate
```

**No macOS / Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```
*(Seu prompt de comando deve mudar para indicar que o ambiente `venv` está ativo).*

#### 3. Configurar as Credenciais da OpenSky

A aplicação precisa das suas credenciais para acessar a API da OpenSky.

1.  Na pasta raiz do projeto, crie um arquivo chamado `.env`.
2.  Abra o arquivo `.env` e adicione suas credenciais no seguinte formato:

```ini
# Substitua 'seu_usuario' e 'sua_senha' pelas suas credenciais reais da OpenSky
OPENSKY_USERNAME="seu_usuario_aqui"
OPENSKY_PASSWORD="sua_senha_aqui"
```

#### 4. Instalar as Dependências

Com o ambiente virtual ativo, instale todas as bibliotecas Python necessárias usando o arquivo `requirements.txt`.
```bash
pip install -r requirements.txt
```

#### 5. Executar a Aplicação

A aplicação precisa que dois scripts sejam executados em paralelo: o backend primeiro, e depois a interface gráfica.

**Passo 1: Rodar o Backend (`back.py`)**

1.  Abra um terminal (com o ambiente virtual ativo).
2.  Execute o servidor Flask:
    ```bash
    python back.py
    ```
3.  O terminal deverá exibir uma mensagem indicando que o servidor está rodando em `http://127.0.0.1:5000`. **Deixe este terminal aberto.**

**Passo 2: Rodar a Interface Gráfica**

1.  Abra um **novo** terminal (e ative o ambiente virtual novamente, se necessário).
2.  Execute o script da interface gráfica PyQt5:
    ```bash
    # Substitua 'seu_arquivo_pyqt.py' pelo nome real do seu arquivo com o código PyQt5
    python seu_arquivo_pyqt.py 
    ```

Uma janela do AeroGuard deve aparecer na sua tela, carregando o mapa e, em alguns segundos, exibindo os ícones das aeronaves.

---

### Personalizando a Área e a Visualização do Mapa

Você pode facilmente alterar a região geográfica monitorada e a visão padrão do mapa.

#### 1. Alterar a Área de Busca de Aeronaves (Backend)

Para mudar a área geográfica de onde os dados dos aviões são coletados, você precisa editar o "bounding box" (caixa delimitadora).

* **Arquivo:** `back.py`
* **Linha a ser modificada:84**

```python
# Coordenadas da sua área de interesse (min lat, max lat, min lon, max lon)
BBOX_VALUES = (-27.333, -16.19, -52.36, -44.736) # Exemplo, ajuste para sua área
```

* **O que significa cada valor:**
    * `lamin`: Latitude mínima (borda Sul)
    * `lamax`: Latitude máxima (borda Norte)
    * `lomin`: Longitude mínima (borda Oeste)
    * `lomax`: Longitude máxima (borda Leste)

Você pode usar ferramentas online como o [bboxfinder](http://bboxfinder.com/) para encontrar as coordenadas da sua área de interesse.

#### 2. Alterar a Visão Inicial do Mapa (Frontend)

Para mudar o ponto central e o nível de zoom que o mapa exibe ao ser carregado.

* **Arquivo:** `static/map_display.html`
* **Linha a ser modificada:31**

```javascript
var map = L.map('mapid').setView([-7.23, -35.88], 10); // Ex: Campina Grande, Paraíba
```

* **O que significa cada valor:**
    * `[-7.23, -35.88]`: As coordenadas do centro do mapa, no formato `[latitude, longitude]`.
    * `10`: O nível de zoom inicial (valores maiores aproximam mais).

**Importante:** É recomendado que a visão inicial do mapa (`setView`) esteja coerente com a área de busca de dados (`BBOX_VALUES`) para uma melhor experiência.

---

---
### Estrutura do Projeto
```
/seu-projeto/
├── .env                  # Suas credenciais da API (CRIAR MANUALMENTE)
├── back.py               # Servidor Backend Flask
├── seu_arquivo_pyqt.py   # Interface Gráfica Desktop
├── requirements.txt      # Dependências Python
└── static/
    └── map_display.html  # Frontend com o mapa Leaflet
