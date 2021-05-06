import copy
from collections import Counter
import requests, sys, argparse, os, datetime
from utils import generate_token_OTP, get_beneficiaries, check_and_book, get_districts, get_pincodes, beep, \
    BENEFICIARIES_URL, WARNING_BEEP_DURATION, get_vaccine_preference


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--token', help='Pass token directly')
    args = parser.parse_args()

    mobile = None
    try:
        base_request_header = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'
        }

        # if args.token:
        #     token = args.token
        # else:
        #     mobile = input("Enter the registered mobile number: ")
        #     token = generate_token_OTP(mobile, base_request_header)

        request_header = copy.deepcopy(base_request_header)
        # request_header["Authorization"] = f"Bearer {token}"

        # Get Beneficiaries
        # print("Fetching registered beneficiaries.. ")
        # beneficiary_dtls = get_beneficiaries(request_header)

        # if len(beneficiary_dtls) == 0:
        #     print("There should be at least one beneficiary. Exiting.")
        #     os.system("pause")
        #     sys.exit(1)

        # Make sure all beneficiaries have the same type of vaccine
        # vaccine_types = [beneficiary['vaccine'] for beneficiary in beneficiary_dtls]
        # vaccines = Counter(vaccine_types)

        # if len(vaccines.keys()) != 1:
        #     print(f"All beneficiaries in one attempt should have the same vaccine type. Found {len(vaccines.keys())}")
        #     os.system("pause")
        #     sys.exit(1)

        vaccine_type = 0
        # if not vaccine_type:
        #     print("\n================================= Vaccine Info =================================\n")
        #     vaccine_type = get_vaccine_preference()

        # print("\n================================= Location Info =================================\n")
        # # get search method to use
        # search_option = input("""Search by Pincode? Or by State/District? \nEnter 1 for Pincode or 2 for State/District. (Default 2) : """)
        # search_option = int(search_option) if int(search_option) in [1, 2] else 2

        # if search_option == 2:
        #     # Collect vaccination center preferance
        #     location_dtls = get_districts(request_header)
        # else:
            # Collect vaccination center preferance
        search_option = 1
        location_dtls = get_pincodes()

        print("\n================================= Additional Info =================================\n")

        # Set filter condition
        minimum_slots = int(input("What is min number of slots u need ?"))

        min_age_booking = int(input("Enter age group, 18 or 45: "))

        # Get refresh frequency
        refresh_freq = input('How often do you want to refresh the calendar (in seconds)? Default 15. Minimum 5. : ')
        refresh_freq = int(refresh_freq) if refresh_freq and int(refresh_freq) >= 5 else 600

        
        start_date = input('Search for next seven day starting from when?\nUse 1 for today, 2 for tomorrow, or provide a date in the format yyyy-mm-dd. Default 2: ')
        if not start_date:
            start_date = 2
        elif start_date in ['1', '2']:
            start_date = int(start_date)
        else:
            try:
                datetime.datetime.strptime(start_date, '%Y-%m-%d')
            except ValueError:
                start_date = 2

        token_valid = True
        while token_valid:
            request_header = copy.deepcopy(base_request_header)
            # call function to check and book slots
            check_and_book(request_header, location_dtls, search_option,
                                         min_slots=minimum_slots,
                                         ref_freq=refresh_freq,
                                         start_date=start_date,
                                         vaccine_type=vaccine_type,
                                         min_age_booking=min_age_booking)

    except Exception as e:
        print(str(e))
        print('Exiting Script')
        os.system("pause")


if __name__ == '__main__':
    main()

