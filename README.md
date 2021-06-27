# Lôro

[![pipeline status](https://gitlab.com/vintem/chatbots/loro/badges/main/pipeline.svg)](https://gitlab.com/vintem/chatbots/loro/-/commits/main)

Um *Chatbot* para whatsapp feito em python, bootstrap e docker;
compatível com [twilio](https://www.twilio.com/whatsapp)

## Como Utilizar este software

### 1 - Download

Este software pode ser baixado gratuitamente e testado livremente no
[github](https://github.com/marcusmello/loro). Se preferir, pode fazer o
download do arquivo *.zip* [neste
link](https://github.com/marcusmello/loro/archive/refs/heads/main.zip);
basta descompactar o arquivo e seguir as instruções abaixo:

### 2 - Lançando o servidor web

#### Pré-requisitos

- [Docker](https://docs.docker.com/get-started/)
- [Docker-compose](https://docs.docker.com/compose/install/)

#### configuração inicial do sistema

Renomeie o arquivo *template.env* apenas para *.env*, altere as variáveis para os valores desejados, respeitando as regras descritas no arquivo

#### Subindo o cluster

    docker-compose up

ou, para correr os contâiners em *background* (*Detached mode*):

    docker-compose up -d

Acessando o endereço [http://localhost:8000/](http://localhost:8000/),
já é possível interagir com a interface do sistema.

### 3 - Criando as respostas

Irure sunt fugiat ea quis consectetur laborum laborum incididunt fugiat
nulla mollit. Eiusmod enim minim nulla non fugiat qui est anim sunt
ipsum commodo do laboris. Laborum incididunt occaecat aute nostrud.

### 4 - Configurando URL de callback no twilio

Ad veniam pariatur id eu labore laboris ea. Dolore id ullamco esse nisi
excepteur aliqua laborum nisi ipsum id magna et duis dolore.
Exercitation ipsum dolore laborum.

#### 4.1 - Modo sandbox

Enim ipsum id velit ullamco ut amet quis velit. Esse magna nostrud
nostrud fugiat. Consectetur minim sit culpa ipsum non quis anim veniam
voluptate pariatur proident deserunt eu. Labore aliqua sint consectetur
incididunt ut enim aute velit proident esse enim ad proident.

#### 4.2 - Conta verificada

Aliqua do eu anim minim adipisicing. Ad cupidatat deserunt proident
dolore culpa commodo cupidatat sit. Eu Lorem ea nulla pariatur deserunt
est aute est nostrud dolor. Exercitation cillum non ea mollit cupidatat
laboris veniam ipsum magna consectetur et. Pariatur ex laborum occaecat
deserunt Lorem magna laboris nulla dolore dolor duis labore. Sit nisi
fugiat velit dolor est est reprehenderit pariatur aute. Laborum nulla
nostrud nostrud non proident nulla aliqua occaecat velit dolor.

## Alguns detalhes deste projeto

*Backend/API* baseados em [fastapi](https://fastapi.tiangolo.com)

*Frontend* concebido em
[bootstrap](https://getbootstrap.com/docs/5.0/getting-started/introduction/)
renderizado pelo sistema de templates
[jinja](https://jinja.palletsprojects.com/en/3.0.x/).

O projeto tem arquitetura monolítica modular (mais detalhes abaixo em
[Estrutura do projeto](#estrutura-do-projeto), tendo suas dependências,
ambiente virtual, empacotamento gerenciados pelo [poetry](https://python-poetry.org/) num nível
mais baixo, e pelo
[docker](https://www.docker.com/)/[docker-compose](https://github.com/docker/compose)
numa abstração mais superior.

A comunicação com a API do *whatsapp* ([whatsapp business
API](https://www.whatsapp.com/business/?lang=pt_br)) é garantida pelo
serviço [twilio](https://www.twilio.com/whatsapp), um parceiro comercial
do facebook, recomendado por este em sua [página
oficial](https://www.facebook.com/business/partner-directory/search?solution_type=messaging&platforms=whatsapp).

## ATENÇÃO

---

Este software é uma prova de conceito; como tal ainda carece de testes
exaustivos, adição de funcionalidades e *code review*, não sendo
recomendado portanto seu uso em produção.

---

---

Apesar de o **fastAPI** ser um framework assíncrono, a comunicação com o
banco de dados é feita através da biblioteca de ORM
[pony](https://ponyorm.org/), que não é (nativamente) assíncrona. Esta
foi uma decisão de projeto; está nos planos de refatoração a
substituição por uma biblioteca assíncrona.

---

---

Podem haver custos para envios de mensagens; ESTE software pode ser
baixado sem custos, seu uso é livre, dentro das restrições impostas pela
sua licença. Entretanto, a operação comercial do envio de mensagens não
é competência deste software, que apenas automatiza as respostas, do
modo recomendado pela empresa responsável pelo
[whatsapp](https://www.whatsapp.com), o
[facebook](https://pt-br.facebook.com/). Este modo demanda a
intermediação de um parceiro comercial, neste caso o
[twilio](https://www.twilio.com), que [cobra por mensagem
enviada](https://www.twilio.com/whatsapp/pricing/br).

---

## Estrutura do projeto

```├── app
│   ├── app
│   │   ├── api
│   │   │   └── api_v1
│   │   │       ├── api.py
│   │   │       └── endpoints
│   │   │           ├── answers.py
│   │   │           └── twilio_hook.py
│   │   ├── lib
│   │   │   ├── chatbot
│   │   │   └── utils
│   │   │       ├── db
│   │   │       │   └── sql
│   │   │       │       ├── crud
│   │   │       │       │   └── answers.py
│   │   │       │       ├── database.sqlite
│   │   │       │       └── models.py
│   │   │       ├── exceptions.py
│   │   │       ├── schemas.py
│   │   │       └── tools
│   │   │           └── string_conversion.py
│   │   ├── main.py
│   │   ├── settings
│   │   │   ├── database_adapters.py
│   │   │   ├── default_answers.py
│   │   │   ├── general.py
│   │   │   ├── url_paths_handler.py
│   │   │   └── web_templating.py
│   │   └── web
│   │       ├── pages
│   │       │   ├── answers_dynamic_form.py
│   │       │   ├── answers.py
│   │       │   ├── home.py
│   │       │   └── router.py
│   │       ├── static
│   │       │   ├── assets
│   │       │   │   ├── img
│   │       │   │   │   ├── favicon.ico
│   │       │   │   │   ├── favicon.svg
│   │       │   │   │   ├── loro.svg
│   │       │   │   │   ├── loro_transparent.png
│   │       │   │   │   └── loro_transparent.svg
│   │       │   │   └── mail
│   │       │   │       ├── contact_me.js
│   │       │   │       ├── contact_me.php
│   │       │   │       └── jqBootstrapValidation.js
│   │       │   ├── css
│   │       │   │   └── styles.css
│   │       │   └── js
│   │       │       └── scripts.js
│   │       └── templates
│   │           ├── answers
│   │           │   ├── answers.html
│   │           │   ├── base_answers.html
│   │           │   ├── delete_confirmation.html
│   │           │   ├── dynamic_form.html
│   │           │   └── not_found.html
│   │           ├── base.html
│   │           ├── clients
│   │           │   ├── not_found.html
│   │           │   └── saved.html
│   │           ├── home.html
│   │           └── page_template.html
│   ├── Dockerfile
│   ├── poetry.lock
│   └── pyproject.toml
├── CHANGELOG.md
├── docker-compose.yml
├── LICENSE
├── README.md
└── template.env
```
