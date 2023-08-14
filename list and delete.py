from azure.identity import DefaultAzureCredential
from azure.mgmt.containerregistry import ContainerRegistryManagementClient
from azure.mgmt.containerregistry.models import ContainerRegistryCredential

def list_images(acr_name, resource_group_name):
    credentials = DefaultAzureCredential()
    registry_client = ContainerRegistryManagementClient(credentials, "<azure_subscription_id>")

    repository_list = registry_client.repositories.list(resource_group_name, acr_name)
    
    for repo in repository_list:
        tag_list = registry_client.tags.list(resource_group_name, acr_name, repo.name)
        for tag in tag_list:
            print(f"Repository: {repo.name}, Tag: {tag.name}")

def delete_image(acr_name, resource_group_name, repository_name, tag_name):
    credentials = DefaultAzureCredential()
    registry_client = ContainerRegistryManagementClient(credentials, "<azure_subscription_id>")
    
    print(f"Deleting image: {repository_name}:{tag_name}")
    registry_client.manifests.delete(resource_group_name, acr_name, repository_name, tag_name)

if __name__ == "__main__":
    acr_name = "<acr_name>"
    resource_group_name = "<resource_group_name>"
    
    list_images(acr_name, resource_group_name)
    
    delete_confirmation = input("Do you want to delete an image? (yes/no): ")
    
    if delete_confirmation.lower() == "yes":
        repository_name = input("Enter the repository name: ")
        tag_name = input("Enter the tag name: ")
        delete_image(acr_name, resource_group_name, repository_name, tag_name)
        print("Image deleted successfully.")
    else:
        print("Deletion canceled.")
