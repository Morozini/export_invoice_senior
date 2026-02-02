# 📄 Consulta Geral de Nota Fiscal – Sênior (NFCP)

## 📦 Visão Geral

Este projeto realiza o consumo da **API nativa de Consulta Geral de Nota Fiscal da Sênior**, com foco na **extração, tratamento, persistência e padronização** dos dados fiscais.

A aplicação foi desenvolvida como um **serviço backend**, responsável por consultar Notas Fiscais diretamente na Sênior, aplicar regras de negócio, organizar os dados e armazená-los para uso interno, relatórios ou integrações com outros sistemas corporativos.

---

## 🎯 Objetivo do Projeto

- Centralizar o consumo da **API de Nota Fiscal da Sênior**
- Automatizar a consulta de Notas Fiscais por período
- Padronizar o tratamento dos dados fiscais
- Garantir atualização recorrente e confiável das informações
- Facilitar futuras integrações e expansões do sistema

---

## 🏗️ Arquitetura do Projeto

O projeto foi desenvolvido em **Python**, seguindo uma **arquitetura em camadas**, com separação clara de responsabilidades, facilitando manutenção, testes e evolução.

### 📂 Estrutura de Diretórios

    consultaGeralNFCP
    ├─ app
    │ ├─ api
    │ │ ├─ config.py
    │ │ └─ routers.py
    │ ├─ celery.py
    │ ├─ config
    │ │ ├─ settings.py
    │ │ └─ init.py
    │ ├─ core
    │ │ └─ executor.py
    │ ├─ database
    │ │ ├─ config.py
    │ │ └─ models.py
    │ ├─ dto
    │ │ └─ get_consultar_geral_dto.py
    │ ├─ helpers
    │ │ └─ base_zeep.py
    │ ├─ mappers
    │ │ ├─ create_consultageral_mapper.py
    │ │ └─ map_nota_fiscal_api_to_model.py
    │ ├─ repository
    │ │ └─ nota_fiscal_entrada_repository.py
    │ ├─ services
    │ │ └─ get_consulta_geral_senior.py
    │ ├─ tasks.py
    │ ├─ use_cases
    │ │ └─ consultar_geral_use_case.py
    │ └─ utils
    │ └─ gerar_semanas.py
    ├─ main.py
    └─ requirements.txt

---

## 🧱 Descrição das Camadas

- **api**  
  Define as rotas e configurações de exposição do serviço via FastAPI.

- **core**  
  Contém componentes centrais responsáveis pela execução e controle do fluxo.

- **config**  
  Gerenciamento de variáveis de ambiente e configurações globais.

- **database**  
  Configuração de conexão e definição dos modelos de dados.

- **dto (Data Transfer Objects)**  
  Padronização dos dados de entrada e saída da aplicação.

- **helpers**  
  Funções auxiliares e abstrações para consumo de serviços SOAP (Zeep).

- **mappers**  
  Conversão dos dados retornados pela API da Sênior para os modelos internos.

- **repository**  
  Camada responsável pela persistência e consulta dos dados no banco.

- **services**  
  Integração direta com a API da Sênior e execução das regras de consulta.

- **use_cases**  
  Orquestração das regras de negócio e do fluxo principal da aplicação.

- **utils**  
  Utilitários gerais, como geração de períodos para consulta (semanas, meses).

---

## ⚙️ Orquestração e Execução

- Serviço orquestrado pelo **FastAPI**
- Execução das consultas via:
  - Endpoints HTTP
  - Processamento assíncrono com **Celery**
- Projetado para execução:
  - Automática
  - Recorrente (ex: diária)
  - Por intervalos de datas

---

## 🔄 Fluxo Geral da Aplicação

1. Definição do período de consulta
2. Chamada à API de Consulta Geral de Nota Fiscal da Sênior
3. Tratamento e normalização dos dados
4. Mapeamento para o modelo interno
5. Persistência no banco de dados
6. Disponibilização para consumo interno ou integrações

---

## 🛠️ Tecnologias Utilizadas

- **Python**
- **FastAPI**
- **Celery**
- **Zeep (SOAP Client)**
- **Integração com API Sênior**
- **Arquitetura em camadas**
- **Banco de dados relacional**

---

## 📌 Observações

- Projeto desenvolvido com foco em:
  - Robustez
  - Clareza estrutural
  - Facilidade de manutenção
- Estrutura preparada para:
  - Inclusão de novas empresas e filiais
  - Expansão para novos tipos de documentos fiscais
  - Adição de novas regras de negócio

---

## 🚀 Status do Projeto

📌 *Projeto em constante evolução.*
