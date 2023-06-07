from fastapi import FastAPI
from pydantic import  BaseModel
from typing import List

app = FastAPI()


class Vehicle(BaseModel):
    immatriculation: str
    owner: str
    category: str
    insurance_rating: float


# On crée une liste d'exemple d'engins (voitures et motos)
vehicles = [
    Vehicle(immatriculation="AB-123-CD", owner="Sœur Marie", category="Voiture", insurance_rating=1.2),
    Vehicle(immatriculation="EF-456-GH", owner="Sœur Anne", category="Moto", insurance_rating=0.8),
    Vehicle(immatriculation="IJ-789-KL", owner="Communauté du Togo", category="Voiture", insurance_rating=1.5),
]

# Le endpoint /category/<category> renvoie la liste des engins de cette catégorie
@app.get("/category/{category}")
async def get_vehicles_by_category(category: str):
    return [vehicle for vehicle in vehicles if vehicle.category == category]

# Le endpoint /owner/<owner> renvoie la liste des engins du propriétaire
@app.get("/owner/{owner}")
async def get_vehicles_by_owner(owner: str):
    return [vehicle for vehicle in vehicles if vehicle.owner == owner]

# Le endpoint /bills/<owner> renvoie la facture imputée à <owner> sur la base des immatriculations qui sont les siennes
@app.get("/bills/{owner}")
async def get_bill_for_owner(owner: str):
    vehicles_of_owner = [vehicle for vehicle in vehicles if vehicle.owner == owner]
    total_insurance_cost = sum(vehicle.insurance_rating for vehicle in vehicles_of_owner)
    total_economat_profit = sum((vehicle.insurance_rating * 0.2) for vehicle in vehicles_of_owner)
    return {
        "owner": owner,
        "immatriculations": [vehicle.immatriculation for vehicle in vehicles_of_owner],
        "total_insurance_cost": total_insurance_cost,
        "total_economat_profit": total_economat_profit,
        "total_bill": total_insurance_cost + total_economat_profit
    }
    
    
# Le endpoint /bills renvoie la facture imputée à chaque propriétaire
@app.get("/bills")
async def get_bill_for_all_owners():
    bills = []
    for owner in set(vehicle.owner for vehicle in vehicles):
        bills.append(await get_bill_for_owner(owner))
    return bills

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=80000)
   
    