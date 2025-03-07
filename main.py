from eth_account import Account
import secrets


def generate_private_keys(num_keys=10):
    """
    Generate Ethereum private keys and save them to private_keys.txt
    
    Args:
        num_keys (int): Number of keys to generate (default: 10)
    """
    # Enable the new account creation
    Account.enable_unaudited_hdwallet_features()
    
    private_keys = []
    # Generate the specified number of private keys
    for _ in range(num_keys):
        private_key = secrets.token_hex(32)
        private_keys.append(private_key)
    
    # Create or open the file in write mode
    with open('private_keys.txt', 'w') as f:
        for private_key in private_keys:
            f.write(f'0x{private_key}\n')
    
    return private_keys

def extract_addresses(private_keys=None):
    """
    Extract Ethereum addresses from private keys and save them to addresses.txt
    
    Args:
        private_keys (list): List of private keys (optional)
    """
    # Enable the new account creation
    Account.enable_unaudited_hdwallet_features()
    
    # If private keys are not provided, read them from private_keys.txt
    if private_keys is None:
        private_keys = []
        try:
            with open('private_keys.txt', 'r') as f:
                for line in f:
                    # Each line should contain only a private key
                    private_key = line.strip()
                    if private_key:  # Skip empty lines
                        private_keys.append(private_key)
        except FileNotFoundError:
            print("Error: private_keys.txt file not found.")
            return []
    
    addresses = []
    # Create or open the file in write mode
    with open('addresses.txt', 'w') as f:
        for private_key in private_keys:
            # Create an account from the private key
            # Handle keys that might already have the 0x prefix
            if not private_key.startswith('0x'):
                account_key = '0x' + private_key
            else:
                account_key = private_key
                
            account = Account.from_key(account_key)
            # Extract the address
            address = account.address
            addresses.append(address)
            # Write to file - just the address
            f.write(f'{address}\n')
    
    return addresses

def generate_keys_and_addresses(num_keys=10):
    """
    Generate private keys and extract addresses, saving both to their respective files
    
    Args:
        num_keys (int): Number of keys to generate (default: 10)
    """
    # Generate private keys
    private_keys = generate_private_keys(num_keys)
    print(f"Successfully generated {num_keys} private keys and saved to private_keys.txt")
    
    # Extract addresses
    # Since we need to add 0x prefix for Account.from_key, let's add it to the private keys
    prefixed_keys = ['0x' + pk for pk in private_keys]
    extract_addresses(prefixed_keys)
    print(f"Successfully extracted {num_keys} addresses and saved to addresses.txt")

def display_menu():
    """Display the menu options and get user selection"""
    print("\n===== Ethereum Wallet Generator =====")
    print("1. Generate private keys")
    print("2. Extract addresses from private keys")
    print("3. Generate private keys and addresses")
    print("4. Exit")
    choice = input("Enter your choice (1-4): ")
    return choice

def main():
    """Main function to run the program"""
    while True:
        choice = display_menu()
        
        if choice == '1':
            try:
                num_keys = int(input("How many private keys do you want to generate? "))
                generate_private_keys(num_keys)
                print(f"Successfully generated {num_keys} private keys and saved to private_keys.txt")
            except ValueError:
                print("Please enter a valid number.")
            except Exception as e:
                print(f"An error occurred: {str(e)}")
        
        elif choice == '2':
            try:
                extract_addresses()
                print("Successfully extracted addresses and saved to addresses.txt")
            except Exception as e:
                print(f"An error occurred: {str(e)}")
        
        elif choice == '3':
            try:
                num_keys = int(input("How many keys do you want to generate? "))
                generate_keys_and_addresses(num_keys)
            except ValueError:
                print("Please enter a valid number.")
            except Exception as e:
                print(f"An error occurred: {str(e)}")
        
        elif choice == '4':
            print("Exiting the program. Goodbye!")
            break
        
        else:
            print("Invalid choice. Please select a number between 1 and 4.")

if __name__ == '__main__':
    main()
