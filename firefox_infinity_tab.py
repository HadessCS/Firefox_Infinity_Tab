import argparse 
import os 
import webbrowser 
from http.server import SimpleHTTPRequestHandler, HTTPServer 
 
# Sample Atom feed content 
ATOM_FEED_CONTENT = '''<?xml version="1.0" encoding="utf-8"?> 
<feed xmlns="http://www.w3.org/2005/Atom"> 
  <!-- ... rest of the content ... --> 
</feed> 
''' 
 
# Function to create a sample Atom file 
def create_sample_atom_file(path): 
    with open(path, 'w') as f: 
        f.write(ATOM_FEED_CONTENT) 
    print(f"Sample Atom file created at {path}") 
 
# Function to serve the file over HTTP 
def serve_file(path): 
    class Handler(SimpleHTTPRequestHandler): 
        def __init__(self, *args, **kwargs): 
            super().__init__(*args, directory=os.path.dirname(path), **kwargs) 
 
    os.chdir(os.path.dirname(path)) 
    port = 8000 
    with HTTPServer(("", port), Handler) as httpd: 
        print(f"Serving {path} at http://0.0.0.0:{port}") 
        httpd.serve_forever() 
 
# Function to open the file locally with Firefox 
def open_with_firefox(path): 
    webbrowser.get('firefox').open_new_tab('file://' + os.path.realpath(path)) 
    print(f"Atom file opened locally in Firefox at {path}") 
 
# Define the argument parser 
parser = argparse.ArgumentParser(description='Create, serve, or open a sample Atom file.') 
group = parser.add_mutually_exclusive_group() 
group.add_argument('--s', action='store_true', help='Serve the file over HTTP.') 
group.add_argument('--path', '-p', type=str, default='firefox_infinity_tab.atom', help='The path to the Atom file.') 
 
group.add_argument('--l', action='store_true', help='Open the file locally with Firefox.') 
 
args = parser.parse_args() 
 
# If no arguments are provided, print help 
if not args.s and not args.l: 
    parser.print_help() 
else: 
    # Check if the Atom file exists; if not, create it 
    if not os.path.exists(args.path): 
        create_sample_atom_file(args.path) 
     
    # Open locally if --l is used 
    if args.l: 
        open_with_firefox(args.path) 
    elif args.s: 
        serve_file("./firefox_infinity_tab.atom")
