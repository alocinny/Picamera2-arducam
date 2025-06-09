# Picamera2-arducam

## Como Fazer Funcionar com o Picamera2 e Opencv

**1. Instalação e Configuração da Câmera**
Antes de usar a câmera em seu código, é importante que o hardware e os drivers estejam corretamente instalados e configurados 

- Intale o driver da câmera: A arducam fornece um script de instalação para os drivers necessários. Baixe e execute o script para instalar o suporte da libcamera e o driver do kernel para a IMX519

```
wget -O install_pivariety_pkgs.sh https://github.com/ArduCAM/Arducam-Pivariety-V4L2-Driver/releases/download/install_script/install_pivariety_pkgs.sh
chmod +x install_pivariety_pkgs.sh
./install_pivariety_pkgs.sh -p libcamera_dev
./install_pivariety_pkgs.sh -p libcamera_apps
./install_pivariety_pkgs.sh -p imx519_kernel_driver
```

**`Após a instalação, reinicie o Raspberry Pi.`**

- Habilite a câmera: Use o comando sudo raspi-config, navegue até Interface options e certifique-se de que Legacy Camera está desabilitado. A IMX519 funciona com a interface CSI moderna.
- Teste a câmera: Verifique se a câmera é detectada e funciona com os utilitários da libcamera

```
libcamera-still -t 5000 -o test.jpg
```

**2. Instale as bibliotecas necessárias para funcionar o script**

```
sudo apt update
sudo apt install -y python3-picamera2 python3-opencv
```
