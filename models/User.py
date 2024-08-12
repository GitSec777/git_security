class User:
    def __init__(self, id, name, mfa, role):
        self._id = id
        self._name = name
        self._mfa = mfa
        self._role = role

    # Getter methods
    def get_id(self):
        return self._id

    def get_name(self):
        return self._name

    def get_mfa(self):
        return self._mfa

    def get_role(self):
        return self._role

    # Setter methods
    def set_id(self, id):
        self._id = id

    def set_name(self, name):
        self._name = name

    def set_mfa(self, mfa):
        self._mfa = mfa

    def set_role(self, role):
        self._role = role
    