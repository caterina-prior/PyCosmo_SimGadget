class PowerSpectrumClass:
    def read_param_file(self, file_path):
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