import importlib

def CanImportModule(name, package=None):
    # Can the named module be imported dynamically?
    # name : str - The Name of the module 
    # package : str - If Python < 3.4 - package name
    # 
    # Return value : bool - true if module can be imported, else false. 

	try:
		importlib.util.find_spec
	except AttributeError:
		# For Python < 3.4
		return importlib.find_loader(name) is not None
	else:
		# For Python >= 3.4
		return importlib.util.find_spec(name, package=package) is not None

def ImportModule(name,classname,package=None):
    if CanImportModule(name,package) is not None:
        return getattr(importlib.import_module(name), classname)