Lista de Comandos:

-Para enviar o programa e os arquivos para o repositório:
1. cd (para entrar nas pastas onde esta o arquivo)
2. echo ".env" > .gitignore
3. echo "*.db" >> .gitignore 
4. git config user.name
5. git config user.email
6. git add main.py .gitignore
7. git commit -m
8. git push

-Para baixar e executar o programa em uma máquina:
1. git clone https://github.com/sofi933/sofielau.git
2. cd sofielau/av5
Recriar o arquivo .env com todas as senhas e acessos necessários do MySQL para o sistema conectar no Aiven:
3. echo MYSQL_HOST=mysql-ifcbluhyl-hvescovi-ifcblu.l.aivencloud.com > .env
4. echo MYSQL_USER=avnadmin >> .env
5. echo MYSQL_PASSWORD=AVNS_PRNk-xeaKjQw7MPwYGg >> .env
6. echo MYSQL_PORT=12960 >> .env
7. echo MYSQL_DB=defaultdb >> .env
8. uv sync
9. uv run main.py
