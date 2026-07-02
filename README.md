# CRM Imobiliário

CRM imobiliário desenvolvido em Python, Streamlit e SQLite para gerenciamento de leads e acompanhamento comercial.

## Funcionalidades

- Importação de planilhas Excel
- Armazenamento em SQLite
- Busca por nome
- Busca por telefone
- Filtro por status
- Edição de leads
- Histórico persistente
- Integração com WhatsApp
- Mensagens personalizadas por template
- Compatível com notebook e celular

## Tecnologias

- Python
- Streamlit
- SQLite
- Pandas
- OpenPyXL

## Instalação

Criar ambiente virtual:

```bash
python -m venv .venv
```

Ativar ambiente:

### Windows

```bash
.venv\Scripts\activate
```

### Git Bash

```bash
source .venv/Scripts/activate
```

Instalar dependências:

```bash
pip install -r requirements.txt
```

Executar:

```bash
streamlit run app.py
```

## Estrutura

```text
app.py              Interface principal
database.py         Banco de dados SQLite
importador.py       Importação de planilhas
mensagens.py        Templates de mensagens
crm.db              Banco local
uploads/            Arquivos importados
backups/            Backups do banco
```

## Roadmap

### V1

- [x] Importação de Excel
- [x] Busca de leads
- [x] Edição de cadastro
- [x] Integração WhatsApp

### V2

- [ ] Origem do Lead
- [ ] Dashboard comercial
- [ ] Indicadores de conversão
- [ ] Controle de atividades
- [ ] Hospedagem online

## Autor

Eduardo Silva