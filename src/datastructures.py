
class FamilyStructure:
    def __init__(self, last_name: str):
        self.last_name = last_name
        self._members: list[dict] = []
        self._next_id: int = 1

    @property
    def members(self) -> list[dict]:
        return self._members

    def _generate_id(self) -> int:
        _id = self._next_id
        self._next_id += 1
        return _id

    # Agrega un miembro y devuelve el miembro creado
    def add_member(self, member: dict) -> dict:
        if "id" in member and member["id"] is not None:
            new_id = int(member["id"])
            if new_id >= self._next_id:
                self._next_id = new_id + 1
        else:
            new_id = self._generate_id()

        # Normaliza campos mínimos
        new_member = {
            "id": new_id,
            "first_name": member["first_name"],
            "last_name": self.last_name,
            "age": int(member["age"]),
            "lucky_numbers": list(member.get("lucky_numbers", [])),
        }

        self._members.append(new_member)
        return new_member

    # Devuelve un miembro por id o None
    def get_member(self, id: int) -> dict | None:
        _id = int(id)
        return next((m for m in self._members if m["id"] == _id), None)

    def get_all_members(self) -> list[dict]:
        return self._members

    def delete_member(self, id: int) -> bool:
        _id = int(id)
        for i, m in enumerate(self._members):
            if m["id"] == _id:
                self._members.pop(i)
                return True
        return False
