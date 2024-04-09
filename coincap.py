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

            # Save data to csv file 
            df = pd.DataFrame(coin_data)
            csv_filename = f"cryptocurrency_data_{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.csv"
            df.to_csv(csv_filename, index=False)

            # Create SQLite table 
            conn = sqlite3.connect('cryptocurrency_data.db')
            cur = conn.cursor()
            cur.execute("""
            CREATE TABLE IF NOT EXISTS cryptocurrencies(
                id INTEGER PRIMARY KEY, 
                name TEXT,
                symbol TEXT,
                price_usd REAL, 
                fetch_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """)

            # Save data into cryptocurrencies table
            for coin in coin_data: 
                cur.execute("""
                INSERT INTO cryptocurrencies (name, symbol, price_usd)
                VALUES (?, ?, ?)
                """, (coin['name'], coin['symbol'], coin['priceUsd'])
                )

            conn.commit()
            cur.close()
            conn.close()
            print(f"{len(coin_data)} records inserted successfully into SQLite at {datetime.datetime.now()}!")

        else:
            print(f"Error: {response.status_code} - {response.reason}")

    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")

def main() -> None: 
    fetch_coin_data()

if __name__ == '__main__':
    main()