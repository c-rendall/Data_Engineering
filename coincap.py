import requests 
import sqlite3 
import datetime 
import pandas as pd  

# CoinCap API endpoint for getting cryptocurrency data 
url = 'https://api.coincap.io/v2/assets'

def fetch_coin_data() -> None: 
    try: 
        response = requests.get(url)
        
        if response.status_code == 200: 
            data = response.json()
            coin_data = data['data']

            # Create SQLite table 
            conn = sqlite3.connect('cryptocurrency_data.db')
            cur = conn.cursor()
            cur.execute("""
            CREATE TABLE IF NOT EXISTS cryptocurrencies(
                id TEXT,
                rank INT,
                symbol TEXT,
                name TEXT,
                supply REAL,
                max_supply REAL,
                market_cap_usd REAL,
                volume_usd_24hr REAL,
                price_usd REAL, 
                change_percent_24hr REAL,
                vwap_24hr REAL,
                explorer TEXT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """)

            # Add timestamp to coin data 
            timestamp = datetime.datetime.now()

            # Save data into cryptocurrencies table
            for coin in coin_data: 
                coin['timestamp'] = timestamp
                cur.execute("""
                INSERT INTO cryptocurrencies (id, rank, symbol, name, supply, max_supply, market_cap_usd, volume_usd_24hr,
                                              price_usd, change_percent_24hr, vwap_24hr, explorer, timestamp)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (coin['id'], coin['rank'], coin['symbol'], coin['name'], coin['supply'], coin['maxSupply'],
                      coin['marketCapUsd'], coin['volumeUsd24Hr'], coin['priceUsd'], coin['changePercent24Hr'], coin['vwap24Hr'],
                      coin['explorer'], coin['timestamp'])
                )

            conn.commit()
            cur.close()
            conn.close()

            # Save data to csv file 
            df = pd.DataFrame(coin_data)
            csv_filename = f"cryptocurrency_data_{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.csv"
            df.to_csv(csv_filename, index=False)

            print(f"{len(coin_data)} records inserted successfully into SQLite at {datetime.datetime.now()}!")

        else:
            print(f"Error: {response.status_code} - {response.reason}")

    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")

def main() -> None: 
    fetch_coin_data()

if __name__ == '__main__':
    main()