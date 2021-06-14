# WHTR
Whiteboard Handwriting Text Recognition

## Installation
```
pip install -r requirements.txt
```

## Usage
```
python main.py --img_file line.png
```
replace line.png with name of image file. Keep the image file in `images/` directory

## Output
1. In the images directory, a folder with the same name as the image file will be created
2. The folder will contain the images of individual lines numbered from 0 to n
3. A .txt file will be there for each line's image containing it's transcript
