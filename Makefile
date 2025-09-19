# Name of the addon folder
ADDON_NAME = misc_blender_addons
ZIP_NAME = $(ADDON_NAME).zip

# Default target
all:
	mkdir misc_blender_addons
	cp *.py misc_blender_addons/
	zip -r $(ZIP_NAME) misc_blender_addons/
	rm -rf misc_blender_addons/

# Clean up the zip
clean:
	rm -f $(ZIP_NAME)