import sys

# check if we got any arguments, if so run the main function and pass the argument to it
# if not, open an idle window where you can edit settings and credentials
if len(sys.argv) > 1:
	from Main import main
	main(sys.argv[1])
else:
	from Modules.GUI import createIdleWindow
	createIdleWindow()
