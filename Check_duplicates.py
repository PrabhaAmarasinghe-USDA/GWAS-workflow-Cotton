def check_duplicates(file_path):
    """
    Check for duplicates in the first column of a text file and show all occurrences.
    
    Args:
        file_path (str): Path to the text file
    
    Returns:
        dict: Dictionary with duplicate values and their full lines
    """
    try:
        # Dictionary to store values and their full lines
        values = {}
        # Dictionary to store duplicate values and their lines
        duplicates = {}
        
        with open(file_path, 'r') as file:
            for line in file:
                # Clean the line and get the first column
                # Split by whitespace while preserving the first word
                first_column = line.strip().split()[0]
                if not first_column:  # Skip empty lines
                    continue
                
                # Store the full line
                if first_column in values:
                    if first_column not in duplicates:
                        duplicates[first_column] = [values[first_column]]
                    duplicates[first_column].append(line.strip())
                else:
                    values[first_column] = line.strip()
        
        return duplicates
    
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        return None
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return None

def remove_duplicates(file_path):
    """
    Remove duplicates from the file while keeping only the first occurrence.
    Creates a backup of the original file.
    
    Args:
        file_path (str): Path to the text file
    """
    try:
        # Create a backup of the original file
        backup_path = file_path + ".bak"
        import shutil
        shutil.copy2(file_path, backup_path)
        print(f"Created backup: {backup_path}")
        
        # Read all lines
        with open(file_path, 'r') as file:
            lines = file.readlines()
        
        # Dictionary to track seen first columns
        seen = set()
        
        # Write only unique lines
        with open(file_path, 'w') as file:
            for line in lines:
                first_column = line.strip().split()[0]
                if first_column not in seen:
                    seen.add(first_column)
                    file.write(line)
        
        print("Duplicates removed successfully.")
        
    except Exception as e:
        print(f"Error removing duplicates: {str(e)}")
        return None

if __name__ == "__main__":
    file_path = "YourFile.txt"
    duplicates = check_duplicates(file_path)
    
    if duplicates:
        print("\nDuplicate names found:")
        for name, lines in duplicates.items():
            print(f"\nName: {name}")
            print(f"Total occurrences: {len(lines)}")
            for i, line in enumerate(lines, 1):
                print(f"Occurrence {i}:")
                print(line)
                print("-" * 80)
        
        # Remove duplicates automatically
        remove_duplicates(file_path)
    else:
        print("No duplicates found or file processed successfully.")
