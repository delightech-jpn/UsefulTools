# ��l�Ǘ��A�v�� �݌v��

## 1. �V�X�e���T�v
�i�ڂ��Ƃ́u��l�i�ň��l�j�v���Ǘ����A���͂��ꂽ���i�E���ʂ���v�Z�����P�����ߋ��̋L�^��������΍X�V����A�v���B  
**�t�����g�G���h�iHTML�j** �� **FastAPI�iRender.com�j** �� **Google Apps Script (GAS)** �� **Google Spreadsheet** �̗���Ńf�[�^���擾�E�X�V����B

---

## 2. �V�X�e���\���}

```mermaid
flowchart TB
    A[�u���E�U\n(HTML + JavaScript)] -->|HTTP GET/POST| B[FastAPI\n(Render.com)]
    B -->|GET/POST (mode�w��)| C[GAS Web App]
    C -->|Spreadsheet API| D[Google Spreadsheet]
    D -->|�i�ځE���i�f�[�^| C
    C -->|JSON���X�|���X| B
    B -->|JSON���X�|���X| A
```

---

## 3. �@�\�ꗗ

### (1) �t�����g�G���h�iHTML�j
- **�i�ڑI��/����**
  - `<input list="items">` �ɂ��ADB�iSpreadsheet�j����擾�����i�ڌ���\���B
  - ���ɂȂ��ꍇ�͎���͉\�i�V�K�o�^���[�h�j�B
- **�Q�Ɨ̈�**
  - �I�������i�ڂ̒�l���i���i�E���ʁE�P���j��\���B
  - �擾���́u�ǂݍ��ݒ�...�v��\���B
- **���͗̈�**
  - �V�������i�E���ʂ���͂��A�u�o�^�v�{�^���ōX�V�B
  - �P���͎����v�Z���ĎQ�Ɛ�p�t�B�[���h�ɕ\���B
- **�V�K�o�^���[�h**
  - �i�ږ���DB�ɑ��݂��Ȃ��ꍇ�A�����I�ɐV�K�o�^���[�h�ŏ����B
- **UI�\��**
  - �u�Q�Ɨ̈�v�Ɓu���͗̈�v���㉺�ɕ��ׁA���ꂼ��g���ň͂ށB
- **��l�X�V���\��**  
  - �u�o�^�v�{�^��������A�X�V��������������܂Łu�X�V��...�v���Q�Ɨ̈�ɕ\���B
- **�X�V��̎Q�Ə�񎩓��X�V**  
  - �X�V����������A�ŐV�̒�l�����擾���A�Q�Ɨ̈���ŐV������B

---

### (2) FastAPI�iRender.com�j
���ϐ� `GAS_WEBHOOK_URL` �� GAS �� URL ��ݒ�B

- **GET `/items`**
  - mode=`list` ��GAS�ɕi�ڈꗗ�擾���˗����AJSON�ԋp�B

- **GET `/item_detail?item=XXX`**
  - mode=`all_data` ��GAS����S�f�[�^�擾��A�Y���i�ڂ��������ĕԋp�B

- **POST `/update`**
  - newItemMode=True �� mode=`new` ��GAS�֐V�K�o�^�˗��B
  - newItemMode=False �� mode=`search` �Œ�l�X�V�����˗��B
  - �X�V������� `/item_detail` ���Ăяo���A�ŐV����ԋp�B

- **GET `/`**
  - API�ғ��m�F�p�X�e�[�^�X�ԋp�B

---

### (3) Google Apps Script�iGAS�j
- **doGet**
  - `mode=list` �� Spreadsheet�̕i�ڈꗗ��Ԃ��B
  - `mode=detail` �� �I��i�ڂ̏ڍ׃f�[�^��Ԃ��B
- **doPost**
  - `mode=search` �� �Y���i�ڂ̒�l��r�E�X�V�B
  - `mode=new` �� �V�K�i�ړo�^�B
- **�ԋp�f�[�^�`��**
  - JSON�`���i��F`{ "item": "���", "price": 100, "quantity": 3, "unit_price": 33.33 }`�j

---

### (4) Google Spreadsheet �\��
1�s�ڂɃw�b�_�[�A2�s�ڈȍ~�f�[�^�B

| �i�� (item) | ���i (price) | ���� (quantity) | �P�� (unit_price) | �X�V�� (updated_at) |
|-------------|-------------|-----------------|-------------------|---------------------|
| ���      | 100         | 3               | 33.33             | 2025/08/10          |
| �o�i�i      | 150         | 5               | 30.00             | 2025/08/09          |

---

## 4. �f�[�^�t���[

### �X�V��
1. ���[�U��HTML�ŕi�ڂ�I��/���� �� ���i�E���ʂ���́B
2. �u��l�X�V�v�{�^������ �� �u�X�V��...�v�\���J�n�B
3. FastAPI�� `/update` POST�B
4. FastAPI�� mode�i`new` or `search`�j�𔻒肵GAS�֑��M�B
5. GAS��Spreadsheet���X�V�B
6. �X�V���ʂ�FastAPI�ɕԋp�B
7. FastAPI�� `/item_detail` ���Ăяo���čŐV���擾�B
8. HTML�̎Q�Ɨ̈���ŐV�����A�u�X�V��...�v�\���������B

---

## 5. �⑫�d�l
- �P���� `���i �� ����` �ŏ�����2�ʂ܂Ōv�Z�B
- �i�ڏڍ׎擾���E�X�V�������̓��[�f�B���O�\���B
- �V�K�o�^�Ɗ����X�V�͓����t�H�[�����珈���\�B
- CORS�ݒ�ς݁i�t�����g�G���h���璼��API�Ăяo���j�B
