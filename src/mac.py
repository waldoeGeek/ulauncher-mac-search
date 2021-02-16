import os
import json
import re

# Turn text file into dictionary
vendor_dict = {}
# vendor_file = "new.oui.txt"
vendor_file = os.path.dirname(__file__) + '/../new.oui.txt'

search_url = 'https://hwaddress.com/?q='

#
class Vendor():
    """Random functions needed for extension to function"""


    def file_to_dict():

        #parse file into a dictionary
        with open(vendor_file) as f:
            for line in f:
                mac, vendor = line.strip().split(None, 1)
                vendor_dict[mac] = vendor.strip()
        #return dictionary
        return vendor_dict

    def format_mac(mac, group=2, char=':'):
        """Properly format mac address if user input has no delimiter or incorrect delimiter
        """
        mac = mac.replace(' ', '')
        # if mac is properly formatted
        if mac[2] == ':':
            mac = mac[0:8]
            return mac.upper()
        # if mac is fomatted with '-' as delimiter
        elif mac[2] == '-':
            mac = mac.replace('-', ":")
            return mac.upper()[0:8]
        elif mac[2] == '.':
            return 'Not a Mac! Check Format'
        else:
            # If mac had no delimiter
            mac = char.join(mac[i:i+group] for i in range(0, len(mac), group))
            return mac[0:8].upper()

    def search_vendor(mac):

        # Setup dictionary
        dict = Vendor.file_to_dict()
        key = mac
        new_list = []
        # check ditionary for query
        if key in dict:
            value = dict[key]
            vendor = re.sub(r'\t', ' ', value.replace(',', ' '))
            # new_list.append(re.sub(r'\t', ' ', value.replace(',', ' ')))
            # return new_list
            # list = {
            #     "vendor": new_list,
            #     "url": search_url + mac
            # }

            list = {
                0: {"vendor": value,
                    "url": search_url + mac}
            }

            return list
            # return new_list

        else:
            new_list.append('Not Found!')
            # list = {
            #     "vendor": new_list,
            #     "url": 'Not Found!'
            # }
            list = {
                0: {"vendor": value,
                    "url": 'Not Found!'}
            }
            return list

            # return new_list
#
# list = Vendor.search_vendor("DC:71:96")
#
# print(list[0]['vendor'])
# print(list[0]['url'])
