import python_minifier
import python_minifier.ministring

minified_string: str

with open("src/rename-me.py", "r", encoding="utf-8") as file:
	minified_string = file.read()

print("Source:")
print(minified_string)

minified_string = python_minifier.minify(
	minified_string,
	"src/rename-me.py",
)

print("Minified:")
print(minified_string)

with open("minified/rename-me.py", "w", encoding="utf-8") as file:
	file.write(minified_string)

print("Finished ♥♥♥♥ !")