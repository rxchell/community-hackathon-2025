import toml
import os

output_dir = ".streamlit"
output_file = os.path.join(output_dir, "secrets.toml")

# Make sure the directory exists
os.makedirs(output_dir, exist_ok=True)

with open("firestore-key.json") as json_file:
    json_text = json_file.read()

config = {"textkey": json_text}
toml_config = toml.dumps(config)

with open(output_file, "w") as target:
    target.write(toml_config)