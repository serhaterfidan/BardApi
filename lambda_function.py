import requests
import json
import boto3
from bs4 import BeautifulSoup

def get_fuel_prices(il, ilce):
    base_url = 'https://www.doviz.com/akaryakit-fiyatlari'
    url = f'{base_url}/{il}/{ilce}'

    response = requests.get(url)
    if response.status_code == 200:
        html_content = response.text
        soup = BeautifulSoup(html_content, 'html.parser')
        tbody = soup.find('tbody')
        rows = tbody.find_all('tr')

        prices = []

        for row in rows:
            columns = row.find_all('td')
            marka = columns[1].text.strip()
            benzin = columns[2].text.strip()
            motorin = columns[3].text.strip()
            lpg = columns[4].text.strip()
            katkilimotorin = columns[5].text.strip()
            katkilibenzin = columns[6].text.strip()
            tarih = columns[7].text.strip()

            prices.append({
                'marka': marka,
                'benzin': benzin,
                'motorin': motorin,
                'lpg': lpg,
                'katkilimotorin': katkilimotorin,
                'katkilibenzin': katkilibenzin,
                'tarih': tarih
            })

        output = {'prices': prices}

        # Write JSON data to a file
        with open('output.json', 'w') as file:
            json.dump(output, file)


        # Upload the JSON file to Amazon S3
        s3 = boto3.client('s3')
        s3.upload_file('output.json', 'fuelprices', 'data.json')
        
        # Update the bucket policy to allow public access to the file
        bucket_policy = {
            'Version': '2012-10-17',
            'Statement': [{
                'Sid': 'PublicReadGetObject',
                'Effect': 'Allow',
                'Principal': '*',
                'Action': ['s3:GetObject'],
                'Resource': f'arn:aws:s3:::fuelprices/data.json'
            }]
        }

        s3.put_bucket_policy(
            Bucket='fuelprices',
            Policy=json.dumps(bucket_policy)
        )

        return output
    else:
        print(f"Error accessing URL: {response.status_code}")


# Usage example
il = 'aydin'
ilce = 'kusadasi'
prices = get_fuel_prices(il, ilce)
print(prices)
