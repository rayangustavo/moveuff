from tortoise.models import Model
from tortoise import fields

class BikeModel(Model):
    id = fields.IntField(primary_key=True)
    serial_number = fields.CharField(max_length=255)
    parking_station_id = fields.ForeignKeyField('models.ParkingStationModel', related_name='bikes')

    def __str__(self):
        return self.id


class ParkingStationModel(Model):
    id = fields.IntField(primary_key=True)
    name = fields.CharField(max_length=255)
    address = fields.TextField()

    def __str__(self):
        return self.name
    

class TokenModel(Model):
    id = fields.IntField(primary_key=True)
    name = fields.CharField(max_length=255)
    symbol = fields.CharField(max_length=5)
    address = fields.CharField(max_length=255)

    def __str__(self):
        return self.name
    

class TripModel(Model):
    id = fields.IntField(primary_key=True)
    user = fields.ForeignKeyField('models.UserModel', related_name='userXtrip')
    bike = fields.ForeignKeyField('models.BikeModel', related_name='bikeXtrip')
    travelled_distance = fields.FloatField()
    source_parking_station = fields.ForeignKeyField('models.ParkingStationModel', related_name='spsXtrip')
    destination_parking_station = fields.ForeignKeyField('models.ParkingStationModel', related_name='dpsXtrip')
    source_timestamp = fields.DateField()
    destination_timestamp = fields.DateField()

    def __str__(self):
        return self.id
    

class UserModel(Model):
    id = fields.IntField(primary_key=True)
    name = fields.CharField(max_length=255)
    address = fields.CharField(max_length=255, null=False)

    def __str__(self):
        return self.name
    

class WalletModel(Model):
    user_id = fields.ForeignKeyField("models.UserModel", related_name="userXbalance")
    token_id = fields.ForeignKeyField("models.TokenModel", related_name="tokenXbalance")
    balance = fields.DecimalField(max_digits=20, decimal_places=8, default=0.0)

class TokenPerTripsModel(Model):
    token_id = fields.ForeignKeyField("models.TokenModel", related_name="tokenpertrip_token")
    trip_id = fields.ForeignKeyField("models.TripModel", related_name="tokenpertrip_trip")
    amount = fields.DecimalField(max_digits=20, decimal_places=8, default=0.0)