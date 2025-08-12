# ShelfScanApp �O���݌v��

## 1. �A�v���T�v
- �u�w���\��i�v�̓o�^�E�Ǘ��E�X�V���s�� Web �A�v���P�[�V�����B  
- FastAPI + GAS + Google Spreadsheet ��A�g���A���p�\�� UI/UX ��ǋ�����B

## 2. ���p��
- �i���L�ځj

## 3. �@�\�ꗗ
- **�i�ڈꗗ�\��**�F�w���\��i���e�[�u���`���ŕ\��
- **�i�ڒǉ�**�F���i���E���i�E��������͂��o�^
- **�w���ςݍX�V**�F��ԁi`status`�j = `"done"` �ɕύX
- **�������\��**�F�{�^�����쎞�ɃX�s�i�[�{�����ŏ�ԕ\��

## 4. ��ʍ\��

### 4.1 �ꗗ���
���w���i�ڂ̕\�����s��
- �e�[�u���\���i�i���^���i�^�����^��ԁ^����j
- �t�B���^�F��ԁi`status`�j === `"pending"` �̂ݕ\��
- ����{�^���F�w���ς�(�X�e�[�^�X�X�V)

### 4.2 �o�^�t�H�[��
�V�K�ɍw���������i�ڂ̓o�^���s��
- ���͍��ځF�i���i�K�{�j�A���i�i�C�Ӂj�A�����i�C�Ӂj
- �{�^���F�i�ڂ�ǉ��i�������\������j

## 5. �Z�p�\��

| �@�\           | �Z�p�X�^�b�N                     |
|---------------|----------------------------------|
| �t�����g�G���h  | GitHub Pages + HTML/CSS/JS       |
| �o�b�N�G���h    | FastAPI�iRender.com��Ńz�X�g�j |
| �f�[�^�x�[�X    | Google Apps Script + �X�v���b�h�V�[�g |
| �ʒm            | SendGrid API                     |

## 6. FastAPI API�݌v

### GET `/shelf/items`
- **�@�\**�F�w���\��i�̈ꗗ�擾
- **�N�G���p�����[�^�i�C�Ӂj**�F`status=pending`

### POST `/shelf/items`
- **�@�\**�F�w���\��i�̐V�K�o�^
- **���N�G�X�g�{�f�B**�F 
```json
 {
    "name": "���iA",
    "price": 1200,
    "deadline": "2025-08-23"
  }
  ```

### PUT `/shelf/items/{id}`
- **�@�\**�F�w���ς݃X�e�[�^�X�ւ̍X�V
- **���N�G�X�g�{�f�B**�F
```json
  {
    "status": "done"
  }
```

### DELETE `/shelf/items/{id}`
- �@�\�F�i�ڂ̍폜

## 7. GAS�A�g
- FastAPI �� GAS WebApp �� `action` �p�����[�^�t���Ń��N�G�X�g
- GAS ���� Spreadsheet �𑀍�i�ǉ��^�X�V�^�폜�^�ꗗ�j

## 8. GAS API�݌v
shelf_sacn_app(GAS_API�d�l).pdf���Q��

## 9. UI/UX�݌v���j
- **�������\��**�F�X�s�i�[�{�����ύX�{�{�^��������
- **�둀��h�~**�F��d�N���b�N�h�~�A�폜���̊m�F�_�C�A���O
- **���F��**�F�e�[�u���`���A�����i�� `line-through` �\��

