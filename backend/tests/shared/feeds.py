from app.models import User, Cleaning


async def new_and_updated_cleanings(users: list[User]) -> list[Cleaning]:
    new_cleanings = await Cleaning.bulk_create(
        [
            Cleaning(
                name=f"feed item cleaning job - {index}",
                description=f"test description for feed item cleaning: {index}",
                price=float(f"{index}9.99"),
                type=["full_clean", "spot_clean", "dust_up"][index % 3],
                user_id=users[index % len(users)].id,
            )
            for index in range(50)
        ]
    )

    for index in range(0, len(new_cleanings), 4):
        new_cleanings[index].description = f"Updated {new_cleanings[index].description}"
        new_cleanings[index].price = float(new_cleanings[index].price) + 100.0

    await Cleaning.bulk_update(new_cleanings, fields=["description", "price"])
    return new_cleanings
