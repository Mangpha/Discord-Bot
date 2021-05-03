import requests
import json
from APITOKEN import bungie_token

api_key = bungie_token()
BASE_URL = "https://bungie.net/Platform/Destiny2/"

membership_types = {
    'xbox': '1',
    'psn': '2',
    'steam': '3',
    'stadia': '5'
}


class ResponseSum:
    def __init__(self, response):
        self.status = response.status_code
        self.url = response.url
        self.error_code = None
        self.error_status = None
        self.message = None

        if self.status == 200:
            result = response.json()
            self.message = result['Message']
            self.error_status = result['ErrorStatus']
            self.error_code = result['ErrorCode']
            if self.error_code == 1:
                try:
                    self.data = result['Response']
                except Exception:
                    print(
                        "No data in result['Response']"
                    )
                    print(
                        f"Exception: {Exception}"
                    )

            else:
                print(
                    f"No data returned for url: {self.url}\n{self.error_code} was the error code with 200 status")

        else:
            print(f"Request failed for url: {self.url}\nStatus: {self.status}")


def destiny2_api_pub(url, apikey):
    headers = headers = {"X-API-Key": api_key}
    response = requests.get(url, headers=headers)
    return ResponseSum(response)


def SearchDestinyPlayerUrl(username, platform):
    membership_type = membership_types[platform]
    return BASE_URL + 'SearchDestinyPlayer/' + membership_type + '/' + username + '/'


def Destiny2GetProfileUrl(MembershipId, MembershipType, components):
    return BASE_URL + MembershipType + '/' + 'Profile/' + MembershipId + '/?components=' + components


prof = destiny2_api_pub(SearchDestinyPlayerUrl("눙귀", "steam"), api_key)
prof = destiny2_api_pub(Destiny2GetProfileUrl(
    prof.data[0]['membershipId'], str(prof.data[0]['membershipType']), "100"
), api_key)

print(prof.data)
