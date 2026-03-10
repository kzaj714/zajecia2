from pydantic import BaseModel
from typing import Dict
import json


class Parameters(BaseModel):
    apartments_json_path: str = 'data/apartments.json'
    tenants_json_path: str = 'data/tenants.json'
    bills_json_path: str = 'data/bills.json'


class Room(BaseModel):
    name: str
    area_m2: float


class Apartment(BaseModel):
    key: str
    name: str
    location: str
    area_m2: float
    rooms: Dict[str, Room]

    @staticmethod
    def from_json_file(file_path: str) -> Dict[str, 'Apartment']:
        data = None
        with open(file_path, 'r') as file:
            data = json.load(file)
        assert isinstance(data, dict), "Expected a dictionary of apartments"
        return {key: Apartment(**apartment) for key, apartment in data.items()}


class Tenant(BaseModel):
    name: str
    apartment: str
    room: str
    rent_pln: float
    deposit_pln: float
    date_agreement_from: str
    date_agreement_to: str

    @staticmethod
    def from_json_file(file_path: str) -> Dict[str, 'Tenant']:
        data = None
        with open(file_path, 'r') as file:
            data = json.load(file)
        assert isinstance(data, dict), "Expected a dictionary of tenants"
        return {key: Tenant(**tenant) for key, tenant in data.items()}


class Rachunek(BaseModel):
    kwota_pln: float
    termin_platnosci: str
    typ_rachunku: str
    mieszkanie: str

    @staticmethod
    def from_json_file(file_path: str) -> Dict[str, 'Rachunek']:
        data = None
        with open(file_path, 'r') as file:
            data = json.load(file)
        assert isinstance(data, dict), "Expected a dictionary of bills"
        return {key: Rachunek(**rachunek) for key, rachunek in data.items()}


class Manager:
    def __init__(self, parameters: Parameters):
        self.parameters = parameters

        self.apartments = {}
        self.tenants = {}
        self.rachunki = {}

        self.load_data()

    def load_data(self):
        self.apartments = Apartment.from_json_file(self.parameters.apartments_json_path)
        self.tenants = Tenant.from_json_file(self.parameters.tenants_json_path)
        self.rachunki = Rachunek.from_json_file(self.parameters.bills_json_path)


if __name__ == '__main__':
    parameters = Parameters()
    manager = Manager(parameters)

    print("MIESZKANIA:")
    for apartment in manager.apartments.values():
        print(apartment.key, apartment.name, apartment.location, apartment.area_m2)
        for room in apartment.rooms.values():
            print('  ', room.name, room.area_m2)

    print("\nNAJEMCY:")
    for tenant in manager.tenants.values():
        print(
            tenant.name,
            tenant.apartment,
            tenant.room,
            tenant.rent_pln,
            tenant.deposit_pln,
            tenant.date_agreement_from,
            tenant.date_agreement_to
        )

    print("\nRACHUNKI:")
    for rachunek in manager.rachunki.values():
        print(
            rachunek.mieszkanie,
            rachunek.typ_rachunku,
            rachunek.kwota_pln,
            rachunek.termin_platnosci
        )