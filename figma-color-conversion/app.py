import argparse
import json
from pathlib import Path

parser = argparse.ArgumentParser(description="Convert Figma color to Dart color")
parser.add_argument("--file", default="colors.json", type=str, help="Output file name")
parser.add_argument(
    "--output", default="colors.dart", type=str, help="Output file name"
)
args = parser.parse_args()


def color_to_dart(name, r, g, b, a):
    return (f"const {name} = Color(0x{a}{r}{g}{b});",)


with open(args.file, "r") as f:
    data = json.load(f)
    path = Path(args.output)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w") as of:
        for var in data["variables"]:
            if var["type"] != "COLOR":
                continue

            rgb = var["resolvedValuesByMode"]["4798:0"]
            if "resolvedValue" in rgb:
                rgb = rgb["resolvedValue"]

            r = hex(int(rgb["r"] * 255)).replace("0x", "").upper()
            g = hex(int(rgb["g"] * 255)).replace("0x", "").upper()
            b = hex(int(rgb["b"] * 255)).replace("0x", "").upper()
            a = hex(int(rgb["a"] * 255)).replace("0x", "").upper()

            name: str = var["name"]
            name = name.replace(" ", "")
            name = name.replace("-", "")
            name = name.replace("/", "")

            print(
                color_to_dart(name, r, g, b, a),
                file=of,
            )
