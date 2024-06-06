import strawberry
from typing import Optional
from strawberry.field_extensions import InputMutationExtension

FRUITS = [
    {"id": "1", "weight": 50.0},
    {"id": "2", "weight": 150.0},
    {"id": "3", "weight": 200.0},
]

@strawberry.type
class Fruit:
    id: strawberry.ID
    weight: float

@strawberry.type
class Query:
    @strawberry.field
    def hello(self) -> str:
        return "world"

@strawberry.input
class UpdateFruitWeightInput:
    id: strawberry.ID
    weight: float

@strawberry.type
class Mutation:
    @strawberry.mutation(extensions=[InputMutationExtension()])
    def update_fruit_weight(
        self,
        info: strawberry.Info,
        input: UpdateFruitWeightInput
    ) -> Optional[Fruit]:
        fruit = next((f for f in FRUITS if f["id"] == input.id), None)
        if fruit is None:
            return None
        
        fruit["weight"] = input.weight
        
        return Fruit(id=fruit["id"], weight=fruit["weight"])

schema = strawberry.Schema(query=Query, mutation=Mutation)
