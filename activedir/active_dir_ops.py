from ldap3 import Server, Connection, ALL


class ActiveDirectoryOps:

    def __init__(self, ad_user, ad_pass, server, port):
        """Initializing class variables."""
        self.ad_user = ad_user
        self.ad_password = ad_pass
        self.server = server
        self.port = port

    def get_connection(self):
        s = Server(f'{self.server}',
                   port=self.port, use_ssl=True, get_info=ALL)
        corp_c = Connection(s, user=self.ad_user, password=self.ad_password,
                            authentication='SIMPLE')

        return corp_c

    def search_user(self, search_base, attributes_to_get, search_filter):
        corp_c = self.get_connection()
        corp_c.bind()
        ldap_data = corp_c.extend.standard.paged_search(
            search_base=search_base, attributes=attributes_to_get, search_filter=search_filter)
        return ldap_data


ad_user = ''
ad_pass = None
server = ''
port = ''


c = ActiveDirectoryOps(ad_user, ad_pass, server, port)

# e.g. 'DC=<>,DC=<>,DC=<>,DC=<>,DC=<>'
search_base = ''
# e.g. ['employeeNumber', 'sAMAccountName', 'displayName', 'objectSid', 'mail','lastLogonTimestamp']
attributes_to_get = ''
# e.g. '(&(objectClass=user)(objectSid=*))'
search_filter = ''
ldap_data = c.search_user(search_base, attributes_to_get, search_filter)
