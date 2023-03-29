Projeto desenvolvido para o processo seletivo (EDITAL Nº 05/2022 – LAIS/UFRN).

Para rodar o projeto em ambiente Windows:

1º - Crie um ambiente virtual com o comando: python -m venv venv
2º - Ative o ambiente virtual com o comando: venv\Scripts\activate
3º - Instale as dependências com o comando: pip install -r requirements.txt
4º - Altere em lais_huol => settings.py as configurações de banco de dados para o seu ambiente local
5º - Rode o projeto com o comando: python manage.py runserver
6º - Atualize o banco de dados com o comando: python manage.py migrate
7º - Para importar os estabelecimentos, utilize o comando: python manage.py inserir_estabelecimentos
8º - Tudo pronto! Basta utilizar a aplicação.
