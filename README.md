Repositório de atividades avaliativas da disciplina 5TAV da Faculdade FAETERJ-RIO
Aluno: Wellington Maciel Guimarães
Professor: José Wilson

AV1: Jogo da velha com algorítmo que faz jogada aleatória, campeã (não perde) e inteligente.
AV2: Sistema com rede neural/inteligência artificial para reconhecimento de espécies de cupins urbanos.

Instalação AV2:
- Baixar projeto;
- Via terminal (powershell, bash, ...), navegue até a pasta "AV2";
- Instale os pacotes python necessários (recomendado instalar em uma env);
  Caso use env.
  - No powershell e bash: pyhton -m venv myenv (myenv é o nome da env, pode-se usar o nome que quiser);
  - para ativar env: .\myenv\Scripts\activate ;
  - para desativar env: .\myenv\Scripts\deactivate.bat ;
- Instale Ultralytics (para treinamento de modelo): pip install ultralytics ;
- Instale Label Studio (para rotulagem de objetos): pip install label-studio ;
- Instale o PyTorch:
  - Caso use CPU: pip3 install torch torchvision torchaudio ;
  - Caso use GPU Nvidia com cuda: pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121 ;
- Para treinamento de modelo: .\train.py ;
- Para uso de modelo treinado: .\predict.py ;

Obs.: Para desinstalar qualquer pacote só trocar a palavra "install" por "uninstall" do comando de instalação do mesmo.
