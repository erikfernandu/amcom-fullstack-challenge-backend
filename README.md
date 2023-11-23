
# Papelaria AMCom

    Bem-vindo à aplicação back-end da Papelaria AMCom, projetada para a gestão de vendas e apuração de comissão das vendas.

# Pré-requisitos

    Certifique-se de ter as seguintes dependências instaladas em seu ambiente de desenvolvimento:

    ## python (3.11.2)
    ## django (4.2.7)
    ## djangorestframework (3.14.0)
    ## django-cors-headers (4.3.1)

# Instalação

    1. Faça o download do projeto via GitHub usando o seguinte comando:

        git clone --depth 1 https://github.com/erikfernandu/amcom-fullstack-challenge-backend.git

    2. Como boa prática, realize o processo de criação e ativação do ambiente virtual:

        cd amcom-fullstack-challenge-backend
        install virtualenv venv
        pip install -r requirements.txt
        source venv/bin/activate.sh

# Configuração

        python3 manage.py migrate
        python3 manage.py makemigrations
        python3 manage.py createsuperuser

    Preencha todos os campos solicitados.

# Uso

    Inicie o servidor local com o comando:

        python3 manage.py runserver

    Acesse a aplicação em seu navegador através do link http://localhost:8000/admin

    Faça login e inicie o processo de registro dos produtos.

# Contribuições

    Sinta-se à vontade para contribuir para este projeto! Abra problemas (issues) e envie pull requests para melhorar nosso código.

# Contato

    Em caso de dúvidas ou problemas, sinta-se à vontade para entrar em contato:

        Nome: Erik Morais
        E-mail: erikfernandu@outlook.com
        Linkedin: https://www.linkedin.com/in/erik-fernando-morais-dos-santos-66911b246/

    Fique à vontade para explorar, modificar e aprimorar nosso código. Agradecemos sua contribuição!