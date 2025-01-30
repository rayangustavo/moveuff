import json
import logging
from eth_abi import encode
from utils import hex2str, str2hex, get_function_selector
from dtos import UserRegistration, TokenRegistration, TripRegistration, BikeRegistration
from models import UserModel, TokenModel, TripModel, BikeModel, WalletModel, ParkingStationModel
from decimal import Decimal

logging.basicConfig(level="INFO")
logger = logging.getLogger(__name__)

class Initializator():
    async def initialize_tokens(self):
        await TokenModel.create(name="MoveUFF", symbol="MUFF", address="0x123abc")

    async def initialize_parking_stations(self):
        await ParkingStationModel.create(name="Estação Central", address="Rua A, 123")
        await ParkingStationModel.create(name="Estação Norte", address="Rua B, 456")

    async def initialize_bikes(self):
        station = await ParkingStationModel.get(id=1) 
        await BikeModel.create(serial_number="BIKE001", parking_station_id=station)
        await BikeModel.create(serial_number="BIKE002", parking_station_id=station)

    async def initialize_users(self):
        await UserModel.create(name="Rayan", address="0x1111")
        await UserModel.create(name="Gustavo", address="0x2222")

    async def initialize_wallets(self):
        rayan = await UserModel.get(id=1)
        gustavo = await UserModel.get(id=2)
        muff = await TokenModel.get(id=1)
        await WalletModel.create(user_id=rayan, token_id=muff, balance=100.50)
        await WalletModel.create(user_id=gustavo, token_id=muff, balance=50.25)

    async def initialize_all_tables(self):
        await self.initialize_parking_stations()
        await self.initialize_bikes()
        await self.initialize_tokens()
        await self.initialize_users()
        await self.initialize_wallets()

class PayloadHandler():
    def get_payload(self, data: dict) -> dict:
        payload = json.loads(hex2str(data['payload']))
        return payload
    
    def get_option(self, payload: dict) -> str:
        option = payload.get('option', '')
        return option
    

class BikeController():
    async def update_parking_station(self, bike_id: int, destination_parking_station_id: int):
        bike = await BikeModel.get(id=bike_id)
        parking_station = await ParkingStationModel.get(id=destination_parking_station_id)
        bike.parking_station_id = parking_station
        await bike.save()
        logger.info(f"Updated Bike {bike_id} Parking Station: to {destination_parking_station_id}.")


class WalletController():
    async def update_token_balance(self, token_id: int, user_id: int, amount: Decimal):
        wallet = await WalletModel.filter(user_id=user_id, token_id=token_id).first()
        if wallet:
            wallet.balance += amount
            await wallet.save() 
            logger.info(f"USER {user_id} UPDATED BALANCE: {wallet.balance}.")
        else:
            wallet = await WalletModel.create(user_id=user_id, token_id=token_id, balance=amount)
            logger.info(f"USER {user_id} NEW BALANCE: {wallet.balance}.")


    def withdraw_tokens(token_id: int, address: str, amount: Decimal):
        function_signature = "transfer(address,uint256)"
        function_selector = get_function_selector(function_signature)
        function_payload = function_selector + encode(["address", "uint256"], [address, amount])
        voucher_payload = "0x" + function_payload.hex()
        return


class TokenController():
    def calculates_new_generated_tokens(self, token_id: int, travelled_distance: float):
        generated_carbon_token = int(travelled_distance/1000) + 1 
        return Decimal(generated_carbon_token)
    

class TripController():
    async def insert_trip(self, trip: TripRegistration):
        new_trip = await TripModel.create(user_id=trip.user_id,
                                          bike_id=trip.bike_id,
                                          travelled_distance=trip.travelled_distance,
                                          source_parking_station_id=trip.source_parking_station_id,
                                          destination_parking_station_id=trip.destination_parking_station_id,
                                          source_timestamp=trip.source_timestamp,
                                          destination_timestamp=trip.destination_timestamp)

class TokenPerTripController():
    async def update_token_generated_by_trip(token_id: int, trip_id: int, amount: Decimal):
        token = await TokenModel.get(id=token_id)
        trip = await TripModel.get(id=trip_id)
        token_by_trip = await WalletModel.filter(token_id=token, trip_id=trip).select_related("token")
        token_by_trip += amount
        await token_by_trip.save()

class UserController():
    async def insert_user(self, user: UserRegistration):
        new_user = await UserModel.create(name=user.name, address=user.name)
        logger.info(f'New User Registred: {new_user}')
        return new_user