import os
import io
import tensorflow as tf
from PIL import Image
import PyPDF2

class PDFCompressor:
    def __init__(self, input_file_path, output_file_path=None):
        self.input_file_path = input_file_path
        if output_file_path:
            self.output_file_path = output_file_path
        else:
            self.output_file_path = os.path.splitext(input_file_path)[0] + '_shrunk.pdf'
        
    def compress(self, max_size=5*1024*1024):
        # Open the input PDF file
        with open(self.input_file_path, 'rb') as input_file:
            # Read the PDF content
            input_pdf = PyPDF2.PdfFileReader(input_file)

            # Create a PDF writer object
            output_pdf = PyPDF2.PdfFileWriter()

            # Iterate over the pages of the input PDF file
            for i in range(input_pdf.getNumPages()):
                # Get the page object
                page = input_pdf.getPage(i)

                # Extract the image from the page and convert it to a Pillow image
                image = self.extract_image(page)
                if image is not None:
                    # Compress the image using Tensorflow and Pillow
                    compressed_image = self.compress_image(image)

                    # Replace the original image in the PDF page with the compressed image
                    self.replace_image(page, compressed_image)

                # Add the page to the output PDF file
                output_pdf.addPage(page)

            # Open the output PDF file for writing
            with open(self.output_file_path, 'wb') as output_file:
                # Write the output PDF content
                output_pdf.write(output_file)

            # Check if the output file size is below the maximum allowed size
            if os.path.getsize(self.output_file_path) > max_size:
                print(f"Error: Failed to shrink PDF file '{self.input_file_path}'. Output file size is {os.path.getsize(self.output_file_path)} bytes.")
            else:
                print(f"Success: PDF file '{self.input_file_path}' has been shrunk to below {max_size} bytes and saved as '{self.output_file_path}'.")

    @staticmethod
    def extract_image(page):
        # Check if the page contains any images
        if '/XObject' not in page['/Resources']:
            return None

        # Get the first image object on the page
        xObject = page['/Resources']['/XObject'].getObject()
        image = None
        for obj in xObject:
            if xObject[obj]['/Subtype'] == '/Image':
                image = xObject[obj]

        # Check if the image is a JPEG or a PNG
        if image['/Filter'] == '/DCTDecode':
            return Image.open(io.BytesIO(image._data))
        elif image['/Filter'] == '/FlateDecode':
            return Image.open(io.BytesIO(image._data)).convert('RGB')
        else:
            return None

    @staticmethod
    def compress_image(image):
        # Convert the Pillow image to a Tensorflow tensor
        tensor = tf.keras.preprocessing.image.img_to_array(image)

        # Normalize the pixel values
        tensor /= 255.

        # Add a batch dimension to the tensor
        tensor = tf.expand_dims(tensor, axis=0)

        # Define the compression model
        model = tf.keras.Sequential([
            tf.keras.layers.Conv2D(filters=32, kernel_size=(3,3), activation='relu', padding='same', input_shape=tensor.shape[1:]),
            tf.keras.layers.MaxPooling2D(pool_size=(2,2)),
            tf.keras.layers.Conv2D(filters=64, kernel_size=(3,3), activation='relu', padding='same'),
            tf.keras.layers.MaxPooling2D(pool_size=(2,2)),
            tf.keras.layers.Conv2D(filters=128, kernel_size=(3,3), activation='relu', padding='same'),
            tf.keras.layers.MaxPooling2D(pool_size=(2,2)),
            tf.keras.layers.Flatten(),
            tf.keras.layers.Dense(units=1024, activation='relu'),
            tf.keras.layers.Dense(units=512, activation='relu'),
            tf.keras.layers.Dense(units=256, activation='relu'),
            tf.keras.layers.Dense(units=128, activation='relu'),
            tf.keras.layers.Dense(units=64, activation='relu'),
            tf.keras.layers.Dense(units=32, activation='relu'),
            tf.keras.layers.Dense(units=16, activation='relu'),
            tf.keras.layers.Dense(units=8, activation='relu'),
            tf.keras.layers.Dense(units=4, activation='relu'),
            tf.keras.layers.Dense(units=1, activation='sigmoid')
        ])

        # Compile the model
        model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

        # Compress the image using the model
        compressed_tensor = model.predict(tensor)

        # Convert the compressed tensor back to a Pillow image
        compressed_image = tf.keras.preprocessing.image.array_to_img(compressed_tensor[0] * 255.)

        return compressed_image


    @staticmethod
    def compress_pdf(input_file_path: str, output_file_path: str):
        # Open the input PDF file
        with open(input_file_path, 'rb') as input_file:
            # Create a PDF reader object
            reader = PyPDF2.PdfReader(input_file)

            # Create a PDF writer object
            writer = PyPDF2.PdfWriter()

            # Iterate over the pages of the input PDF file
            for i in range(reader.numPages):
                # Get the page object
                page = reader.pages[i]

                # Convert the page to a Pillow image
                image = page.to_image()

                # Compress the image
                compressed_image = PDFCompressor.compress_image(image)

                # Convert the compressed image back to a PDF page and add it to the output PDF file
                compressed_page = PyPDF2.pdf.PageObject.createBlankPage(reader, page.mediaBox.getWidth(), page.mediaBox.getHeight())
                compressed_page.addImage(compressed_image)
                writer.addPage(compressed_page)

            # Open the output PDF file for writing
            with open(output_file_path, 'wb') as output_file:
                # Write the output PDF content
                writer.write(output_file)

            # Check if the output file size is below the maximum allowed size
            if os.path.getsize(output_file_path) > PDFCompressor.MAX_FILE_SIZE:
                print(f"Error: Failed to compress PDF file '{input_file_path}'. Output file size is {os.path.getsize(output_file_path)} bytes.")
            else:
                print(f"Success: PDF file '{input_file_path}' has been compressed and saved as '{output_file_path}'.")

if __name__ == '__main__':
    input_file_path = 'Resume_Jingyi_Li.pdf'
    output_file_path = os.path.splitext(input_file_path)[0] + '_compressed.pdf'
    PDFCompressor.compress_pdf(input_file_path, output_file_path)

pdf_compressor = PdfCompressor('Resume_Jingyi_Li.pdf', 'compressed_resume.pdf')
pdf_compressor.compress()
