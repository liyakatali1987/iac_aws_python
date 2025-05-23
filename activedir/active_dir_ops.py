from ldap3 import Server, Connection, ALL
import os
import getpass


class ActiveDirectoryOps:

    def __init__(self, ad_user, ad_pass, server, port):
        """Initializing class variables."""
        self.ad_user = ad_user
        self.ad_password = ad_pass
        self.server = server
        self.port = int(port) # Ensure port is an integer

    def get_connection(self):
        s = Server(self.server, # Removed f-string as it's not necessary
                   port=self.port, use_ssl=True, get_info=ALL)
        # Ensure user is in the format DOMAIN\user or user@domain.com if required by your AD
        corp_c = Connection(s, user=self.ad_user, password=self.ad_password,
                            authentication='SIMPLE', check_names=True) # Added check_names for safety

        return corp_c

    def search_user(self, search_base, attributes_to_get, search_filter):
        corp_c = self.get_connection()
        if not corp_c.bind(): # Check if bind was successful
            print(f"Failed to bind to AD server: {corp_c.result}")
            return None 
        
        # Ensure attributes_to_get is a list if it's coming from input/env var
        if isinstance(attributes_to_get, str):
            attributes_to_get = [attr.strip() for attr in attributes_to_get.split(',')]

        ldap_data_generator = corp_c.extend.standard.paged_search(
            search_base=search_base,
            search_filter=search_filter,
            attributes=attributes_to_get,
            paged_size=100 # Example page size
        )
        
        results = []
        for entry in ldap_data_generator:
            results.append(entry)
        
        corp_c.unbind() # Good practice to unbind
        return results


# Read configuration from environment variables or prompt user
ad_user = os.environ.get('AD_USER')
if not ad_user:
    ad_user = input('Enter Active Directory username (e.g., DOMAIN\\user or user@domain.com): ')

ad_pass = os.environ.get('AD_PASS')
if not ad_pass:
    ad_pass = getpass.getpass(prompt='Enter Active Directory password: ')

server = os.environ.get('AD_SERVER')
if not server:
    server = input('Enter Active Directory server address (e.g., ad.example.com): ')

port_str = os.environ.get('AD_PORT')
if not port_str:
    port_str = input('Enter Active Directory server port (default 636 for SSL): ') or "636"

# Validate port is an integer
try:
    port = int(port_str)
except ValueError:
    print(f"Invalid port number '{port_str}'. Using default 636.")
    port = 636


# Example Usage (can be moved into a main() function or if __name__ == '__main__': block)
if __name__ == '__main__':
    print("\n--- Active Directory Operations Script ---")
    # Ensure all necessary details are provided before proceeding
    if not all([ad_user, ad_pass, server, port]):
        print("Missing one or more connection details. Aborting.")
    else:
        try:
            c = ActiveDirectoryOps(ad_user, ad_pass, server, port)

            # Example search parameters (consider getting these from input/env vars as well for flexibility)
            search_base_input = input("Enter Search Base (e.g., 'DC=example,DC=com'): ")
            
            attributes_input = input("Enter attributes to retrieve (comma-separated, e.g., 'sAMAccountName,displayName,mail'): ")
            if not attributes_input:
                attributes_to_get_list = ['sAMAccountName', 'displayName', 'mail', 'objectSid', 'lastLogonTimestamp'] # Default
                print(f"Using default attributes: {', '.join(attributes_to_get_list)}")
            else:
                attributes_to_get_list = [attr.strip() for attr in attributes_input.split(',')]

            search_filter_input = input("Enter LDAP search filter (e.g., '(&(objectClass=user)(sAMAccountName=your_user))'): ")
            
            if not all([search_base_input, attributes_to_get_list, search_filter_input]):
                print("Missing one or more search parameters. Aborting search example.")
            else:
                print(f"\nSearching with Base='{search_base_input}', Filter='{search_filter_input}', Attributes='{attributes_to_get_list}'")
                ldap_data = c.search_user(search_base_input, attributes_to_get_list, search_filter_input)

                if ldap_data is not None:
                    print("\nLDAP Search Results:")
                    if ldap_data:
                        for entry in ldap_data:
                            print(entry)
                    else:
                        print("No entries found matching the criteria.")
                else:
                    print("LDAP search failed.")
        except Exception as e:
            print(f"An error occurred during Active Directory operations: {e}")
