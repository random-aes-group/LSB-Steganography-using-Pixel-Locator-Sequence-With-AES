import LSB as lsb
import AES as Cipher
import os
import fire
class Demo:
    @staticmethod
    def encrypt(
        input_image_path,
        output_image_path,
        secret_message,
        password_text,
        pls_password
    ):
        # Deletes output image if already exists
        if os.path.exists(output_image_path):
            os.remove(output_image_path)

        # clean PLS encryption cache
        if os.path.exists("pls.txt.enc"):
            os.remove("pls.txt.enc")
        if os.path.exists("pls.txt"):
            os.remove("pls.txt")

        if os.path.exists(input_image_path):
            # AES encrpytion
            encoded_message = Cipher.encrypt(secret_message, password_text)
            print(encoded_message)
            # LSB encoding and output image
            lsb.lsb_encode(input_image_path, output_image_path, encoded_message, pls_password)
            
            # clean PLS encryption cache
            if os.path.exists("pls.txt"):
                os.remove("pls.txt")
        else: 
            print("Image is not Present")
    
    @staticmethod
    def decrypt(
        output_image_path,
        password_text,
        pls_password
    ):
        password_text = str(password_text)
        pls_password = str(pls_password)
        if os.path.exists("pls.txt.enc"):
            decoded_text = lsb.lsb_decode(
                output_image_path,
                pls_password
            )
            print(decoded_text)
            # password = input("Enter the password :")
            decrypted_message = Cipher.decrypt(decoded_text, password_text)
            print("Final decrypted message :", decrypted_message)
        else :
            print("PLS file is not present !")


fire.Fire(Demo)

# main()
