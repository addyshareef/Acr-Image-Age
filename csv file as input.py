import os
import csv
import datetime
import docker

def get_image_creation_date(image_id, client):
    image_info = client.images.get(image_id)
    created_date_str = image_info.attrs['Created']
    created_date = datetime.datetime.strptime(created_date_str, '%Y-%m-%dT%H:%M:%S.%fZ')
    return created_date

def delete_old_images(images, client, max_age_days):
    for image in images:
        image_id = image['Id']
        creation_date = get_image_creation_date(image_id, client)
        current_date = datetime.datetime.now()
        age = (current_date - creation_date).days
        if age > max_age_days:
            print(f"Deleting image {image_id} created {age} days ago.")
            client.images.remove(image_id)
            print(f"Image {image_id} deleted.")

if __name__ == "__main__":
    csv_file_path = input("Enter the path to the CSV file: ")
    max_age_days = 60

    client = docker.from_env()

    try:
        with open(csv_file_path, 'r') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            images = list(csv_reader)
            delete_old_images(images, client, max_age_days)
    except FileNotFoundError:
        print("CSV file not found.")
    except Exception as e:
        print(f"An error occurred: {e}")
