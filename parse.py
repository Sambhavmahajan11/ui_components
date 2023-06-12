import cv2
import os
import xml.etree.ElementTree as ET
from draw2 import draw_all_bounding_boxes 

# Path to the directory containing XML annotations
xml_dir = './yolo_train/ui/'

# Output path for storing the annotations
annotation_dir = './yolo_train/annotations/'
classes=set()
# Function to recursively find UI components within the node
def find_ui_components(node, image_width, image_height):
    ui_components = []
    class_name = node.get('class')
    if class_name is not None:
        class_name = class_name.split('.')[-1]  # Extract class name from the class attribute
        classes.add(class_name)
        bndbox = node.get('bounds')
        coords = bndbox.strip('[]').replace('][', ',').split(',')
        xmin, ymin = int(coords[0]), int(coords[1])
        xmax, ymax = int(coords[2]), int(coords[3])

        # Normalize bounding box coordinates
        x_center = (xmin + xmax) / (2.0 * image_width)
        y_center = (ymin + ymax) / (2.0 * image_height)
        box_width = (xmax - xmin) / float(image_width)
        box_height = (ymax - ymin) / float(image_height)

        ui_components.append((class_name, x_center, y_center, box_width, box_height, (xmin, ymin, xmax, ymax)))

    # Recursively search for UI components within child nodes
    for child_node in node.findall('node'):
        ui_components.extend(find_ui_components(child_node, image_width, image_height))

    return ui_components

# Create the annotation directory if it doesn't exist
if not os.path.exists(annotation_dir):
    os.makedirs(annotation_dir)

# Iterate through XML annotations directory
for filename in os.listdir(xml_dir):
    if filename.endswith('.xml'):
        xml_path = os.path.join(xml_dir, filename)
        image_path = os.path.splitext(xml_path)[0] + '.png'  # Assuming images have the same filename but with .jpg extension

        # Load the image
        image = cv2.imread(image_path)
        if image is None:
            print(f"Failed to load image: {image_path}")
            continue

        # Get image size
        image_height, image_width, _ = image.shape

        # Parse the XML file
        tree = ET.parse(xml_path)
        root = tree.getroot()

        # Find UI components recursively within the root node
        yolo_annotations = find_ui_components(root, image_width, image_height)

        # Draw rectangles on the image for each UI component
        for annotation in yolo_annotations:
            class_name, x_center, y_center, box_width, box_height, bbox = annotation
            xmin, ymin, xmax, ymax = bbox

            # Scale the coordinates back to the original image size
            xmin = int(xmin * image_width)
            ymin = int(ymin * image_height)
            xmax = int(xmax * image_width)
            ymax = int(ymax * image_height)


        # Write the YOLO annotation file
        annotation_filename = os.path.splitext(filename)[0] + '.txt'
        annotation_path = os.path.join(annotation_dir, annotation_filename)
        with open(annotation_path, 'w') as f:
            for annotation in yolo_annotations:
                line = f"{annotation[0]} {annotation[1]} {annotation[2]} {annotation[3]} {annotation[4]}\n"
                f.write(line)

# Call the function to draw bounding boxes for all annotation files
draw_all_bounding_boxes(annotation_dir, xml_dir)
print(len(classes))
with open("classes.names", 'w') as f:
            for name in classes:
                line = f"{name}\n"
                f.write(line)