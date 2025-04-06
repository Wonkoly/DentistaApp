import json

def get_all_reservas():
    with open("data/reservas.json", "r") as f:
        return json.load(f)

def actualizar_estado_reserva(reserva_id, nuevo_estado):
    with open("data/reservas.json", "r+") as f:
        reservas = json.load(f)
        for r in reservas:
            if r["id"] == reserva_id:
                r["estado"] = nuevo_estado
                break
        f.seek(0)
        json.dump(reservas, f, indent=2)
        f.truncate()

def get_reservas_por_dentista(email_dentista):
    with open("data/reservas.json", "r") as f:
        reservas = json.load(f)
        return [r for r in reservas if r.get("dentista", email_dentista) == email_dentista]