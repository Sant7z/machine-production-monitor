def validate_mass(data):
    alerts = []

    for index, row in data.iterrows():
        mass = row["mass"]

        if mass < 95 or mass > 105:
            alerts.append(
                f"Mass out of range on machine {row['machine_id']} at {row['timestamp']} (mass={mass})"
            )

    return alerts