import python_minifier
import python_minifier.ministring

minified_string: str

with open("src/gui.py", "r", encoding="utf-8") as file:
	minified_string = file.read()

print("Source:")
print(minified_string)

minified_string = python_minifier.minify(
	minified_string,
	"src/gui.py",
)

print("Minified:")
print(minified_string)

with open("minified/gui.py", "w", encoding="utf-8") as file:
	file.write(minified_string)

print("Finished ♥♥♥♥ !")