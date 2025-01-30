from os import environ
import logging
import requests
import json
import asyncio
from tortoise import Tortoise, run_async
from utils import str2hex, hex2str, get_function_selector
from controllers import *
from dtos import UserRegistration, TripRegistration
from decimal import Decimal
# import db_manager as dbm

logging.basicConfig(level="INFO")
logger = logging.getLogger(__name__)

rollup_server = environ["ROLLUP_HTTP_SERVER_URL"]
logger.info(f"HTTP rollup_server url is {rollup_server}")

initializator = Initializator()
payload_handler = PayloadHandler()
user_controller = UserController()
trip_controller = TripController()
bike_controller = BikeController()
token_controller = TokenController()
wallet_controller = WalletController()

async def init_db():
    await Tortoise.init(
        db_url='sqlite://db.sqlite3',
        modules={'models': ['models']}
    )
    await Tortoise.generate_schemas()
    await initializator.initialize_all_tables()


def handle_advance(data):
    logger.info(f"Received advance request data {data}")
    payload = payload_handler.get_payload(data)
    option = payload_handler.get_option(payload)
    logger.info(f"Initial Payload: {payload}")

    logger.info(f"OPTION: {option}")

    match option:
        # case str2hex("erc20_deposit"):
        #     try:
        #         wallet_controller.update_token_balance(token_id=1, user_id=1, amount=0)
        #     except Exception as err:
        #         logger.error(f"ERC20 DEPOSIT ERROR: {err}")
        #     return "accept"
        
    
        # case str2hex("erc20_withdraw"):
        #     try:
        #         wallet_controller.update_token_balance(token_id=1, user_id=1, amount=0)
        #     except Exception as err:
        #         logger.error(f"ERC20 WITHDRAW ERROR: {err}")
        #     return "accept"

        case "new_user":
            try:
                register_user = UserRegistration(name=payload['name'], address=payload['address'])
                new_user = asyncio.run(user_controller.insert_user(user=register_user)) 
            except Exception as err:
                logger.error(f"ERROR: {err}")


        case "new_trip":
            generated_carbon_token = token_controller.calculates_new_generated_tokens(token_id=1, travelled_distance=payload['travelled_distance'])
            register_trip = TripRegistration(user_id=int(payload["id_user"]),
                                            bike_id=int(payload["id_bike"]),
                                            travelled_distance=float(payload["travelled_distance"]),
                                            source_parking_station_id=int(payload["source_parking_station"]),
                                            destination_parking_station_id=int(payload["destination_parking_station"]),
                                            source_timestamp=payload['source_timestamp'],
                                            destination_timestamp =payload["destination_timestamp"])
            try: 
                asyncio.run(trip_controller.insert_trip(trip=register_trip))
            except Exception as err:
                logger.error(f"NEW TRIP ERROR: {err}")

            try:
                asyncio.run(bike_controller.update_parking_station(bike_id=register_trip.bike_id, destination_parking_station_id=register_trip.destination_parking_station_id))
            except Exception as err:
                logger.error(f"UPDATE PARKING STATION ERROR: {err}")

            # try:
            asyncio.run(wallet_controller.update_token_balance(token_id=1, user_id=register_trip.user_id, amount=generated_carbon_token))
            # except Exception as err:
            #     logger.error(f"UPDATE WALLET BALANCE ERROR: {err}")
        

        case _:
            logger.info("THE OPTION DOES NOT MATCH.")
            return "accept"

    return "accept"

def handle_inspect(data):
    logger.info(f"Received inspect request data {data}")
    # con = dbm.connect_db("moveuff.db")
    # bikes = dbm.show_bikes(con)
    # logger.info(f"BIKES: {bikes}")

    return "accept"

handlers = {
    "advance_state": handle_advance,
    "inspect_state": handle_inspect,
}

finish = {"status": "accept"}

run_async(init_db())

while True:
    logger.info("Sending finish")
    response = requests.post(rollup_server + "/finish", json=finish)
    logger.info(f"Received finish status {response.status_code}")
    if response.status_code == 202:
        logger.info("No pending rollup request, trying again")
    else:
        rollup_request = response.json()
        data = rollup_request["data"]
        handler = handlers[rollup_request["request_type"]]
        finish["status"] = handler(rollup_request["data"])
