from django.shortcuts import render
from django.http import HttpResponse
from .check import *
from unidecode import unidecode
import mimetypes
import base64
import io
p = 11
q = 17
public_key, private_key = generate_keypair(p, q)

def encryption(request):
    if request.method == 'POST':
        encryption_type = request.POST.get('encryption_type')
        # print(encryption_type)
        if encryption_type == 'text':
            text = request.POST.get('text')
            orig_text = text
            text = unidecode(text)
            ciphertext = encrypt(public_key, text)
            return render(request, 'encryption.html', {'ciphertext': ciphertext, 'origtext': orig_text})
        elif encryption_type == 'file':
            file = request.FILES['file']
            file_content = file.read().decode('utf-8')
            file_name = file.name
            file_type = mimetypes.guess_type(file_name)[0]
            print(file_content)
            file_content = unidecode(file_content)
            # Encrypt the file content
            ciphertext = encrypt(public_key, file_content)
            print(ciphertext)
            ciphertext_str = ", ".join(str(c) for c in ciphertext)
            # Convert the encrypted data to Base64-encoded form
            ciphertext_base64 = base64.b64encode(bytes(ciphertext))

            # Create a new file object in memory
            encrypted_file = io.BytesIO()
            encrypted_file.write(ciphertext_str.encode('utf-8'))

            # Set the file pointer at the beginning of the file object
            encrypted_file.seek(0)

            # Return the encrypted file as a response
            response = HttpResponse(encrypted_file, content_type=file_type)
            response['Content-Disposition'] = f'attachment; filename="enc_{file_name}"'

            return response

    return render(request, 'encryption.html')

def decryption(request):
    if request.method == 'POST':
        decryption_type = request.POST.get('decryption_type')
        # print(decryption_type)
        if decryption_type == 'text':
            ciphertext = request.POST.get('ciphertext')
            text = decrypt(private_key, ciphertext)
            # print(text)
            translation_table = {
            'ts': 'ц', 'ia': 'я', 'zh': 'ж', 'kh': 'х', 'ch': 'ч', 'shchit': 'щить', 'sh': 'ш', 'a': 'а', 'b': 'б', 'c': 'ц', 'd': 'д', 'e': 'е', 'f': 'ф', 'g': 'г',
            'h': 'х', 'i': 'и', 'j': 'й', 'k': 'к', 'l': 'л', 'm': 'м', 'n': 'н',
            'o': 'о', 'p': 'п', 'q': 'к', 'r': 'р', 's': 'с', 't': 'т', 'u': 'у',
            'v': 'в', 'w': 'в', 'x': 'кс', 'y': 'ы', 'z': 'з', 
            'A': 'А', 'B': 'Б', 'C': 'Ц', 'D': 'Д', 'E': 'Е', 'F': 'Ф', 'G': 'Г',
            'H': 'Х', 'I': 'И', 'J': 'Й', 'K': 'К', 'L': 'Л', 'M': 'М', 'N': 'Н',
            'O': 'О', 'P': 'П', 'Q': 'К', 'R': 'Р', 'S': 'С', 'T': 'Т', 'U': 'У',
            'V': 'В', 'W': 'В', 'X': 'КС', 'Y': 'Ы', 'Z': 'З', 
            }
            # text = text.translate(str.maketrans(translation_table))
            for source, target in translation_table.items():
                text = text.replace(source, target)
            return render(request, 'decryption.html', {'text': text, 'ciphertext': ciphertext})
        elif decryption_type == 'file':
            file = request.FILES['file']
            file_content = file.read().decode('utf-8')
            file_name = file.name
            file_type = mimetypes.guess_type(file_name)[0]
            # print(file_content)
            # Encrypt the file content
            text = decrypt(private_key, file_content)
            # print(text)
            ciphertext_str = text
            translation_table = {
            'ts': 'ц', 'ia': 'я', 'zh': 'ж', 'a': 'а', 'b': 'б', 'c': 'ц', 'd': 'д', 'e': 'е', 'f': 'ф', 'g': 'г',
            'h': 'х', 'i': 'и', 'j': 'й', 'k': 'к', 'l': 'л', 'm': 'м', 'n': 'н',
            'o': 'о', 'p': 'п', 'q': 'к', 'r': 'р', 's': 'с', 't': 'т', 'u': 'у',
            'v': 'в', 'w': 'в', 'x': 'кс', 'y': 'ы', 'z': 'з', 
            'A': 'А', 'B': 'Б', 'C': 'Ц', 'D': 'Д', 'E': 'Е', 'F': 'Ф', 'G': 'Г',
            'H': 'Х', 'I': 'И', 'J': 'Й', 'K': 'К', 'L': 'Л', 'M': 'М', 'N': 'Н',
            'O': 'О', 'P': 'П', 'Q': 'К', 'R': 'Р', 'S': 'С', 'T': 'Т', 'U': 'У',
            'V': 'В', 'W': 'В', 'X': 'КС', 'Y': 'Ы', 'Z': 'З', 
            }
            for source, target in translation_table.items():
                ciphertext_str = ciphertext_str.replace(source, target)
            # Create a new file object in memory
            encrypted_file = io.BytesIO()
            encrypted_file.write(ciphertext_str.encode('utf-8'))

            # Set the file pointer at the beginning of the file object
            encrypted_file.seek(0)

            # Return the encrypted file as a response
            response = HttpResponse(encrypted_file, content_type=file_type)
            response['Content-Disposition'] = f'attachment; filename="dec_{file_name}"'

            return response    
    return render(request, 'decryption.html')