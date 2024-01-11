from origin import SharpInfo
import json

if __name__ == "__main__":
    
    test = SharpInfo('Plugin.cs')

    with open("Plugin.json", 'w') as file:
        json.dump(test.data, file, indent=4)
