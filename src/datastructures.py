"""
Update this file to implement the following already declared methods:
- add_member: Should add a member to the self._members list
- delete_member: Should delete a member from the self._members list
- get_member: Should return a member from the self._members list
"""

class FamilyStructure:
    def __init__(self, last_name):
        self.last_name = last_name
        self._next_id = 1
        self._members = []

    # This method generates a unique incremental ID
    def _generate_id(self):
        generated_id = self._next_id
        self._next_id += 1
        return generated_id

    def add_member(self, member):
        new_member = dict(member) if isinstance(member,dict) else {}## You have to implement this method
        if "id" not in new_member or new_member["id"] is None:
            new_member["id"] = self._generate_id()
            
        new_member["last_name"] = self.last_name
        
        self._members.append(new_member)## Append the member to the list of _members
        return new_member

    def delete_member(self, id):
        for idx, m in enumerate(self.members):
            if m.get("id") == id:
                self._members.pop(idx)## You have to implement this method
                return True
        return False  ## Loop the list and delete the member with the given id

    def get_member(self, id):
        for m in self._members:
            if m.get("id") == id:
                return m ## You have to implement this method
        return None ## Loop all the members and return the one with the given id
        

    # This method is done, it returns a list with all the family members
    def get_all_members(self):
        return self._members