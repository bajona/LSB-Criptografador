import argparse
from PIL import Image

def to_binary(data):
    if isinstance(data, str):
        return ''.join([format(ord(i), '08b') for i in data])
    elif isinstance(data, bytes):
        return ''.join([format(i, '08b') for i in data])
    elif isinstance(data, int):
        return format(data, '08b')
    else:
        raise TypeError("Tipo não suportado.")

def hide_message(image_path, message, output_path):
    print(f"Escondendo mensagem em: {image_path}")
    try:
        img = Image.open(image_path, 'r')
    except FileNotFoundError:
        print(f"Erro: O arquivo '{image_path}' não foi encontrado.")
        return

    if img.mode != 'RGB':
        img = img.convert('RGB')
        
    width, height = img.size
    
    terminator = '&&&&'
    binary_message = to_binary(message) + to_binary(terminator)
    message_length = len(binary_message)
    
    required_pixels = message_length // 3
    if required_pixels > width * height:
        print("Erro: Mensagem muito longa para ser escondida nesta imagem.")
        return

    new_img = Image.new('RGB', (width, height))
    data_index = 0
    
    for y in range(height):
        for x in range(width):
            if data_index < message_length:
                r, g, b = img.getpixel((x, y))
                
                if data_index < message_length:
                    r = r & 0xFE | int(binary_message[data_index], 2)
                    data_index += 1
                
                if data_index < message_length:
                    g = g & 0xFE | int(binary_message[data_index], 2)
                    data_index += 1
                
                if data_index < message_length:
                    b = b & 0xFE | int(binary_message[data_index], 2)
                    data_index += 1
                
                new_img.putpixel((x, y), (r, g, b))
            else:
                new_img.putpixel((x, y), img.getpixel((x, y)))

    new_img.save(output_path, 'PNG')
    print(f"Mensagem escondida com sucesso em: {output_path}")

def reveal_message(image_path):
    print(f"Tentando revelar mensagem de: {image_path}")
    try:
        img = Image.open(image_path, 'r')
    except FileNotFoundError:
        print(f"Erro: O arquivo '{image_path}' não foi encontrado.")
        return None
    
    if img.mode != 'RGB':
        img = img.convert('RGB')
        
    width, height = img.size
    binary_message = ""
    terminator_binary = to_binary('&&&&')
    
    for y in range(height):
        for x in range(width):
            r, g, b = img.getpixel((x, y))
            
            binary_message += bin(r)[-1]
            binary_message += bin(g)[-1]
            binary_message += bin(b)[-1]
            
            if binary_message.endswith(terminator_binary):
                break 
        else:
            continue
        break
    
    if binary_message.endswith(terminator_binary):
        message_without_terminator = binary_message[:-len(terminator_binary)]
        
        try:
            decoded_message = ''.join([chr(int(message_without_terminator[i:i+8], 2)) for i in range(0, len(message_without_terminator), 8)])
            print(f"Mensagem revelada com sucesso: {decoded_message}")
            return decoded_message
        except ValueError:
            print("Erro: A mensagem escondida não pôde ser decodificada.")
            return None
    else:
        print("Nenhuma mensagem válida foi encontrada no arquivo.")
        return None

def main():
    parser = argparse.ArgumentParser(description="Ferramenta de esteganografia LSB.")
    subparsers = parser.add_subparsers(dest="command", help="Comando para executar (hide ou reveal)", required=True)

    hide_parser = subparsers.add_parser("hide", help="Esconde uma mensagem.")
    hide_parser.add_argument("input_image", type=str, help="Caminho para a imagem de entrada.")
    hide_parser.add_argument("output_image", type=str, help="Caminho para a imagem de saída.")
    hide_parser.add_argument("message", type=str, help="A mensagem a ser escondida.")

    reveal_parser = subparsers.add_parser("reveal", help="Revela uma mensagem.")
    reveal_parser.add_argument("input_image", type=str, help="Caminho para a imagem que contém a mensagem.")

    args = parser.parse_args()

    if args.command == "hide":
        hide_message(args.input_image, args.message, args.output_image)
    elif args.command == "reveal":
        reveal_message(args.input_image)

if __name__ == "__main__":
    main()
