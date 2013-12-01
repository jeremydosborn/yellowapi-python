__author__ = 'jeremy osborn'

# This module returns business details from the Yellow Pages "Places" API
# See YellowAPI docs for API details -- http://www.yellowapi.com/docs/places/

import urllib2
import re
import xml.etree.ElementTree as ET
import time


class YellowAPI:

    def __init__(self, what, city, prov, pglen, uid, apikey, errlogpath):
        self.what = str(what)
        self.city = str(city)
        self.prov = str(prov)
        self.pglen = str(pglen)
        self.uid = str(uid)
        self.apikey = str(apikey)
        self.root = None
        self.errlogpath = errlogpath

    def find_businesses(self):

        # build url for the YellowAPI in sandox format, returns xml by default.
        req = 'http://api.sandbox.yellowapi.com/FindBusiness/?what=' + self.what + '&where=' \
              + self.city + '&pgLen=' + self.pglen + '&UID=' + self.uid + '&apikey=' + self.apikey
        response = urllib2.urlopen(req)
        tree = ET.parse(response)
        self.root = tree.getiterator('Listing')

    def get_business_details(self):

        businessdetails = list()

        if self.errlogpath:
            errlogfile = open(self.errlogpath + time.strftime("%b %d %Y %H%M%S") + '.txt', 'w')

        # if self.root is None then need to make a call to find_businesses first.
        if not self.root:
                errlogfile.write("Error: tried to get business details before calling find business.")
                return None

        for listing in self.root:

            time.sleep(1)  # API doesn't allow more than 1 call per second in sandbox env, email for higher limit

            # replace all non-alphanumeric chars with '-' as required by API spec
            listingname = re.sub('[^0-9a-zA-Z]+', '-', listing[0].text)
            listingid = listing.get('id')
            province = re.sub('[^0-9a-zA-Z]+', '-', self.prov)
            city = re.sub('[^0-9a-zA-Z]+', '-', self.city)

            # now call to the API to get business details
            req2 = 'http://api.sandbox.yellowapi.com/GetBusinessDetails/?prov=' + province \
                   + '&city=' + city + '&bus-name=' + listingname + '&listingId=' + listingid \
                   + '&lang=en&fmt=xml&apikey=yq7axj3rx4rk9bettc4fjmna&UID=127.0.0.1'
            response2 = urllib2.urlopen(req2)
            tree2 = ET.parse(response2)

            # parse business details from element tree
            try:
                name = tree2.findtext('Name')
                street = tree2.findtext('Address/Street')
                city = tree2.findtext('Address/City')
                province = tree2.findtext('Address/Prov')
                postal = tree2.findtext('Address/Pcode')
                phones = tree2.findtext('Phones/Phone/DisplayNum')
                logo = tree2.findtext('Logos/Logo')
                url = tree2.findtext('Products/WebUrl')
                # more fields available, check API docs for details

                business = (name, street, city, province, postal, phones, logo, url)
                businessdetails.append(business)

            except AttributeError as a:
                if self.errlogpath:
                    errlogfile.write(str(a,))

        return businessdetails


def main():
    yellow = YellowAPI("restaurant", "some city", "someprovince", 10, "127.0.0.1", "yourapikeyhere",
                       "/Users/legerton/Desktop/")
    yellow.find_businesses()
    businessdetails = yellow.get_business_details()
    print businessdetails

main()
