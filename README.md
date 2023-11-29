
# Papelaria AMCom

    Bem-vindo à aplicação back-end da Papelaria AMCom, projetada para a gestão de vendas e apuração de comissão das vendas.
    O presente documento visa orientar o processo de instação e configuração básica em ambiente Linux.

# Pré-requisitos

    Este projeto faz uso das seguintes dependências instaladas para o correto funcionamento.
    O processo de instalação destas, será abordada no próximo tópico.

    ## python (3.11.2)
    ## django (4.2.7)
    ## djangorestframework (3.14.0)
    ## django-cors-headers (4.3.1)

# Instalação

    1. Faça o download do projeto via GitHub usando o seguinte comando:

        git clone --depth 1 https://github.com/erikfernandu/amcom-fullstack-challenge-backend.git

    2. Para acessar o diretório dos arquivos deste projeto:

        cd amcom-fullstack-challenge-backend

    3. Como boa prática, realizaremos o processo instalação, criação e ativação do ambiente virtual:

        sudo apt install virtualenv
        virtualenv venv 
        source venv/bin/activate.sh
    
    4. Para instalação das dependências do projeto:

        pip install -r requirements.txt

# Configuração

        python3 manage.py migrate
        python3 manage.py makemigrations
        python3 manage.py loaddata initial_data.json
        python3 manage.py createsuperuser

    Preencha todos os campos solicitados: nome, e-mail e senha.

# Uso

    Inicie o servidor local com o comando:

        python3 manage.py runserver

    Acesse a aplicação em seu navegador através do link http://localhost:8000/admin

    Faça login e inicie o processo de registro dos produtos, vendedores e clientes.

# Contribuições

    Sinta-se à vontade para contribuir para este projeto! Abra problemas (issues) e envie pull requests para melhorar nosso código.

# Contato

    Em caso de dúvidas ou problemas, sinta-se à vontade para entrar em contato:

        Nome: Erik Morais
        E-mail: erikfernandu@outlook.com
        Linkedin: https://www.linkedin.com/in/erik-fernando-morais-dos-santos-66911b246/

    Fique à vontade para explorar, modificar e aprimorar nosso código. Agradecemos sua contribuição!