# brf_performance_mercato_inventory

Executar o teste via front localhost, apontando o diretorio do teste:
locust -f locustfiles/locustfile_inventory.py

Executar em headless mode, passando usuarios e utilizando "tags":
locust --headless -f locustfiles/locustfile_inventory.py --tags test1 --users 1 -
-spawn-rate 1