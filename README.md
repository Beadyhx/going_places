# Going_Places

The script uses a Google Maps API to download photos of places in the area specified by coordinates and search radius.
Results may be found in folder with coordinates. The script saves no more than 10 photos for each place.

## Installation
### Cloning a repository

```bash
git clone https://github.com/Beadyhx/going_places
python -m pip install wget requests
```

## Usage

Add your Google Maps API key to the config.py file

```bash
apikey = 'YOUR_API_KEY_HERE'
```

Run going_places.py with your Python version

```bash
python going_places.py
```

## License

MIT © [going_places](https://github.com/Beadyhx/going_places)
