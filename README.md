# LSB-Criptografador
Criptografador de imagem a partir do método LSB.

# Ferramenta de Esteganografia LSB em Python
Uma ferramenta de linha de comando simples e eficaz para esconder e revelar mensagens em arquivos de imagem PNG usando a técnica de Esteganografia LSB (Least Significant Bit).

# Visão Geral
Este projeto permite que você oculte uma mensagem de texto secreta em uma imagem. A técnica LSB modifica os bits menos significativos dos pixels da imagem, o que é imperceptível a olho nu, mas armazena dados de forma segura.

# Funcionalidades
hide: Esconde uma mensagem em uma imagem.
reveal: Revela a mensagem que está escondida em uma imagem.

# Pré-requisitos
Para usar este programa, você precisará ter o Python 3 instalado em seu sistema.

# Instalação
A única dependência externa é a biblioteca Pillow para manipulação de imagens. Você pode instalá-la facilmente com o pip:
py pip -m install Pillow


# Como Usar
1. Escondendo uma Mensagem
Use o comando hide seguido pelo caminho da imagem de entrada, o caminho da imagem de saída e a mensagem a ser escondida (entre aspas).
py projetolsbcripto.py hide caminho/da/imagem.png nova_imagem.png "Sua mensagem secreta aqui."


2. Revelando uma Mensagem
Use o comando reveal seguido pelo caminho da imagem que contém a mensagem oculta.
py projetolsbcripto.py reveal nova_imagem.png


# Detalhes Técnicos
A mensagem é codificada bit a bit e cada bit é inserido no bit menos significativo dos canais de cor (RGB) de cada pixel da imagem. Para garantir que o programa saiba onde a mensagem termina, uma sequência de quatro caracteres de ampersand (&&&&) é adicionada ao final da mensagem original. Esta sequência age como um terminador, permitindo que o programa pare de ler os dados da imagem no ponto certo.
