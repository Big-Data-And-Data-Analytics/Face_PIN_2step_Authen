from imutils import paths
import os
import cv2
import recognition_system

class evaluationCls:

    def read_images(self, parent_folder_path):
        image_path = list(paths.list_images(parent_folder_path))

        total_images = len(image_path)
        images_matched = 0

        for (i, imagePath) in enumerate(image_path):
            print("**Image {0} of {1}**".format(i + 1, len(image_path)))
            folder_name = imagePath.split(os.path.sep)[-2]
            folder_name = folder_name.split("/")[-1]
            print(f"folder name: {folder_name}")
            image = cv2.imread(imagePath)

            image = cv2.resize(image, (100, 100))

            name = recognition_system.start(image)
            print(f"recognized image: {name}")

            if folder_name.lower() == name.lower():
                images_matched += 1

        overall_accuracy = images_matched / total_images
        print(f"overall accuracy: {overall_accuracy}")


if __name__ == '__main__':
    # start - pass parent folder path, parent folder containing sub-folders. Each sub-folder has name of a person and his/her images
    path = "./test_images/"

    obj = evaluationCls()
    obj.read_images(path)