from locust import between, task, HttpUser, tag
import os
from dotenv import load_dotenv
from helpers.body_mercato_inventory import BodyCreatorInventory

failureMessage = "Não foi possível acessar ou visualizar o valor de idProduct"
load_dotenv()


class CargaApiInventoryMercato(HttpUser):
    host = os.environ["PRD_MERCARTO"]
    wait_time = between(1.0, 3.0)
    prefix_inventory = os.environ["PREFIX_INVENTORY_PRD"]
    token_uat = os.environ["TOKEN_INVENTORY_UAT"]
    token_prd = os.environ["TOKEN_INVENTORY_PRD"]

    @tag('test1')
    @task
    def retorno_inventory(self):
        consult_inventory_endpoint = f"{self.prefix_inventory}"
        body = BodyCreatorInventory.create_default_inventory_body()

        # Subscription Key:
        self.client.headers['X-Api-Key-User'] = f'{self.token_prd}'
        with self.client.post(url=consult_inventory_endpoint,
                              name="CargaInventoryMercato - Retorna itens",
                              catch_response=True, json=body) as response:

            #print(response.json())

            if response.status_code == 200:
                resposta = response.json()

                if resposta[0]['IdProduct'] != "":
                    print(
                        f"---- SUCESSO NA CONSULTA ---- \n Id Produtos: "
                        f"{resposta[0]['IdProduct']} \n STATUS CODE: {response.status_code}")

                else:
                    print(f"---- FALHA NA CONSULTA ----\n {response.text} \n "
                          f"STATUS CODE: {response.status_code} \n {body}")
                    response.failure(
                        failureMessage + f" Status CODE: {response.status_code}"
                    )

            else:
                print(
                    f"---- FALHA NA CONSULTA ----\n {response.text} \n STATUS CODE: {response.status_code}")
                response.failure(
                    failureMessage + f" Status CODE: {response.status_code}"
                )
