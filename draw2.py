import cv2
import os

# Path to the directory containing annotation files
annotation_dir = './yolo_train/annotations/'

# Path to the directory containing the corresponding images
image_dir = './yolo_train/ui/'

# Function to draw bounding boxes on the image
def draw_bounding_boxes(image_path, annotation_path):
    image = cv2.imread(image_path)
    height, width, _ = image.shape

    with open(annotation_path, 'r') as f:
        lines = f.readlines()

    for line in lines:
        class_label, x_center, y_center, box_width, box_height = map(str,line.split())
        x_center=float(x_center)
        y_center=float(y_center)
        box_width=float(box_width)
        box_height=float(box_height)
        # Convert relative coordinates to absolute coordinates
        xmin = int((x_center - box_width / 2) * width)
        ymin = int((y_center - box_height / 2) * height)
        xmax = int((x_center + box_width / 2) * width)
        ymax = int((y_center + box_height / 2) * height)

        # Draw bounding box on the image
        cv2.rectangle(image, (xmin, ymin), (xmax, ymax), (0, 255, 0), 2)

        # Get class label
        # class_label = classes[int(class_id)]

        # Draw class label on the image
        cv2.putText(image, class_label, (xmin, ymin - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

    # Save the image with bounding boxes
    output_path = os.path.splitext(annotation_path)[0] + '_bbox.jpg'
    cv2.imwrite(output_path, image)

# Function to draw bounding boxes for all annotation files in the directory
def draw_all_bounding_boxes(annotation_dir, image_dir):
    # Iterate through the annotation directory
    for filename in os.listdir(annotation_dir):
        if filename.endswith('.txt'):
            annotation_path = os.path.join(annotation_dir, filename)
            image_filename = os.path.splitext(filename)[0] + '.png'
            image_path = os.path.join(image_dir, image_filename)

            # Check if the corresponding image file exists
            if os.path.isfile(image_path):
                draw_bounding_boxes(image_path, annotation_path)
            else:
                print(f"Image file not found for annotation: {filename}")

# Call the function to draw bounding boxes for all annotation files
draw_all_bounding_boxes(annotation_dir, image_dir)
