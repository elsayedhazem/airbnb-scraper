import os

def clear():
    csv_dir = 'C:/Users/user/Desktop/Practice/Python/Scrapy/AirbnbListings/csv/'
    csv_files = os.listdir(csv_dir)
    json_dir = 'C:/Users/user/Desktop/Practice/Python/Scrapy/AirbnbListings/json/'
    json_files = os.listdir(json_dir)
    for file in csv_files: os.remove(csv_dir + file)
    for file in json_files: os.remove(json_dir + file)
    print("JSON and CSV destination folders deleted.")
    
if __name__ == '__main__':
    clear()
