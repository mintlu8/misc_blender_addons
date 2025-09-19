# Name of the addon folder
ADDON_NAME = misc_blender_addons
ZIP_NAME = $(ADDON_NAME).zip

# Default target
all: $(ZIP_NAME)

# Create the zip
$(ZIP_NAME):
	zip $(ZIP_NAME) *.py

# Clean up the zip
clean:
	rm -f $(ZIP_NAME)