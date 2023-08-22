from tinydb import TinyDB

class WsDb:
    def __init__(self):
        self.__DB = TinyDB("Utils/Database/ws.json")

    def get_ws(self, wsID):
        return self.__DB.get(doc_id=wsID)

    def get_all_ws(self):
        return self.__DB.all()

    # Getter for players
    def get_players(self, wsID):
        ws = self.__DB.get(doc_id=wsID)
        return ws["players"] if ws else None

    # Setter for players
    def set_players(self, wsID, players):
        self.__DB.update({"players": players}, doc_ids=[wsID])

    def add_player(self, wsID, player):
        ws = self.__DB.get(doc_id=wsID)
        if ws:
            players = ws["players"]
            players.append(player)
            self.__DB.update({"players": players}, doc_ids=[wsID])

    def remove_player(self, wsID, player):
        ws = self.__DB.get(doc_id=wsID)
        if ws:
            players = ws["players"]
            players.remove(player)
            self.__DB.update({"players": players}, doc_ids=[wsID])

    # Getter for msgID
    def get_msgID(self, wsID):
        ws = self.__DB.get(doc_id=wsID)
        return ws["msgID"] if ws else None

    # Setter for msgID
    def set_msgID(self, wsID, msgID):
        self.__DB.update({"msgID": msgID}, doc_ids=[wsID])


    # Getter for name
    def get_name(self, wsID):
        ws = self.__DB.get(doc_id=wsID)
        return ws["name"] if ws else None

    # Setter for name
    def set_name(self, wsID, name):
        self.__DB.update({"name": name}, doc_ids=[wsID])

    # Getter for size
    def get_size(self, wsID):
        ws = self.__DB.get(doc_id=wsID)
        return ws["size"] if ws else None

    # Setter for size
    def set_size(self, wsID, size):
        self.__DB.update({"size": size}, doc_ids=[wsID])

    # Getter for startDate
    def get_startDate(self, wsID):
        ws = self.__DB.get(doc_id=wsID)
        return ws["startDate"] if ws else None

    # Setter for startDate
    def set_startDate(self, wsID, start_date):
        self.__DB.update({"startDate": start_date}, doc_ids=[wsID])

    def get_role_IDs(self, wsID):
        ws = self.__DB.get(doc_id=wsID)
        return ws["wsRoleIDs"] if ws else None

    def set_role_IDs(self, wsID, roleIDs):
        self.__DB.update({"wsRoleIDs": roleIDs}, doc_ids=[wsID])

    def get_msg_channel(self, wsID):
        ws = self.__DB.get(doc_id=wsID)
        return ws["msgChannel"] if ws else None

    def set_msg_channel(self, wsID, msgChannel):
        self.__DB.update({"msgChannel": msgChannel}, doc_ids=[wsID])

#
# if __name__ == "__main__":
#     ws_db = WsDb()
#
#     print(ws_db.get_msgID(2))
#     ws_db.set_msgID(2, -2)
#     print(ws_db.get_msgID(2))