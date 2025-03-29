def read_param_file(file_path):
    """
    Reads a parameter file and extracts key-value pairs.

    :param file_path: Path to the parameter file
    :return: Dictionary containing parameter key-value pairs
    """
    params = {}
    try:
        with open(file_path, 'r') as file:
            for line in file:
                # Skip comments and empty lines
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                
                # Split key and value
                if '=' in line:
                    key, value = line.split('=', 1)
                    params[key.strip()] = value.strip()
    except FileNotFoundError:
        print(f"Error: File not found at {file_path}")
    except Exception as e:
        print(f"Error reading file: {e}")
    
    return params


# Example usage
if __name__ == "__main__":
    param_file_path = "ngenic/parameterfiles/lsf_16.param"
    parameters = read_param_file(param_file_path)
    for key, value in parameters.items():
        print(f"{key}: {value}")